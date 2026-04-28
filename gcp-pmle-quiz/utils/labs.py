"""Phase 5 — Labs Integration loader + persistence.

Reads `data/labs.json` (the 20 Skills Boost items) and `data/lab_progress.json`
(per-lab status + shared notes + ohhh insights + post-lab quiz attempts).
Atomic writes for progress.
"""

from __future__ import annotations

import json
import os
import random
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field

from models.questions import Question
from utils import DATA_DIR, QUIZ_FILE
from utils.weekly import SECTION_WEIGHTS

LABS_FILE = DATA_DIR / "labs.json"
LAB_PROGRESS_FILE = DATA_DIR / "lab_progress.json"


class Lab(BaseModel):
    id: int
    name: str
    type: str = "course"
    platform: str = "Google Skills"
    url: str = ""
    duration_hours: float = 0.0
    rating: str = "should"
    exam_sections: list[str] = Field(default_factory=list)
    weeks: list[int] = Field(default_factory=list)
    decay_risk: str = "low"
    last_updated_estimate: str | None = None
    console_focus: list[str] = Field(default_factory=list)
    exam_yield_note: str = ""


class PostLabQuizAttempt(BaseModel):
    timestamp: str
    n_questions: int
    n_correct: int
    score: float
    wrong_ids: list[int] = Field(default_factory=list)


class LabProgress(BaseModel):
    status: str = "not_started"  # not_started | in_progress | completed | skipped
    started_at: str | None = None
    completed_at: str | None = None
    shared_notes: str = ""
    ohhh_insights: list[str] = Field(default_factory=list)
    post_lab_quiz_attempts: list[PostLabQuizAttempt] = Field(default_factory=list)


def load_labs() -> list[Lab]:
    if not LABS_FILE.exists():
        return []
    with LABS_FILE.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    labs = [Lab.model_validate(rec) for rec in payload.get("labs", [])]
    labs.sort(key=lambda l: l.id)
    return labs


def get_lab(lab_id: int) -> Lab:
    for l in load_labs():
        if l.id == lab_id:
            return l
    raise ValueError(f"Lab {lab_id} not found")


def labs_for_week(week_num: int) -> list[Lab]:
    return [l for l in load_labs() if week_num in l.weeks]


def _ensure_progress_file() -> None:
    if LAB_PROGRESS_FILE.exists():
        return
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "as_of": datetime.now(timezone.utc).date().isoformat(),
        "labs": {},
    }
    LAB_PROGRESS_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_lab_progress() -> dict[int, LabProgress]:
    _ensure_progress_file()
    with LAB_PROGRESS_FILE.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    out: dict[int, LabProgress] = {}
    for k, v in (payload.get("labs", {}) or {}).items():
        out[int(k)] = LabProgress.model_validate(v)
    return out


def save_lab_progress(progress: dict[int, LabProgress]) -> None:
    _ensure_progress_file()
    payload = {
        "as_of": datetime.now(timezone.utc).date().isoformat(),
        "labs": {str(k): v.model_dump() for k, v in progress.items()},
    }
    tmp = LAB_PROGRESS_FILE.with_suffix(LAB_PROGRESS_FILE.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, LAB_PROGRESS_FILE)


def update_lab(lab_id: int, **fields) -> LabProgress:
    """Merge fields into the existing progress entry; create one if missing."""
    progress = load_lab_progress()
    current = progress.get(lab_id) or LabProgress()
    data = current.model_dump()
    data.update(fields)
    new = LabProgress.model_validate(data)
    progress[lab_id] = new
    save_lab_progress(progress)
    return new


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def post_lab_quiz_questions(lab: Lab, n: int = 15, seed: int | None = None) -> list[Question]:
    """Sample n questions covering this lab's exam_sections.

    Uses the same v3.1-weight stratification as the per-week sampler. Excludes
    mock-pool questions. If the seed is None, derives one from the wall clock
    so each click yields a fresh attempt.
    """
    if not QUIZ_FILE.exists() or not lab.exam_sections:
        return []
    target_sections = set(lab.exam_sections)

    pool: list[Question] = []
    with QUIZ_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                q = Question.model_validate_json(line)
            except Exception:
                continue
            if q.exam_section not in target_sections:
                continue
            if q.mock_pool:
                continue
            pool.append(q)

    if not pool:
        return []

    if seed is None:
        seed = int(datetime.now(timezone.utc).timestamp())
    rng = random.Random(seed)

    by_sub: dict[str, list[Question]] = {}
    for q in pool:
        by_sub.setdefault(q.exam_section or "?", []).append(q)

    take_total = min(n, len(pool))
    parents = {sub.split(".")[0] for sub in by_sub}
    parent_weight_sum = sum(SECTION_WEIGHTS.get(p, 0) for p in parents) or 1

    raw_targets: dict[str, float] = {}
    for sub, qs in by_sub.items():
        parent = sub.split(".")[0]
        parent_share = SECTION_WEIGHTS.get(parent, 0) / parent_weight_sum
        parent_subs = [s for s in by_sub if s.split(".")[0] == parent]
        parent_avail = sum(len(by_sub[s]) for s in parent_subs)
        sub_share = (len(qs) / parent_avail) if parent_avail else 0
        raw_targets[sub] = take_total * parent_share * sub_share

    floors = {sub: int(raw_targets[sub]) for sub in by_sub}
    remainder = take_total - sum(floors.values())
    fractional = sorted(
        ((raw_targets[sub] - floors[sub], sub) for sub in by_sub),
        key=lambda x: (-x[0], x[1]),
    )
    for _, sub in fractional[:remainder]:
        floors[sub] += 1

    selected: list[Question] = []
    leftover: list[Question] = []
    for sub, want in floors.items():
        avail = list(by_sub[sub])
        rng.shuffle(avail)
        take = min(want, len(avail))
        selected.extend(avail[:take])
        leftover.extend(avail[take:])

    if len(selected) < take_total and leftover:
        rng.shuffle(leftover)
        need = take_total - len(selected)
        selected.extend(leftover[:need])

    rng.shuffle(selected)
    return selected[:take_total]


def lab_completion_summary() -> dict:
    labs = load_labs()
    progress = load_lab_progress()
    must_labs = [l for l in labs if l.rating == "must"]
    completed_must = sum(
        1 for l in must_labs if (progress.get(l.id) and progress[l.id].status == "completed")
    )
    in_progress = sum(
        1 for l in labs if (progress.get(l.id) and progress[l.id].status == "in_progress")
    )
    total_completed = sum(
        1 for l in labs if (progress.get(l.id) and progress[l.id].status == "completed")
    )
    hours_logged = sum(
        l.duration_hours for l in labs
        if progress.get(l.id) and progress[l.id].status == "completed"
    )
    must_hours_remaining = sum(
        l.duration_hours for l in must_labs
        if not (progress.get(l.id) and progress[l.id].status == "completed")
    )
    return {
        "total_labs": len(labs),
        "must_labs": len(must_labs),
        "completed_total": total_completed,
        "completed_must": completed_must,
        "in_progress": in_progress,
        "hours_logged": round(hours_logged, 2),
        "must_hours_remaining": round(must_hours_remaining, 2),
    }
