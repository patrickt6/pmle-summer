"""Tests for utils.labs — Phase 5 labs loader, persistence, and post-lab quiz sampler."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import utils.labs as labs_mod
from utils.labs import (
    Lab,
    LabProgress,
    PostLabQuizAttempt,
    get_lab,
    lab_completion_summary,
    labs_for_week,
    load_lab_progress,
    load_labs,
    post_lab_quiz_questions,
    save_lab_progress,
    update_lab,
)


@pytest.fixture
def tmp_progress(tmp_path: Path, monkeypatch):
    fake = tmp_path / "lab_progress.json"
    monkeypatch.setattr(labs_mod, "LAB_PROGRESS_FILE", fake)
    monkeypatch.setattr(labs_mod, "DATA_DIR", tmp_path)
    return fake


def test_load_labs_count():
    labs = load_labs()
    assert len(labs) == 20
    # Sorted by id
    assert [l.id for l in labs] == sorted(l.id for l in labs)


def test_load_labs_required_fields():
    for l in load_labs():
        assert l.id > 0
        assert l.name
        assert l.platform
        assert l.rating in {"must", "should", "skip"}


def test_get_lab_finds_match():
    lab = get_lab(7)
    assert "Keras" in lab.name
    assert lab.duration_hours == 10.75
    assert lab.rating == "must"


def test_get_lab_missing_raises():
    with pytest.raises(ValueError):
        get_lab(999)


def test_labs_for_week_5_includes_keras():
    week5_labs = labs_for_week(5)
    assert any("Keras" in l.name for l in week5_labs)


def test_labs_for_week_handles_no_match():
    assert labs_for_week(999) == []


def test_must_labs_count():
    must = [l for l in load_labs() if l.rating == "must"]
    # Per skills-boost-path.md §5: 14 must items
    assert len(must) == 14


def test_progress_load_empty(tmp_progress):
    assert load_lab_progress() == {}


def test_save_then_load(tmp_progress):
    p = LabProgress(
        status="in_progress",
        started_at="2026-04-28T10:00:00+00:00",
        shared_notes="Patrick: this is a test\nMatty Boy: agreed",
        ohhh_insights=["First insight", "Second insight"],
    )
    save_lab_progress({7: p})
    loaded = load_lab_progress()
    assert 7 in loaded
    assert loaded[7].status == "in_progress"
    assert "Patrick:" in loaded[7].shared_notes
    assert len(loaded[7].ohhh_insights) == 2


def test_atomic_write_no_partial(tmp_progress):
    save_lab_progress({1: LabProgress(status="completed")})
    raw = json.loads(tmp_progress.read_text())
    assert "labs" in raw
    tmp_file = tmp_progress.with_suffix(tmp_progress.suffix + ".tmp")
    assert not tmp_file.exists()


def test_update_lab_creates_entry(tmp_progress):
    p = update_lab(4, status="completed", completed_at="2026-04-28T11:00:00+00:00")
    assert p.status == "completed"
    loaded = load_lab_progress()
    assert loaded[4].status == "completed"


def test_update_lab_merges_fields(tmp_progress):
    update_lab(4, status="in_progress", started_at="2026-04-28T10:00:00+00:00")
    update_lab(4, shared_notes="some notes")  # status should persist
    loaded = load_lab_progress()
    assert loaded[4].status == "in_progress"
    assert loaded[4].shared_notes == "some notes"
    assert loaded[4].started_at == "2026-04-28T10:00:00+00:00"


def test_post_lab_quiz_returns_questions():
    lab = get_lab(7)  # §3.1, §3.2, §4.1
    questions = post_lab_quiz_questions(lab, n=15, seed=1)
    assert len(questions) == 15
    target = set(lab.exam_sections)
    for q in questions:
        assert q.exam_section in target
        assert not q.mock_pool


def test_post_lab_quiz_seed_determinism():
    lab = get_lab(7)
    a = post_lab_quiz_questions(lab, n=15, seed=42)
    b = post_lab_quiz_questions(lab, n=15, seed=42)
    assert [q.id for q in a] == [q.id for q in b]


def test_post_lab_quiz_excludes_mock_pool():
    """All sampled questions must have empty/None mock_pool."""
    for lab in load_labs():
        if not lab.exam_sections:
            continue
        sampled = post_lab_quiz_questions(lab, n=5, seed=0)
        for q in sampled:
            assert not q.mock_pool


def test_completion_summary_empty(tmp_progress):
    summary = lab_completion_summary()
    assert summary["total_labs"] == 20
    assert summary["completed_total"] == 0
    assert summary["completed_must"] == 0
    assert summary["hours_logged"] == 0


def test_completion_summary_after_one_done(tmp_progress):
    update_lab(7, status="completed", completed_at="2026-04-28T11:00:00+00:00")
    summary = lab_completion_summary()
    assert summary["completed_total"] == 1
    assert summary["completed_must"] == 1
    assert summary["hours_logged"] >= 10.75


def test_post_lab_quiz_attempt_appends(tmp_progress):
    update_lab(7, status="in_progress")
    progress = load_lab_progress()
    p = progress[7]
    p.post_lab_quiz_attempts.append(
        PostLabQuizAttempt(
            timestamp="2026-04-28T11:00:00+00:00",
            n_questions=15,
            n_correct=12,
            score=0.80,
            wrong_ids=[100, 200, 300],
        )
    )
    save_lab_progress({7: p})
    loaded = load_lab_progress()
    assert len(loaded[7].post_lab_quiz_attempts) == 1
    assert loaded[7].post_lab_quiz_attempts[0].score == 0.80
