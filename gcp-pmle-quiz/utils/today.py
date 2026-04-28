"""Phase 6a — Today/Plan cursor engine.

Given the active profile's ``study_start_date``, today's date, and the
profile's ``cursor.json`` file, compute:

  - the target Week + Day to surface in the Today UI
  - the on-track delta (days ahead/behind expected)
  - days remaining to the booked exam

Cadence model: each week is Mon–Sun (7 days, day_index 0..6). Mon–Fri are
the focused study days, Sat is the paired lab session, Sun is the
self-assessment quiz. ``manual_override_day`` lets the user jump to any
(week, day) without disturbing ``completed_days``.

This module owns no Streamlit imports — it's pure data so we can unit
test the math.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path

from utils.profiles import current_profile, profile_path
from utils.study_plan import Day, StudyPlan, Week, load_study_plan

DAYS_PER_WEEK = 7
DAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
DAY_ID_RE = re.compile(r"^w(\d+)d(\d+)$")


@dataclass
class CursorState:
    completed_days: list[str] = field(default_factory=list)
    skipped_days: list[str] = field(default_factory=list)
    manual_override_day: str | None = None
    last_active: str = ""


@dataclass
class TodayContext:
    target_week: Week | None
    target_day: Day | None
    expected_week_num: int
    expected_day_index: int
    actual_completed: int
    expected_completed: int
    delta_days: int  # +ve = ahead of schedule, −ve = behind
    days_to_exam: int | None
    is_pre_start: bool
    is_post_plan: bool
    is_override: bool


# ---------- ID helpers ----------


def day_id(week_num: int, day_index: int) -> str:
    return f"w{week_num}d{day_index}"


def parse_day_id(day_id_str: str) -> tuple[int, int] | None:
    m = DAY_ID_RE.match(day_id_str)
    if not m:
        return None
    return (int(m.group(1)), int(m.group(2)))


# ---------- Cursor persistence ----------


def _cursor_file(profile_name: str | None = None) -> Path:
    return profile_path("cursor.json", profile_name)


def load_cursor(profile_name: str | None = None) -> CursorState:
    path = _cursor_file(profile_name)
    if not path.exists():
        return CursorState(last_active=datetime.now(timezone.utc).isoformat())
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f) or {}
    except json.JSONDecodeError:
        data = {}
    return CursorState(
        completed_days=list(data.get("completed_days", [])),
        skipped_days=list(data.get("skipped_days", [])),
        manual_override_day=data.get("manual_override_day"),
        last_active=data.get("last_active", datetime.now(timezone.utc).isoformat()),
    )


def save_cursor(state: CursorState, profile_name: str | None = None) -> None:
    path = _cursor_file(profile_name)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "completed_days": state.completed_days,
        "skipped_days": state.skipped_days,
        "manual_override_day": state.manual_override_day,
        "last_active": state.last_active,
    }
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, path)


# ---------- Calendar math ----------


def expected_position(
    study_start_date: date, today: date, total_weeks: int
) -> tuple[int, int, bool, bool]:
    """Return ``(week_num, day_index, is_pre_start, is_post_plan)``.

    week_num is 1-indexed; day_index is 0-indexed (Mon = 0).
    """
    if total_weeks <= 0:
        return (1, 0, today < study_start_date, False)

    days_since = (today - study_start_date).days
    if days_since < 0:
        return (1, 0, True, False)

    total_days = total_weeks * DAYS_PER_WEEK
    if days_since >= total_days:
        return (total_weeks, DAYS_PER_WEEK - 1, False, True)

    week_num = days_since // DAYS_PER_WEEK + 1
    day_index = days_since % DAYS_PER_WEEK
    return (week_num, day_index, False, False)


def find_day(
    plan: StudyPlan, week_num: int, day_index: int
) -> tuple[Week | None, Day | None]:
    week = next((w for w in plan.weeks if w.num == week_num), None)
    if week is None:
        return (None, None)
    if day_index < 5:
        for d in week.days:
            if d.day_index == day_index:
                return (week, d)
        return (week, None)
    if day_index == 5:
        # Prefer the parsed Saturday lab day; fall back to a Sat bullet in
        # the daily breakdown (week 12's REAL EXAM lives in days[]).
        if week.saturday is not None:
            return (week, week.saturday)
        sat = next((d for d in week.days if d.day_index == 5), None)
        return (week, sat)
    if day_index == 6:
        return (week, week.sunday)
    return (week, None)


def days_to_exam(profile_exam_date: str, today: date | None = None) -> int | None:
    today = today or date.today()
    try:
        exam = date.fromisoformat(profile_exam_date)
    except (ValueError, TypeError):
        return None
    return (exam - today).days


# ---------- Top-level orchestration ----------


def compute_today_context(today: date | None = None) -> TodayContext:
    today = today or date.today()
    profile = current_profile()
    cursor = load_cursor()
    plan = load_study_plan()

    try:
        start = date.fromisoformat(profile.study_start_date)
    except ValueError:
        start = today

    total_weeks = max(len(plan.weeks), 1)
    # By start-of-day N, only the previous N−1 days are "expected done";
    # today itself is still in progress and shouldn't push the user behind.
    expected_completed = max(0, (today - start).days) if today >= start else 0
    actual_completed = len(cursor.completed_days)
    delta = actual_completed - expected_completed

    if cursor.manual_override_day:
        parsed = parse_day_id(cursor.manual_override_day)
        if parsed:
            ow_num, od_idx = parsed
            week, day = find_day(plan, ow_num, od_idx)
            return TodayContext(
                target_week=week,
                target_day=day,
                expected_week_num=ow_num,
                expected_day_index=od_idx,
                actual_completed=actual_completed,
                expected_completed=expected_completed,
                delta_days=delta,
                days_to_exam=days_to_exam(profile.exam_target_date, today),
                is_pre_start=False,
                is_post_plan=False,
                is_override=True,
            )

    exp_week, exp_day, pre, post = expected_position(start, today, total_weeks)
    week, day = find_day(plan, exp_week, exp_day)
    return TodayContext(
        target_week=week,
        target_day=day,
        expected_week_num=exp_week,
        expected_day_index=exp_day,
        actual_completed=actual_completed,
        expected_completed=expected_completed,
        delta_days=delta,
        days_to_exam=days_to_exam(profile.exam_target_date, today),
        is_pre_start=pre,
        is_post_plan=post,
        is_override=False,
    )


# ---------- Mutations ----------


def _touch(state: CursorState) -> None:
    state.last_active = datetime.now(timezone.utc).isoformat()


def mark_day_complete(
    week_num: int, day_index: int, profile_name: str | None = None
) -> CursorState:
    state = load_cursor(profile_name)
    did = day_id(week_num, day_index)
    if did not in state.completed_days:
        state.completed_days.append(did)
    if did in state.skipped_days:
        state.skipped_days.remove(did)
    _touch(state)
    save_cursor(state, profile_name)
    return state


def unmark_day_complete(
    week_num: int, day_index: int, profile_name: str | None = None
) -> CursorState:
    state = load_cursor(profile_name)
    did = day_id(week_num, day_index)
    if did in state.completed_days:
        state.completed_days.remove(did)
    _touch(state)
    save_cursor(state, profile_name)
    return state


def mark_day_skipped(
    week_num: int, day_index: int, profile_name: str | None = None
) -> CursorState:
    state = load_cursor(profile_name)
    did = day_id(week_num, day_index)
    if did not in state.skipped_days:
        state.skipped_days.append(did)
    if did in state.completed_days:
        state.completed_days.remove(did)
    _touch(state)
    save_cursor(state, profile_name)
    return state


def set_manual_override(
    day_id_str: str | None, profile_name: str | None = None
) -> CursorState:
    state = load_cursor(profile_name)
    if day_id_str is not None and parse_day_id(day_id_str) is None:
        raise ValueError(f"Invalid day id '{day_id_str}'; expected format 'wNdM'")
    state.manual_override_day = day_id_str
    _touch(state)
    save_cursor(state, profile_name)
    return state
