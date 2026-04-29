"""Tests for the Plan page module — focuses on the pure helpers + smoke loads.

Streamlit page rendering is tested with the manual-smoke verification step
in 6a verification (launching the dev server and clicking through). Here
we verify the data slice the page consumes is sound, and that referenced
deep links resolve to real artifacts.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

import utils.profiles as profiles_mod
import utils.study_plan as study_plan_mod
import utils.today as today_mod
from utils.profiles import Profile, create_profile, ensure_default_profiles, set_current_profile
from utils.study_plan import Day, StudyPlan, Task, Week
from utils.today import day_id, mark_day_complete, mark_day_skipped, set_manual_override

_APP_DIR = Path(__file__).resolve().parent.parent
_PLAN_PAGE = _APP_DIR / "pages" / "14_🗺_Plan.py"
_spec = importlib.util.spec_from_file_location("plan_page", _PLAN_PAGE)
plan_page = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
_spec.loader.exec_module(plan_page)  # type: ignore[union-attr]


@pytest.fixture
def tmp_app(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(profiles_mod, "PROFILES_DIR", tmp_path / "profiles")
    monkeypatch.setattr(profiles_mod, "APP_SETTINGS_FILE", tmp_path / "app_settings.json")
    monkeypatch.setattr(profiles_mod, "DATA_DIR", tmp_path)
    monkeypatch.setattr(study_plan_mod, "STUDY_PLAN_FILE", tmp_path / "study_plan.json")
    return tmp_path


def _make_week(num: int = 1) -> Week:
    return Week(
        num=num,
        theme=f"Theme {num}",
        exam_sections=["§1.1"],
        days=[
            Day(
                day_label=lbl,
                day_index=i,
                tasks=[Task(type="read", label=f"Task {lbl}")],
            )
            for i, lbl in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri"])
        ],
        saturday=Day(
            day_label="Sat",
            day_index=5,
            tasks=[Task(type="lab", label="Sat lab")],
        ),
        sunday=Day(
            day_label="Sun",
            day_index=6,
            tasks=[Task(type="drill", label="Sunday quiz")],
        ),
    )


def _seed_profile(tmp_path: Path):
    create_profile(
        Profile(
            name="patrick",
            display_name="Patrick",
            study_start_date="2026-04-27",
            exam_target_date="2026-07-26",
        )
    )
    set_current_profile("patrick")


# ---------- Pure helpers ----------


def test_day_status_done(tmp_app):
    _seed_profile(tmp_app)
    mark_day_complete(1, 0)
    cursor = today_mod.load_cursor()
    assert plan_page._day_status(1, 0, cursor, 1, 0) == "done"


def test_day_status_skipped(tmp_app):
    _seed_profile(tmp_app)
    mark_day_skipped(1, 0)
    cursor = today_mod.load_cursor()
    assert plan_page._day_status(1, 0, cursor, 1, 0) == "skipped"


def test_day_status_current(tmp_app):
    _seed_profile(tmp_app)
    cursor = today_mod.load_cursor()
    assert plan_page._day_status(1, 2, cursor, 1, 2) == "current"


def test_day_status_missed(tmp_app):
    _seed_profile(tmp_app)
    cursor = today_mod.load_cursor()
    # Day 1d0 is in the past relative to expected_w=1, expected_d=2 and was not done.
    assert plan_page._day_status(1, 0, cursor, 1, 2) == "missed"


def test_day_status_future(tmp_app):
    _seed_profile(tmp_app)
    cursor = today_mod.load_cursor()
    assert plan_page._day_status(2, 0, cursor, 1, 2) == "future"


def test_resolve_day_weekday():
    week = _make_week()
    day = plan_page._resolve_day(week, 2)
    assert day is not None and day.day_label == "Wed"


def test_resolve_day_saturday_prefers_lab():
    week = _make_week()
    day = plan_page._resolve_day(week, 5)
    assert day is not None and day.day_label == "Sat"
    assert day.tasks[0].type == "lab"


def test_resolve_day_sunday():
    week = _make_week()
    day = plan_page._resolve_day(week, 6)
    assert day is not None and day.day_label == "Sun"


def test_resolve_day_out_of_range():
    week = _make_week()
    assert plan_page._resolve_day(week, 9) is None


# ---------- Deep links are public URLs ----------


def test_real_plan_links_are_public(tmp_app, monkeypatch):
    """No task link should still point at a local research/*.md file."""
    repo_root = _APP_DIR.parent
    md_path = repo_root / "study_plan.md"
    if not md_path.exists():
        pytest.skip("study_plan.md not present in this checkout")
    import importlib.util as _iu
    parser_path = _APP_DIR / "scripts" / "parse_study_plan.py"
    spec = _iu.spec_from_file_location("parse_study_plan", parser_path)
    parser = _iu.module_from_spec(spec)
    spec.loader.exec_module(parser)  # type: ignore[union-attr]
    plan = parser.parse_study_plan(md_path.read_text(encoding="utf-8"))

    http_links = 0
    for w in plan.weeks:
        all_tasks: list[Task] = []
        all_tasks.extend(w.deliverables)
        all_tasks.extend(w.above_and_beyond)
        for d in w.days:
            all_tasks.extend(d.tasks)
        if w.saturday:
            all_tasks.extend(w.saturday.tasks)
        if w.sunday:
            all_tasks.extend(w.sunday.tasks)
        for t in all_tasks:
            for link in t.links:
                assert not link.url.startswith("research/"), (
                    f"Week {w.num} task '{t.label[:40]}…' still points at {link.url}"
                )
                if link.url.startswith("http"):
                    http_links += 1
    assert http_links > 30, "Expected the plan to be peppered with public http(s) links"
