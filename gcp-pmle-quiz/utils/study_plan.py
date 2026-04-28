"""Phase 6a — Structured study-plan loader.

The 12-week plan lives canonically as ``study_plan.md`` (human-edited).
``scripts/parse_study_plan.py`` extracts a structured JSON view at
``data/study_plan.json``; this module loads it at runtime.

Schema is intentionally simple: every "doable thing" surfaces as a
:class:`Task` (read / drill / lab / video / app / external / other).
A :class:`Day` bundles the tasks for a weekday. A :class:`Week` is a
container with metadata + days + deliverables + anchors. The Today
page consumes weeks/days/tasks; the Plan page renders the same view at
the 12-week granularity.
"""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field

from utils import DATA_DIR

STUDY_PLAN_FILE = DATA_DIR / "study_plan.json"


class TaskLink(BaseModel):
    label: str
    url: str


class Task(BaseModel):
    type: str  # "read" | "drill" | "lab" | "video" | "app" | "external" | "other"
    label: str
    description: str = ""
    estimated_min: int | None = None
    ref: str | None = None  # primary URL/path (first link, or in-app target)
    links: list[TaskLink] = Field(default_factory=list)


class Day(BaseModel):
    day_label: str  # "Mon", "Tue", ..., "Sat", "Sun"
    day_index: int  # 0=Mon … 6=Sun
    estimated_min: int | None = None
    description: str = ""
    tasks: list[Task] = Field(default_factory=list)


class Week(BaseModel):
    num: int
    theme: str
    exam_sections: list[str] = Field(default_factory=list)
    estimated_hours: float | None = None
    saturday_lab_label: str | None = None
    saturday_lab_url: str | None = None
    deliverables: list[Task] = Field(default_factory=list)
    concept_anchors: list[str] = Field(default_factory=list)
    days: list[Day] = Field(default_factory=list)
    saturday: Day | None = None
    sunday: Day | None = None
    above_and_beyond: list[Task] = Field(default_factory=list)
    sunday_quiz_target: float | None = None  # 0.70 etc.


class StudyPlan(BaseModel):
    as_of: str
    weeks: list[Week]


def load_study_plan() -> StudyPlan:
    if not STUDY_PLAN_FILE.exists():
        return StudyPlan(as_of="never", weeks=[])
    with STUDY_PLAN_FILE.open("r", encoding="utf-8") as f:
        return StudyPlan.model_validate(json.load(f))


def get_week(num: int) -> Week | None:
    for w in load_study_plan().weeks:
        if w.num == num:
            return w
    return None


def total_weeks() -> int:
    return len(load_study_plan().weeks)
