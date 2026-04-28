"""Tests for utils.week_results — persistent week-quiz results store."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import utils.week_results as wr
from utils.week_results import (
    WeekQuizResult,
    append_week_quiz_result,
    attempts_for_week,
    latest_attempt,
    load_week_quiz_results,
)


@pytest.fixture
def tmp_results_file(tmp_path: Path, monkeypatch):
    """Redirect WEEK_QUIZ_RESULTS_FILE to a temp file so tests don't pollute real data."""
    fake = tmp_path / "week_quiz_results.json"
    monkeypatch.setattr(wr, "WEEK_QUIZ_RESULTS_FILE", fake)
    monkeypatch.setattr(wr, "DATA_DIR", tmp_path)
    return fake


def make_result(week: int = 5, attempt_id: str = "5A", pct: float = 0.80) -> WeekQuizResult:
    return WeekQuizResult(
        week=week,
        attempt_id=attempt_id,
        seed=5001,
        started_at="2026-05-25T13:00:00+00:00",
        finished_at="2026-05-25T13:24:18+00:00",
        duration_s=1458,
        n_questions=20,
        n_correct=int(pct * 20),
        pct=pct,
        passed=pct >= 0.70,
        by_section={"§3.1": [13, 16], "§3.2": [3, 4]},
        wrong_question_ids=[356, 401, 482, 519],
    )


def test_load_empty(tmp_results_file):
    assert load_week_quiz_results() == []


def test_append_then_load(tmp_results_file):
    r = make_result()
    append_week_quiz_result(r)
    loaded = load_week_quiz_results()
    assert len(loaded) == 1
    assert loaded[0].week == 5
    assert loaded[0].attempt_id == "5A"
    assert loaded[0].pct == 0.80


def test_append_preserves_existing(tmp_results_file):
    append_week_quiz_result(make_result(week=5, attempt_id="5A", pct=0.80))
    append_week_quiz_result(make_result(week=5, attempt_id="5B", pct=0.65))
    loaded = load_week_quiz_results()
    assert len(loaded) == 2
    ids = {(r.week, r.attempt_id) for r in loaded}
    assert ids == {(5, "5A"), (5, "5B")}


def test_atomic_write_no_partial(tmp_results_file):
    """If write fails midway, the temp file shouldn't replace the real one."""
    append_week_quiz_result(make_result())
    raw = json.loads(tmp_results_file.read_text())
    assert "results" in raw and len(raw["results"]) == 1
    # Verify no leftover .tmp file
    tmp = tmp_results_file.with_suffix(tmp_results_file.suffix + ".tmp")
    assert not tmp.exists()


def test_latest_attempt_picks_most_recent(tmp_results_file):
    older = WeekQuizResult(
        week=5, attempt_id="5A", seed=5001,
        started_at="2026-05-25T13:00:00+00:00", finished_at="2026-05-25T13:30:00+00:00",
        duration_s=1800, n_questions=20, n_correct=14, pct=0.70, passed=True,
    )
    newer = WeekQuizResult(
        week=5, attempt_id="5A", seed=5001,
        started_at="2026-05-26T13:00:00+00:00", finished_at="2026-05-26T13:30:00+00:00",
        duration_s=1800, n_questions=20, n_correct=18, pct=0.90, passed=True,
    )
    append_week_quiz_result(older)
    append_week_quiz_result(newer)
    found = latest_attempt(5, "5A")
    assert found is not None
    assert found.pct == 0.90


def test_latest_attempt_missing_returns_none(tmp_results_file):
    assert latest_attempt(99, "99X") is None


def test_attempts_for_week_filters_by_week(tmp_results_file):
    append_week_quiz_result(make_result(week=5, attempt_id="5A"))
    append_week_quiz_result(make_result(week=5, attempt_id="5B"))
    append_week_quiz_result(make_result(week=8, attempt_id="8A"))
    week5_attempts = attempts_for_week(5)
    assert {r.attempt_id for r in week5_attempts} == {"5A", "5B"}


def test_keeps_all_attempts_forever(tmp_results_file):
    for i in range(10):
        append_week_quiz_result(make_result(week=5, attempt_id="5A", pct=0.50 + i * 0.04))
    assert len(load_week_quiz_results()) == 10


def test_round_trip_preserves_fields(tmp_results_file):
    original = make_result()
    append_week_quiz_result(original)
    loaded = load_week_quiz_results()[0]
    assert loaded.by_section == original.by_section
    assert loaded.wrong_question_ids == original.wrong_question_ids
    assert loaded.passed == original.passed
