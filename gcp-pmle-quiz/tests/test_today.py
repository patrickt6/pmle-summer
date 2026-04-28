"""Tests for utils.today — Phase 6a date-anchored cursor engine."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest

import utils.profiles as profiles_mod
import utils.study_plan as study_plan_mod
import utils.today as today_mod
from utils.profiles import (
    Profile,
    create_profile,
    ensure_default_profiles,
    profile_path,
    set_current_profile,
)
from utils.study_plan import Day, StudyPlan, Task, Week
from utils.today import (
    CursorState,
    DAYS_PER_WEEK,
    compute_today_context,
    day_id,
    days_to_exam,
    expected_position,
    find_day,
    load_cursor,
    mark_day_complete,
    mark_day_skipped,
    parse_day_id,
    save_cursor,
    set_manual_override,
    unmark_day_complete,
)


@pytest.fixture
def tmp_app(tmp_path: Path, monkeypatch):
    """Redirect profiles + study plan + data dir to a tmp path."""
    profiles_dir = tmp_path / "profiles"
    monkeypatch.setattr(profiles_mod, "PROFILES_DIR", profiles_dir)
    monkeypatch.setattr(profiles_mod, "APP_SETTINGS_FILE", tmp_path / "app_settings.json")
    monkeypatch.setattr(profiles_mod, "DATA_DIR", tmp_path)
    monkeypatch.setattr(study_plan_mod, "STUDY_PLAN_FILE", tmp_path / "study_plan.json")
    return tmp_path


def _seed_plan(tmp_path: Path, n_weeks: int = 12) -> StudyPlan:
    weeks = []
    for n in range(1, n_weeks + 1):
        weeks.append(
            Week(
                num=n,
                theme=f"Week {n} theme",
                exam_sections=["§1.1"],
                estimated_hours=5.0,
                days=[
                    Day(
                        day_label=lbl,
                        day_index=i,
                        estimated_min=60,
                        description=f"task {lbl}",
                        tasks=[Task(type="read", label=f"task {lbl}")],
                    )
                    for i, lbl in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri"])
                ],
                saturday=Day(
                    day_label="Sat",
                    day_index=5,
                    estimated_min=90,
                    description=f"week {n} sat",
                    tasks=[Task(type="lab", label=f"week {n} lab")],
                ),
                sunday=Day(
                    day_label="Sun",
                    day_index=6,
                    description=f"week {n} sun",
                    tasks=[Task(type="drill", label=f"week {n} quiz")],
                ),
                sunday_quiz_target=0.70,
            )
        )
    plan = StudyPlan(as_of="2026-04-28", weeks=weeks)
    target = tmp_path / "study_plan.json"
    target.write_text(plan.model_dump_json(indent=2), encoding="utf-8")
    return plan


def _seed_profile(name: str = "patrick", start: str = "2026-04-27", exam: str = "2026-07-26"):
    create_profile(
        Profile(
            name=name,
            display_name=name.title(),
            study_start_date=start,
            exam_target_date=exam,
        )
    )
    set_current_profile(name)


# ---------- ID helpers ----------


def test_day_id_round_trip():
    assert day_id(3, 4) == "w3d4"
    assert parse_day_id("w3d4") == (3, 4)
    assert parse_day_id("nope") is None


# ---------- expected_position math ----------


def test_expected_position_pre_start():
    start = date(2026, 4, 27)
    today = date(2026, 4, 25)
    w, d, pre, post = expected_position(start, today, total_weeks=12)
    assert pre is True and post is False
    assert (w, d) == (1, 0)


def test_expected_position_first_day():
    start = date(2026, 4, 27)
    today = date(2026, 4, 27)
    w, d, pre, post = expected_position(start, today, total_weeks=12)
    assert (w, d, pre, post) == (1, 0, False, False)


def test_expected_position_mid_week():
    start = date(2026, 4, 27)  # Mon
    today = date(2026, 4, 30)  # Thu
    w, d, _, _ = expected_position(start, today, total_weeks=12)
    assert (w, d) == (1, 3)


def test_expected_position_week_two_monday():
    start = date(2026, 4, 27)
    today = date(2026, 5, 4)  # Mon, +7 days
    w, d, _, _ = expected_position(start, today, total_weeks=12)
    assert (w, d) == (2, 0)


def test_expected_position_post_plan():
    start = date(2026, 4, 27)
    today = date(2026, 8, 1)  # > 84 days
    w, d, pre, post = expected_position(start, today, total_weeks=12)
    assert post is True
    assert (w, d) == (12, 6)


def test_expected_position_zero_weeks():
    start = date(2026, 4, 27)
    today = date(2026, 4, 27)
    w, d, pre, post = expected_position(start, today, total_weeks=0)
    assert (w, d, pre, post) == (1, 0, False, False)


# ---------- find_day ----------


def test_find_day_weekday(tmp_app):
    plan = _seed_plan(tmp_app, n_weeks=2)
    week, day = find_day(plan, 1, 2)  # Wed
    assert week is not None and day is not None
    assert day.day_label == "Wed"


def test_find_day_saturday_prefers_lab_section(tmp_app):
    plan = _seed_plan(tmp_app, n_weeks=2)
    _, day = find_day(plan, 1, 5)
    assert day is not None and day.day_label == "Sat"
    assert day.tasks[0].type == "lab"


def test_find_day_sunday(tmp_app):
    plan = _seed_plan(tmp_app, n_weeks=2)
    _, day = find_day(plan, 1, 6)
    assert day is not None and day.day_label == "Sun"


def test_find_day_missing_week(tmp_app):
    plan = _seed_plan(tmp_app, n_weeks=2)
    week, day = find_day(plan, 99, 0)
    assert week is None and day is None


# ---------- Cursor persistence ----------


def test_load_cursor_when_missing(tmp_app):
    ensure_default_profiles()
    state = load_cursor("patrick")
    assert state.completed_days == []
    assert state.manual_override_day is None


def test_save_then_load_cursor(tmp_app):
    ensure_default_profiles()
    set_current_profile("patrick")
    state = CursorState(completed_days=["w1d0"], skipped_days=[], manual_override_day=None, last_active="2026-04-28T12:00:00Z")
    save_cursor(state)
    loaded = load_cursor()
    assert loaded.completed_days == ["w1d0"]


def test_atomic_write_no_partial(tmp_app):
    ensure_default_profiles()
    set_current_profile("patrick")
    save_cursor(CursorState(completed_days=["w1d0"]))
    cursor_file = profile_path("cursor.json", "patrick")
    tmp = cursor_file.with_suffix(cursor_file.suffix + ".tmp")
    assert not tmp.exists()


# ---------- Mutations ----------


def test_mark_day_complete_idempotent(tmp_app):
    ensure_default_profiles()
    set_current_profile("patrick")
    mark_day_complete(1, 0)
    mark_day_complete(1, 0)
    state = load_cursor()
    assert state.completed_days == ["w1d0"]


def test_mark_day_complete_clears_skip(tmp_app):
    ensure_default_profiles()
    set_current_profile("patrick")
    mark_day_skipped(1, 1)
    mark_day_complete(1, 1)
    state = load_cursor()
    assert "w1d1" in state.completed_days
    assert "w1d1" not in state.skipped_days


def test_mark_day_skipped_clears_complete(tmp_app):
    ensure_default_profiles()
    set_current_profile("patrick")
    mark_day_complete(1, 1)
    mark_day_skipped(1, 1)
    state = load_cursor()
    assert "w1d1" in state.skipped_days
    assert "w1d1" not in state.completed_days


def test_unmark_day_complete(tmp_app):
    ensure_default_profiles()
    set_current_profile("patrick")
    mark_day_complete(1, 0)
    unmark_day_complete(1, 0)
    state = load_cursor()
    assert state.completed_days == []


def test_set_manual_override(tmp_app):
    ensure_default_profiles()
    set_current_profile("patrick")
    set_manual_override("w3d2")
    state = load_cursor()
    assert state.manual_override_day == "w3d2"


def test_set_manual_override_invalid_raises(tmp_app):
    ensure_default_profiles()
    set_current_profile("patrick")
    with pytest.raises(ValueError):
        set_manual_override("not-a-day")


def test_clear_manual_override(tmp_app):
    ensure_default_profiles()
    set_current_profile("patrick")
    set_manual_override("w3d2")
    set_manual_override(None)
    assert load_cursor().manual_override_day is None


# ---------- compute_today_context ----------


def test_today_context_first_day(tmp_app):
    _seed_plan(tmp_app, n_weeks=12)
    ensure_default_profiles()
    _seed_profile("patrick", start="2026-04-27", exam="2026-07-26")
    ctx = compute_today_context(today=date(2026, 4, 27))
    assert ctx.expected_week_num == 1
    assert ctx.expected_day_index == 0
    assert ctx.target_day is not None
    assert ctx.target_day.day_label == "Mon"
    assert not ctx.is_pre_start
    assert not ctx.is_post_plan


def test_today_context_pre_start(tmp_app):
    _seed_plan(tmp_app, n_weeks=12)
    ensure_default_profiles()
    _seed_profile("patrick", start="2026-04-27", exam="2026-07-26")
    ctx = compute_today_context(today=date(2026, 4, 25))
    assert ctx.is_pre_start


def test_today_context_post_plan(tmp_app):
    _seed_plan(tmp_app, n_weeks=12)
    ensure_default_profiles()
    _seed_profile("patrick", start="2026-04-27", exam="2026-07-26")
    ctx = compute_today_context(today=date(2026, 9, 1))
    assert ctx.is_post_plan
    assert ctx.expected_week_num == 12


def test_today_context_on_track(tmp_app):
    _seed_plan(tmp_app, n_weeks=12)
    ensure_default_profiles()
    _seed_profile("patrick", start="2026-04-27", exam="2026-07-26")
    # By start-of-Thu, days Mon/Tue/Wed (3) are expected done.
    mark_day_complete(1, 0)
    mark_day_complete(1, 1)
    mark_day_complete(1, 2)
    ctx = compute_today_context(today=date(2026, 4, 30))  # Thu
    assert ctx.expected_completed == 3
    assert ctx.actual_completed == 3
    assert ctx.delta_days == 0


def test_today_context_behind_schedule(tmp_app):
    _seed_plan(tmp_app, n_weeks=12)
    ensure_default_profiles()
    _seed_profile("patrick", start="2026-04-27", exam="2026-07-26")
    ctx = compute_today_context(today=date(2026, 4, 30))  # Thu, expected 3
    assert ctx.delta_days == -3


def test_today_context_ahead_of_schedule(tmp_app):
    _seed_plan(tmp_app, n_weeks=12)
    ensure_default_profiles()
    _seed_profile("patrick", start="2026-04-27", exam="2026-07-26")
    for d in range(0, 5):
        mark_day_complete(1, d)
    ctx = compute_today_context(today=date(2026, 4, 28))  # Tue, expected 1
    assert ctx.delta_days == 4


def test_today_context_first_day_no_pressure(tmp_app):
    """Start-of-day-1 with nothing done = on track, not 'behind 1 day'."""
    _seed_plan(tmp_app, n_weeks=12)
    ensure_default_profiles()
    _seed_profile("patrick", start="2026-04-27", exam="2026-07-26")
    ctx = compute_today_context(today=date(2026, 4, 27))  # Mon (day 0)
    assert ctx.expected_completed == 0
    assert ctx.delta_days == 0


def test_today_context_manual_override(tmp_app):
    _seed_plan(tmp_app, n_weeks=12)
    ensure_default_profiles()
    _seed_profile("patrick", start="2026-04-27", exam="2026-07-26")
    set_manual_override("w5d2")
    ctx = compute_today_context(today=date(2026, 4, 28))
    assert ctx.is_override
    assert ctx.expected_week_num == 5
    assert ctx.expected_day_index == 2


# ---------- days_to_exam ----------


def test_days_to_exam_positive():
    assert days_to_exam("2026-07-26", today=date(2026, 4, 28)) == 89


def test_days_to_exam_negative_when_past():
    assert days_to_exam("2026-04-01", today=date(2026, 4, 28)) == -27


def test_days_to_exam_invalid_returns_none():
    assert days_to_exam("not-a-date") is None


def test_days_to_exam_in_context(tmp_app):
    _seed_plan(tmp_app, n_weeks=12)
    ensure_default_profiles()
    _seed_profile("patrick", start="2026-04-27", exam="2026-07-26")
    ctx = compute_today_context(today=date(2026, 4, 28))
    assert ctx.days_to_exam == 89


# ---------- Per-profile isolation ----------


def test_cursor_isolated_per_profile(tmp_app):
    _seed_plan(tmp_app, n_weeks=12)
    ensure_default_profiles()
    set_current_profile("patrick")
    mark_day_complete(1, 0)
    mark_day_complete(1, 1)

    set_current_profile("matt")
    matt_state = load_cursor()
    assert matt_state.completed_days == []

    set_current_profile("patrick")
    patrick_state = load_cursor()
    assert patrick_state.completed_days == ["w1d0", "w1d1"]
