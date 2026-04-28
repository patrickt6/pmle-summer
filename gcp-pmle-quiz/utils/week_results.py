"""Persistent store for per-week timed-quiz results.

Lives at `data/week_quiz_results.json`. Separate from `progress.json` so the
Quiz Mode round-by-round tracking stays distinct from the
"I sat the timed Sunday quiz" record. Atomic writes; append-only (we keep
every attempt forever — the file is tiny).
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field

from utils import DATA_DIR

WEEK_QUIZ_RESULTS_FILE = DATA_DIR / "week_quiz_results.json"


class WeekQuizResult(BaseModel):
    week: int
    attempt_id: str  # "5A" / "5B" / "5C" / "remix-<unix>"
    seed: int
    started_at: str  # ISO 8601 UTC
    finished_at: str
    duration_s: int
    n_questions: int
    n_correct: int
    pct: float
    passed: bool
    by_section: dict[str, list[int]] = Field(
        default_factory=dict,
        description="Map exam_section -> [correct, total]",
    )
    wrong_question_ids: list[int] = Field(default_factory=list)


def _ensure_file() -> None:
    if WEEK_QUIZ_RESULTS_FILE.exists():
        return
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    payload = {"as_of": datetime.now(timezone.utc).date().isoformat(), "results": []}
    WEEK_QUIZ_RESULTS_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_week_quiz_results() -> list[WeekQuizResult]:
    _ensure_file()
    with WEEK_QUIZ_RESULTS_FILE.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    return [WeekQuizResult.model_validate(r) for r in payload.get("results", [])]


def append_week_quiz_result(result: WeekQuizResult) -> None:
    _ensure_file()
    with WEEK_QUIZ_RESULTS_FILE.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    payload.setdefault("results", []).append(result.model_dump())
    payload["as_of"] = datetime.now(timezone.utc).date().isoformat()
    tmp = WEEK_QUIZ_RESULTS_FILE.with_suffix(WEEK_QUIZ_RESULTS_FILE.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, WEEK_QUIZ_RESULTS_FILE)


def latest_attempt(week: int, attempt_id: str) -> WeekQuizResult | None:
    candidates = [
        r for r in load_week_quiz_results() if r.week == week and r.attempt_id == attempt_id
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda r: r.finished_at)


def attempts_for_week(week: int) -> list[WeekQuizResult]:
    return [r for r in load_week_quiz_results() if r.week == week]
