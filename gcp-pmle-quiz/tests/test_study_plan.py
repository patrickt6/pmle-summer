"""Tests for the study_plan parser and runtime loader."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

import utils.study_plan as sp_mod
from utils.study_plan import StudyPlan, load_study_plan

# Load scripts/parse_study_plan.py as a module without running its main().
_APP_DIR = Path(__file__).resolve().parent.parent
_PARSER_PATH = _APP_DIR / "scripts" / "parse_study_plan.py"
_spec = importlib.util.spec_from_file_location("parse_study_plan", _PARSER_PATH)
parser_mod = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
sys.modules["parse_study_plan"] = parser_mod
_spec.loader.exec_module(parser_mod)  # type: ignore[union-attr]


SAMPLE_MD = """\
# PMLE 12-Week Study Plan

## Week 1 — Sample
**§s.** §1.1, §1.2 · **Hours.** ~3 · **Sat lab.** [#1 sample lab](https://www.skills.google/course_templates/593)

### 🎯 Theme
sample

### 📦 Hard deliverables
- [ ] Read [v3.1 exam guide](exam.pdf) cover-to-cover.
- [ ] Skills Boost [#1](https://www.skills.google/course_templates/593) (~4h).

### 🧠 Concept anchors
- Anchor one
- Anchor two

### 📅 Daily breakdown
- **Mon (60 min).** Read [exam guide](exam.pdf).
- **Tue (45 min).** Quiz Mode filtered to BQML — 10 Qs.
- **Wed (30 min).** [#1 modules 1–2](https://www.skills.google/course_templates/593).
- **Thu (60 min).** Watch [intro video](https://www.youtube.com/watch?v=abc).
- **Fri (45 min).** Skim [research/concepts/x.md](research/concepts/x.md).

### 🧪 Saturday lab (90 min paired)
[#1 sample lab](https://www.skills.google/course_templates/593) — finish modules.

### 📊 Sunday self-assessment
- **Week 1 Quiz A** ≥ 70 %.
- Wrong-answer drill.

### 🚀 Above-and-beyond
- Run a free-tier lab.

---

## Week 2 — Second
**§s.** §2.1 · **Hours.** ~5 · **Sat lab.** [#4](https://www.skills.google/course_templates/626)

### 📅 Daily breakdown
- **Mon (60 min).** [#4 modules](https://www.skills.google/course_templates/626).
- **Tue (60 min).** Read docs.

### 📊 Sunday self-assessment
- **Week 2 Quiz A** ≥ **65 %**.
"""


# ---------- Parser unit tests on synthetic input ----------


def test_parse_returns_two_weeks():
    plan = parser_mod.parse_study_plan(SAMPLE_MD)
    assert len(plan.weeks) == 2
    assert [w.num for w in plan.weeks] == [1, 2]


def test_week1_metadata():
    w = parser_mod.parse_study_plan(SAMPLE_MD).weeks[0]
    assert w.theme == "Sample"
    assert "§1.1" in w.exam_sections
    assert "§1.2" in w.exam_sections
    assert w.estimated_hours == 3.0
    assert w.saturday_lab_label == "#1 sample lab"
    assert w.saturday_lab_url == "https://www.skills.google/course_templates/593"


def test_week1_days_mon_through_fri():
    w = parser_mod.parse_study_plan(SAMPLE_MD).weeks[0]
    assert [d.day_label for d in w.days] == ["Mon", "Tue", "Wed", "Thu", "Fri"]


def test_day_estimated_min_extracted():
    w = parser_mod.parse_study_plan(SAMPLE_MD).weeks[0]
    assert w.days[0].estimated_min == 60
    assert w.days[1].estimated_min == 45


def test_task_classification_via_links():
    w = parser_mod.parse_study_plan(SAMPLE_MD).weeks[0]
    types = {d.day_label: d.tasks[0].type for d in w.days}
    assert types["Mon"] == "read"  # exam.pdf
    assert types["Tue"] == "drill"  # Quiz Mode keyword
    assert types["Wed"] == "lab"  # skills.google
    assert types["Thu"] == "video"  # youtube
    assert types["Fri"] == "read"  # research/*.md


def test_task_links_captured():
    w = parser_mod.parse_study_plan(SAMPLE_MD).weeks[0]
    assert w.days[2].tasks[0].links[0].url == "https://www.skills.google/course_templates/593"


def test_deliverables_parsed():
    w = parser_mod.parse_study_plan(SAMPLE_MD).weeks[0]
    assert len(w.deliverables) == 2
    labels = " ".join(d.label.lower() for d in w.deliverables)
    assert "exam guide" in labels
    assert "skills boost" in labels


def test_concept_anchors_parsed():
    w = parser_mod.parse_study_plan(SAMPLE_MD).weeks[0]
    assert w.concept_anchors == ["Anchor one", "Anchor two"]


def test_sunday_quiz_target_plain():
    plan = parser_mod.parse_study_plan(SAMPLE_MD)
    assert plan.weeks[0].sunday_quiz_target == 0.70


def test_sunday_quiz_target_with_bold_markup():
    """The week 8 case in real plan uses ≥ **75 %** — bold must not block parse."""
    plan = parser_mod.parse_study_plan(SAMPLE_MD)
    assert plan.weeks[1].sunday_quiz_target == 0.65


def test_saturday_day_present():
    w = parser_mod.parse_study_plan(SAMPLE_MD).weeks[0]
    assert w.saturday is not None
    assert w.saturday.day_index == 5
    assert w.saturday.tasks[0].type == "lab"


def test_above_and_beyond_parsed():
    w = parser_mod.parse_study_plan(SAMPLE_MD).weeks[0]
    assert len(w.above_and_beyond) == 1


def test_parse_no_headers_raises():
    with pytest.raises(ValueError, match="No '## Week"):
        parser_mod.parse_study_plan("# just a heading\n\nno week sections.\n")


# ---------- Real study_plan.md smoke tests ----------


def test_real_study_plan_parses_to_12_weeks():
    md_path = parser_mod.STUDY_PLAN_MD
    if not md_path.exists():
        pytest.skip("study_plan.md not present in this checkout")
    md = md_path.read_text(encoding="utf-8")
    plan = parser_mod.parse_study_plan(md)
    assert len(plan.weeks) == 12
    assert [w.num for w in plan.weeks] == list(range(1, 13))


def test_real_study_plan_every_week_has_metadata():
    md_path = parser_mod.STUDY_PLAN_MD
    if not md_path.exists():
        pytest.skip("study_plan.md not present in this checkout")
    plan = parser_mod.parse_study_plan(md_path.read_text(encoding="utf-8"))
    for w in plan.weeks:
        assert w.theme, f"week {w.num} theme empty"
        assert w.exam_sections, f"week {w.num} exam_sections empty"
        assert w.estimated_hours and w.estimated_hours > 0, f"week {w.num} hours missing"


def test_real_study_plan_every_week_has_daily_bullets():
    md_path = parser_mod.STUDY_PLAN_MD
    if not md_path.exists():
        pytest.skip("study_plan.md not present in this checkout")
    plan = parser_mod.parse_study_plan(md_path.read_text(encoding="utf-8"))
    for w in plan.weeks:
        assert len(w.days) >= 4, f"week {w.num} only parsed {len(w.days)} days"


def test_real_study_plan_week_8_target_75_percent():
    """Week 8 has ≥ **75 %** with bold markup — regression guard for the strip-** fix."""
    md_path = parser_mod.STUDY_PLAN_MD
    if not md_path.exists():
        pytest.skip("study_plan.md not present in this checkout")
    plan = parser_mod.parse_study_plan(md_path.read_text(encoding="utf-8"))
    w8 = next(w for w in plan.weeks if w.num == 8)
    assert w8.sunday_quiz_target == 0.75


def test_real_study_plan_week_12_includes_saturday_in_days():
    """Week 12 daily breakdown includes a Sat bullet with the **Sat: REAL EXAM.** format."""
    md_path = parser_mod.STUDY_PLAN_MD
    if not md_path.exists():
        pytest.skip("study_plan.md not present in this checkout")
    plan = parser_mod.parse_study_plan(md_path.read_text(encoding="utf-8"))
    w12 = next(w for w in plan.weeks if w.num == 12)
    sat_days = [d for d in w12.days if d.day_label == "Sat"]
    assert len(sat_days) == 1


def test_real_study_plan_lab_links_resolve_to_skills_google():
    """Most weekday lab links should resolve to skills.google or official Google docs."""
    md_path = parser_mod.STUDY_PLAN_MD
    if not md_path.exists():
        pytest.skip("study_plan.md not present in this checkout")
    plan = parser_mod.parse_study_plan(md_path.read_text(encoding="utf-8"))
    lab_tasks = [
        t
        for w in plan.weeks
        for d in w.days
        for t in d.tasks
        if t.type == "lab"
    ]
    assert len(lab_tasks) >= 5
    for t in lab_tasks:
        assert t.ref is not None and "skills.google" in t.ref


# ---------- Runtime loader tests ----------


def test_load_study_plan_returns_empty_when_file_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(sp_mod, "STUDY_PLAN_FILE", tmp_path / "missing.json")
    plan = load_study_plan()
    assert plan.weeks == []
    assert plan.as_of == "never"


def test_load_study_plan_round_trip(tmp_path, monkeypatch):
    parsed = parser_mod.parse_study_plan(SAMPLE_MD)
    target = tmp_path / "study_plan.json"
    target.write_text(parsed.model_dump_json(indent=2), encoding="utf-8")
    monkeypatch.setattr(sp_mod, "STUDY_PLAN_FILE", target)
    plan = load_study_plan()
    assert len(plan.weeks) == 2
    assert plan.weeks[0].theme == "Sample"


def test_get_week_returns_match(tmp_path, monkeypatch):
    parsed = parser_mod.parse_study_plan(SAMPLE_MD)
    target = tmp_path / "study_plan.json"
    target.write_text(parsed.model_dump_json(indent=2), encoding="utf-8")
    monkeypatch.setattr(sp_mod, "STUDY_PLAN_FILE", target)

    w = sp_mod.get_week(2)
    assert w is not None
    assert w.theme == "Second"
    assert sp_mod.get_week(99) is None


def test_total_weeks_matches(tmp_path, monkeypatch):
    parsed = parser_mod.parse_study_plan(SAMPLE_MD)
    target = tmp_path / "study_plan.json"
    target.write_text(parsed.model_dump_json(indent=2), encoding="utf-8")
    monkeypatch.setattr(sp_mod, "STUDY_PLAN_FILE", target)
    assert sp_mod.total_weeks() == 2
