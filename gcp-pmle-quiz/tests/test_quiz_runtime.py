"""Tests for utils.quiz_runtime — the shared timed-quiz scoring helpers."""

from __future__ import annotations

import pytest

from models.questions import Question
from utils.quiz_runtime import ScoreResult, format_clock, score


def make_q(qid: int, mode: str, answer, options=None, section: str | None = "§1.1") -> Question:
    options = options or ["A", "B", "C", "D"]
    return Question(
        id=qid,
        mode=mode,
        question=f"Question {qid}",
        options=options,
        answer=answer,
        explanation="explanation",
        exam_section=section,
    )


def test_score_empty():
    result = score([], {})
    assert result.correct == 0
    assert result.total == 0
    assert result.pct == 0.0
    assert result.wrong_items == []


def test_score_single_choice_correct():
    qs = [make_q(1, "single_choice", 2)]
    result = score(qs, {0: 2})
    assert result.correct == 1
    assert result.total == 1
    assert result.pct == 1.0
    assert result.wrong_items == []
    assert result.by_section_total == {"§1.1": 1}
    assert result.by_section_correct == {"§1.1": 1}


def test_score_single_choice_wrong():
    qs = [make_q(1, "single_choice", 2)]
    result = score(qs, {0: 1})
    assert result.correct == 0
    assert result.pct == 0.0
    assert len(result.wrong_items) == 1
    assert result.wrong_items[0][0] == 0  # position
    assert result.wrong_items[0][2] == 1  # the chosen value


def test_score_single_choice_unanswered():
    qs = [make_q(1, "single_choice", 2)]
    result = score(qs, {})
    assert result.correct == 0
    assert len(result.wrong_items) == 1
    # Unanswered shows up as None in wrong_items
    assert result.wrong_items[0][2] is None


def test_score_single_choice_set_response():
    """Single-choice answers may arrive as a single-element set (legacy mock state)."""
    qs = [make_q(1, "single_choice", 2)]
    result = score(qs, {0: {2}})
    assert result.correct == 1


def test_score_multi_choice_correct():
    qs = [make_q(1, "multiple_choice", [0, 2])]
    result = score(qs, {0: {0, 2}})
    assert result.correct == 1


def test_score_multi_choice_partial():
    qs = [make_q(1, "multiple_choice", [0, 2])]
    result = score(qs, {0: {0}})  # missed one
    assert result.correct == 0
    assert len(result.wrong_items) == 1


def test_score_multi_choice_extra():
    qs = [make_q(1, "multiple_choice", [0, 2])]
    result = score(qs, {0: {0, 1, 2}})  # picked extra
    assert result.correct == 0


def test_score_per_section_breakdown():
    qs = [
        make_q(1, "single_choice", 0, section="§1.1"),
        make_q(2, "single_choice", 0, section="§1.1"),
        make_q(3, "single_choice", 0, section="§5.1"),
    ]
    responses = {0: 0, 1: 1, 2: 0}  # 1.1: 1/2, 5.1: 1/1
    result = score(qs, responses)
    assert result.correct == 2
    assert result.by_section_total == {"§1.1": 2, "§5.1": 1}
    assert result.by_section_correct == {"§1.1": 1, "§5.1": 1}


def test_score_uncategorized_section():
    qs = [make_q(1, "single_choice", 0, section=None)]
    result = score(qs, {0: 0})
    assert "(uncategorized)" in result.by_section_total


def test_format_clock_zero():
    assert format_clock(0) == "00:00:00"


def test_format_clock_minute():
    assert format_clock(60) == "00:01:00"


def test_format_clock_hour():
    assert format_clock(3661) == "01:01:01"


def test_format_clock_negative_clamps():
    assert format_clock(-5) == "00:00:00"


def test_format_clock_two_hours():
    assert format_clock(2 * 60 * 60) == "02:00:00"


def test_score_result_is_dataclass():
    assert isinstance(score([], {}), ScoreResult)
