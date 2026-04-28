"""Tests for utils.weekly.sample_quiz_for_week — Phase 4 stratified sampler."""

from __future__ import annotations

import pytest

from utils.weekly import (
    SECTION_WEIGHTS,
    Week,
    load_weeks,
    quizzes_for_week,
    sample_quiz_for_week,
)


@pytest.fixture
def all_weeks() -> list[Week]:
    return load_weeks()


def test_loads_12_weeks(all_weeks):
    assert len(all_weeks) == 12


def test_section_weights_sum_to_100():
    assert sum(SECTION_WEIGHTS.values()) == 100


def test_sampler_size_default(all_weeks):
    """Every week with ≥ 20 in-scope questions returns exactly 20."""
    for w in all_weeks:
        pool = quizzes_for_week(w)
        if len(pool) >= 20:
            sampled = sample_quiz_for_week(w, n_questions=20, seed=0)
            assert len(sampled) == 20, f"Week {w.week}: expected 20, got {len(sampled)}"


def test_sampler_size_30q(all_weeks):
    """Mock-week format (30 Qs) works on weeks with ≥ 30 in-scope."""
    w11 = next(w for w in all_weeks if w.week == 11)
    sampled = sample_quiz_for_week(w11, n_questions=30, seed=0)
    assert len(sampled) == 30


def test_sampler_capped_by_available(all_weeks):
    """If a week has fewer than n in-scope questions, sampler returns what's available."""
    # Find smallest week
    smallest = min(all_weeks, key=lambda w: len(quizzes_for_week(w)))
    avail = len(quizzes_for_week(smallest))
    sampled = sample_quiz_for_week(smallest, n_questions=avail + 50, seed=0)
    assert len(sampled) == avail


def test_sampler_deterministic(all_weeks):
    """Same seed → same set of question IDs in the same order."""
    w5 = next(w for w in all_weeks if w.week == 5)
    a = sample_quiz_for_week(w5, n_questions=20, seed=42)
    b = sample_quiz_for_week(w5, n_questions=20, seed=42)
    assert [q.id for q in a] == [q.id for q in b]


def test_sampler_different_seeds_diverge(all_weeks):
    """Different seeds → significantly different question IDs (≥ 50% novelty) on weeks with ≥ 60 in-scope."""
    big_weeks = [w for w in all_weeks if len(quizzes_for_week(w)) >= 60]
    assert big_weeks, "expected at least one week with ≥60 in-scope questions"
    w = big_weeks[0]
    a_ids = {q.id for q in sample_quiz_for_week(w, n_questions=20, seed=1)}
    b_ids = {q.id for q in sample_quiz_for_week(w, n_questions=20, seed=2)}
    overlap = len(a_ids & b_ids)
    assert overlap < len(a_ids), "fully identical samples means seeds aren't being used"


def test_sampler_excludes_mock_pool_by_default(all_weeks):
    """Default exclude_mock=True means no sampled question carries a mock_pool tag."""
    for w in all_weeks:
        sampled = sample_quiz_for_week(w, n_questions=10, seed=0)
        for q in sampled:
            assert not q.mock_pool, f"Week {w.week}: question {q.id} has mock_pool {q.mock_pool}"


def test_sampler_includes_mock_when_opted_in(all_weeks):
    """Setting exclude_mock=False allows mock-pool questions back in."""
    w5 = next(w for w in all_weeks if w.week == 5)
    incl = sample_quiz_for_week(w5, n_questions=20, seed=0, exclude_mock=False)
    excl = sample_quiz_for_week(w5, n_questions=20, seed=0, exclude_mock=True)
    # Both should be valid samples
    assert len(incl) == 20
    assert len(excl) == 20


def test_sampler_only_returns_in_scope(all_weeks):
    """Every sampled question must have exam_section in the week's scope."""
    for w in all_weeks:
        scope = set(w.exam_sections)
        sampled = sample_quiz_for_week(w, n_questions=10, seed=0)
        for q in sampled:
            assert q.exam_section in scope, (
                f"Week {w.week}: sampled question {q.id} has section {q.exam_section} "
                f"not in scope {scope}"
            )


def test_sampler_unique_ids(all_weeks):
    """Sampled questions are unique within a single attempt (no doubles)."""
    w7 = next(w for w in all_weeks if w.week == 7)
    sampled = sample_quiz_for_week(w7, n_questions=20, seed=0)
    ids = [q.id for q in sampled]
    assert len(ids) == len(set(ids))
