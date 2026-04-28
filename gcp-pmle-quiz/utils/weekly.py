"""Phase 3 weekly-overview loader.

Purely additive: defines Pydantic models for `weeks.json` and `rebrands.json`,
and helpers for looking up a week, scoping the quiz pool to a week's exam
sections, and slicing user progress against that scope.

Does NOT modify utils/__init__.py or models/questions.py.
"""

from __future__ import annotations

import json
import random
from collections import defaultdict
from datetime import date
from pathlib import Path

from pydantic import BaseModel, Field

from models.questions import Question
from utils import DATA_DIR, QUIZ_FILE

# v3.1 weights — also used by Phase 2 mock-pool tagging and Phase 4 quiz sampling
SECTION_WEIGHTS = {"§1": 13, "§2": 14, "§3": 18, "§4": 20, "§5": 22, "§6": 13}

WEEKS_FILE = DATA_DIR / "weeks.json"
REBRANDS_FILE = DATA_DIR / "rebrands.json"

# First Monday of Week 1. Sourced from weeks.json `study_start_date`.
# Used to compute the default week selector value: (today - start).days // 7 + 1.
STUDY_START_DATE = date(2026, 4, 27)


class Lab(BaseModel):
    id: int
    name: str
    platform: str = "Google Skills"
    url: str = ""


class Resource(BaseModel):
    title: str
    url: str
    kind: str = Field(description="One of: official, community, video, paid, book")


class Week(BaseModel):
    week: int
    title: str
    exam_sections: list[str]
    primary_section: str
    hours_target: float
    labs: list[Lab] = Field(default_factory=list)
    research_files: list[str] = Field(default_factory=list)
    decision_trees: list[str] = Field(default_factory=list)
    rebrand_alerts: list[str] = Field(default_factory=list)
    resources: list[Resource] = Field(default_factory=list)
    milestone: str | None = None


class Rebrand(BaseModel):
    old: str
    new: str
    rebranded_at: str
    context: str | None = None
    note: str | None = None


def load_weeks() -> list[Week]:
    """Parse `data/weeks.json` into typed Week objects, ordered by week number."""
    if not WEEKS_FILE.exists():
        return []
    with WEEKS_FILE.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    weeks = [Week.model_validate(w) for w in payload.get("weeks", [])]
    weeks.sort(key=lambda w: w.week)
    return weeks


def load_rebrands() -> list[Rebrand]:
    """Parse `data/rebrands.json` into typed Rebrand objects."""
    if not REBRANDS_FILE.exists():
        return []
    with REBRANDS_FILE.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    return [Rebrand.model_validate(r) for r in payload.get("rebrands", [])]


def get_week(week_num: int) -> Week:
    """Look up a Week by its number; raise ValueError if not found."""
    for w in load_weeks():
        if w.week == week_num:
            return w
    raise ValueError(f"Week {week_num} not found in weeks.json")


def current_week_number(today: date | None = None) -> int:
    """Compute the current study week clamped to [1, 12]."""
    today = today or date.today()
    delta_days = (today - STUDY_START_DATE).days
    week_num = delta_days // 7 + 1
    return max(1, min(12, week_num))


def quizzes_for_week(week: Week, *, exclude_mock: bool = True) -> list[Question]:
    """Return all Questions whose `exam_section` is in this week's scope.

    Defaults to excluding mock-pool questions so they stay held-out for
    Mock #1 / #2 in Weeks 11–12 — the same default the Quiz Mode page uses.
    """
    if not QUIZ_FILE.exists():
        return []
    target_sections = set(week.exam_sections)
    out: list[Question] = []
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
            if exclude_mock and q.mock_pool:
                continue
            out.append(q)
    return out


def sample_quiz_for_week(
    week: Week,
    *,
    n_questions: int = 20,
    seed: int,
    exclude_mock: bool = True,
) -> list[Question]:
    """Stratified random sample of `n_questions` from this week's scope.

    Distribution. For weeks that span multiple sub-sections, the count is
    distributed proportionally to the v3.1 parent-section weights for
    sub-sections that actually appear in the week's scope. Inside a parent
    section, sub-sections share the parent's allocation proportional to
    available-question count. If a sub-section runs out, the shortfall spills
    to whichever sub-section still has the most headroom — small weeks
    naturally end up with overlap (Week 3 has only 24 questions in scope).

    Reproducibility. Fixed `random.Random(seed)`; same seed = same questions
    in the same order.
    """
    pool = quizzes_for_week(week, exclude_mock=exclude_mock)
    if not pool:
        return []

    rng = random.Random(seed)

    by_sub: dict[str, list[Question]] = defaultdict(list)
    for q in pool:
        if q.exam_section:
            by_sub[q.exam_section].append(q)

    available = sum(len(v) for v in by_sub.values())
    if available == 0:
        return []

    take_total = min(n_questions, available)

    # Sum the v3.1 weights only over parent sections actually represented.
    sub_to_parent = {sub: sub.split(".")[0] for sub in by_sub}
    parents_present = set(sub_to_parent.values())
    parent_weight_sum = sum(SECTION_WEIGHTS.get(p, 0) for p in parents_present) or 1

    raw_targets: dict[str, float] = {}
    for sub, parent in sub_to_parent.items():
        parent_share = SECTION_WEIGHTS.get(parent, 0) / parent_weight_sum
        # Within a parent, split by available question count (so §3.1 with 132
        # questions gets more than §3.2 with 17).
        parent_subs = [s for s, p in sub_to_parent.items() if p == parent]
        parent_avail = sum(len(by_sub[s]) for s in parent_subs)
        sub_share = (len(by_sub[sub]) / parent_avail) if parent_avail else 0
        raw_targets[sub] = take_total * parent_share * sub_share

    # Floor + remainder distribution (largest fractional first)
    floors: dict[str, int] = {sub: int(raw_targets[sub]) for sub in by_sub}
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


def progress_for_week(week: Week, progress: dict[int, bool]) -> dict[str, list[int]]:
    """Slice user progress to only this week's quiz IDs.

    Returns a dict with three lists of Question IDs:
      - answered_correctly
      - answered_incorrectly
      - not_answered
    """
    week_qs = quizzes_for_week(week)
    correct: list[int] = []
    incorrect: list[int] = []
    not_answered: list[int] = []
    for q in week_qs:
        if q.id in progress:
            if progress[q.id]:
                correct.append(q.id)
            else:
                incorrect.append(q.id)
        else:
            not_answered.append(q.id)
    return {
        "answered_correctly": correct,
        "answered_incorrectly": incorrect,
        "not_answered": not_answered,
    }
