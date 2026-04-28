"""Mock Exam — timed UI surfacing the 200 held-out questions.

Mock #1 (Week 11 Sat): 50 Qs from `mock1-pool`, 2-hour timed, pass ≥ 70%.
Mock #2 (Week 12 Wed): 50 Qs from `mock2-pool`, 2-hour timed, pass ≥ 80%.

Mock results are NOT written to `data/progress.json` — held-out questions stay
held out for repeat calibration. State lives in `st.session_state` only.
"""

from __future__ import annotations

import collections
import random
import time
from pathlib import Path

import streamlit as st

from models.questions import Question
from utils import QUIZ_FILE, set_css_style
from utils.labs import LabProgress, load_lab_progress, load_labs
from utils.weekly import quizzes_for_week  # not used directly; keeps lazy-loaded modules warm

MOCK_DURATION_SECONDS = 2 * 60 * 60  # 2 hours
MOCK_QUESTION_COUNT = 50
PASS_THRESHOLD = {1: 0.70, 2: 0.80}
POOL_TAG = {1: "mock1-pool", 2: "mock2-pool"}
SHUFFLE_SEED = {1: 110_001, 2: 120_002}


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_pool(mock_num: int) -> list[Question]:
    """Load all questions tagged with this mock's pool, deterministically shuffled."""
    tag = POOL_TAG[mock_num]
    pool: list[Question] = []
    if not QUIZ_FILE.exists():
        return pool
    with QUIZ_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                q = Question.model_validate_json(line)
            except Exception:
                continue
            if q.mock_pool and tag in q.mock_pool:
                pool.append(q)

    rng = random.Random(SHUFFLE_SEED[mock_num])
    rng.shuffle(pool)
    return pool[:MOCK_QUESTION_COUNT]


# ---------------------------------------------------------------------------
# Session state helpers
# ---------------------------------------------------------------------------

def _init_state() -> None:
    st.session_state.setdefault("mock_phase", "idle")  # idle | running | submitted
    st.session_state.setdefault("mock_num", None)
    st.session_state.setdefault("mock_questions", [])
    st.session_state.setdefault("mock_pos", 0)
    st.session_state.setdefault("mock_responses", {})  # pos -> set[int] | int
    st.session_state.setdefault("mock_started_at", None)
    st.session_state.setdefault("mock_finished_at", None)


def _reset_state() -> None:
    for key in (
        "mock_phase",
        "mock_num",
        "mock_questions",
        "mock_pos",
        "mock_responses",
        "mock_started_at",
        "mock_finished_at",
    ):
        if key in st.session_state:
            del st.session_state[key]
    _init_state()


def _start_mock(mock_num: int) -> None:
    questions = load_pool(mock_num)
    if not questions:
        st.error(f"No questions found in `{POOL_TAG[mock_num]}`. Re-run Phase 2 mock-pool tagging.")
        return
    st.session_state.mock_phase = "running"
    st.session_state.mock_num = mock_num
    st.session_state.mock_questions = questions
    st.session_state.mock_pos = 0
    st.session_state.mock_responses = {}
    st.session_state.mock_started_at = time.time()
    st.session_state.mock_finished_at = None


def _submit_mock() -> None:
    st.session_state.mock_phase = "submitted"
    st.session_state.mock_finished_at = time.time()


def _seconds_remaining() -> int:
    started = st.session_state.mock_started_at
    if started is None:
        return MOCK_DURATION_SECONDS
    elapsed = int(time.time() - started)
    return max(0, MOCK_DURATION_SECONDS - elapsed)


def _format_clock(seconds: int) -> str:
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def _score(questions: list[Question], responses: dict[int, set[int] | int | None]) -> dict:
    correct = 0
    by_section_total: dict[str, int] = collections.Counter()
    by_section_correct: dict[str, int] = collections.Counter()
    wrong_items: list[tuple[int, Question, set[int] | int | None]] = []

    for pos, q in enumerate(questions):
        section = q.exam_section or "(uncategorized)"
        by_section_total[section] += 1
        chosen = responses.get(pos)
        is_correct = False

        if chosen is not None:
            if q.mode == "multiple_choice":
                expected = set(q.answer) if isinstance(q.answer, list) else {q.answer}
                got = chosen if isinstance(chosen, set) else {chosen}
                is_correct = expected == got
            else:
                expected_idx = q.answer if isinstance(q.answer, int) else q.answer[0]
                got_idx = next(iter(chosen)) if isinstance(chosen, set) else chosen
                is_correct = got_idx == expected_idx

        if is_correct:
            correct += 1
            by_section_correct[section] += 1
        else:
            wrong_items.append((pos, q, chosen))

    total = len(questions)
    pct = correct / total if total else 0.0
    return {
        "correct": correct,
        "total": total,
        "pct": pct,
        "by_section_total": dict(by_section_total),
        "by_section_correct": dict(by_section_correct),
        "wrong_items": wrong_items,
    }


# ---------------------------------------------------------------------------
# Renderers
# ---------------------------------------------------------------------------

def _render_idle() -> None:
    st.markdown(
        "Two held-out 100-question pools were stratified-sampled from the 841-question bank "
        "in Phase 2 with `random.seed(42)`. They're excluded from Quiz Mode by default so "
        "they retain calibration value here."
    )

    cols = st.columns(2)
    with cols[0]:
        with st.container(border=True):
            st.subheader("📝 Mock #1")
            st.caption("Scheduled: **Week 11 Sat** · Pass ≥ **70%**")
            st.markdown(
                "- 50 questions sampled from `mock1-pool`\n"
                "- 2-hour countdown timer\n"
                "- No explanations until you submit\n"
                "- Pool stays held out — does not write to your progress"
            )
            if st.button("▶️ Start Mock #1", type="primary", use_container_width=True, key="start_mock_1"):
                _start_mock(1)
                st.rerun()

    with cols[1]:
        with st.container(border=True):
            st.subheader("📝 Mock #2")
            st.caption("Scheduled: **Week 12 Wed** · Pass ≥ **80%** (deliberately above real-exam threshold)")
            st.markdown(
                "- 50 questions sampled from `mock2-pool` (disjoint from Mock #1)\n"
                "- 2-hour countdown timer\n"
                "- Take only after you've passed Mock #1\n"
                "- < 80% → consider pushing the real exam by a week"
            )
            if st.button("▶️ Start Mock #2", type="primary", use_container_width=True, key="start_mock_2"):
                _start_mock(2)
                st.rerun()

    st.divider()
    st.caption(
        "**House rules.** Real PMLE: 60 questions / 2 hours. We use 50 / 2 hours per the "
        "study plan — the spare 10 questions are buffer in the pool. No explanations during "
        "the exam (matches real-exam conditions). Use Quiz Mode for drill rounds with "
        "explanations after each question."
    )


def _render_running() -> None:
    questions = st.session_state.mock_questions
    pos = st.session_state.mock_pos
    n_total = len(questions)
    mock_num = st.session_state.mock_num

    remaining = _seconds_remaining()
    if remaining <= 0:
        st.error("⏰ Time's up — auto-submitting.")
        _submit_mock()
        st.rerun()
        return

    # Timer + progress strip
    pct_time_used = 1 - remaining / MOCK_DURATION_SECONDS
    cols = st.columns([2, 2, 1])
    cols[0].metric("⏱️ Time remaining", _format_clock(remaining))
    cols[1].metric("Question", f"{min(pos + 1, n_total)} / {n_total}")
    cols[2].metric("Mock", f"#{mock_num}")
    st.progress(pct_time_used)

    if pos >= n_total:
        st.success("All questions answered.")
        col1, col2 = st.columns(2)
        if col1.button("✅ Submit mock", type="primary", use_container_width=True):
            _submit_mock()
            st.rerun()
        if col2.button("⬅️ Back to last question", use_container_width=True):
            st.session_state.mock_pos = n_total - 1
            st.rerun()
        return

    q = questions[pos]
    st.divider()
    st.subheader(f"Question {pos + 1}")
    st.markdown(q.question, unsafe_allow_html=True)

    chosen = st.session_state.mock_responses.get(pos)
    choice_key = f"mock_choice_{pos}"

    if q.mode == "single_choice":
        # Find existing index if already answered
        default_idx = None
        if chosen is not None:
            existing = next(iter(chosen)) if isinstance(chosen, set) else chosen
            default_idx = existing
        selection = st.radio(
            "Choose an answer:",
            options=list(range(len(q.options))),
            format_func=lambda i: q.options[i],
            index=default_idx,
            key=choice_key,
        )
        new_response = selection if selection is not None else None
    else:
        existing = chosen if isinstance(chosen, set) else set()
        cb_values = []
        for i, opt in enumerate(q.options):
            cb_values.append(
                st.checkbox(opt, value=(i in existing), key=f"{choice_key}_{i}")
            )
        new_response = {i for i, v in enumerate(cb_values) if v}
        if not new_response:
            new_response = None

    # Buttons
    nav = st.columns([1, 1, 1, 1])
    if nav[0].button("⬅️ Previous", disabled=(pos == 0), key=f"prev_{pos}"):
        if new_response is not None:
            st.session_state.mock_responses[pos] = new_response
        st.session_state.mock_pos = max(0, pos - 1)
        st.rerun()

    if nav[1].button("⏭️ Skip", key=f"skip_{pos}"):
        st.session_state.mock_pos = pos + 1
        st.rerun()

    next_label = "✅ Save & Next" if pos < n_total - 1 else "✅ Save & Review"
    if nav[2].button(next_label, type="primary", key=f"next_{pos}"):
        if new_response is not None:
            st.session_state.mock_responses[pos] = new_response
        st.session_state.mock_pos = pos + 1
        st.rerun()

    if nav[3].button("🏁 End early", key=f"end_{pos}"):
        if new_response is not None:
            st.session_state.mock_responses[pos] = new_response
        _submit_mock()
        st.rerun()

    # Quick jump
    st.divider()
    answered_positions = sorted(st.session_state.mock_responses.keys())
    st.caption(
        f"Answered so far: **{len(answered_positions)} / {n_total}** · "
        f"Skipped/unanswered: **{n_total - len(answered_positions)}**"
    )

    with st.expander("🧭 Jump to a specific question"):
        target = st.number_input(
            "Question number",
            min_value=1,
            max_value=n_total,
            value=pos + 1,
            step=1,
            key=f"jump_{pos}",
        )
        if st.button("Go", key=f"go_{pos}"):
            if new_response is not None:
                st.session_state.mock_responses[pos] = new_response
            st.session_state.mock_pos = int(target) - 1
            st.rerun()


def _render_submitted() -> None:
    questions = st.session_state.mock_questions
    responses = st.session_state.mock_responses
    mock_num = st.session_state.mock_num

    started = st.session_state.mock_started_at
    finished = st.session_state.mock_finished_at or time.time()
    elapsed = int(finished - started) if started else 0

    result = _score(questions, responses)
    threshold = PASS_THRESHOLD[mock_num]
    pct = result["pct"]

    # ---- Hero metrics ----
    if pct >= threshold:
        st.success(f"🎉 PASS — {result['correct']} / {result['total']} ({pct:.1%})")
    else:
        st.error(f"❌ Below threshold — {result['correct']} / {result['total']} ({pct:.1%})")

    cols = st.columns(4)
    cols[0].metric("Score", f"{pct:.1%}")
    cols[1].metric("Correct", f"{result['correct']}/{result['total']}")
    cols[2].metric("Pass threshold", f"{threshold:.0%}")
    cols[3].metric("Time elapsed", _format_clock(elapsed))

    if pct < threshold:
        gap = threshold - pct
        n_more = int(round(gap * result["total"])) + 1
        st.warning(
            f"You needed **{n_more}** more correct to clear the threshold. "
            f"Drill the wrong-answer list below in Quiz Mode, then retake.",
            icon="🔁",
        )

    # ---- Per-section breakdown ----
    st.divider()
    st.subheader("📊 Per-section breakdown")
    rows = []
    for sec, total in sorted(result["by_section_total"].items()):
        correct = result["by_section_correct"].get(sec, 0)
        sec_pct = correct / total if total else 0.0
        rows.append({
            "Section": sec,
            "Correct": correct,
            "Total": total,
            "Accuracy": f"{sec_pct:.0%}",
            "Status": "🟢" if sec_pct >= threshold else ("🟡" if sec_pct >= 0.5 else "🔴"),
        })
    st.dataframe(rows, hide_index=True, use_container_width=True)

    weakest = sorted(
        result["by_section_total"].items(),
        key=lambda kv: result["by_section_correct"].get(kv[0], 0) / max(1, kv[1]),
    )[:3]
    if weakest:
        st.markdown(
            "**Weakest 3 sections:** "
            + ", ".join(f"`{s}` ({result['by_section_correct'].get(s,0)}/{t})" for s, t in weakest)
            + ". Use these as your wrong-answer-drill targets in Weekly Overview / Quiz Mode."
        )

        # Phase 5 cross-link: suggest incomplete labs covering the weak sections
        weak_sections = {s for s, _ in weakest}
        all_labs = load_labs()
        lab_prog = load_lab_progress()
        suggested = []
        for lab in all_labs:
            prog = lab_prog.get(lab.id) or LabProgress()
            if prog.status == "completed":
                continue
            if any(s in weak_sections for s in lab.exam_sections):
                suggested.append(lab)
        if suggested:
            st.info(
                "💡 **Suggested labs for your weak sections** (incomplete + covering ≥1 weak §): "
                + ", ".join(f"#{l.id} {l.name}" for l in suggested[:5])
                + ". Open the Labs page to track them.",
                icon="🧪",
            )

    # ---- Wrong answers ----
    st.divider()
    st.subheader(f"🔎 Wrong / unanswered questions ({len(result['wrong_items'])})")
    if not result["wrong_items"]:
        st.success("Nothing wrong — clean sweep.")
    else:
        for pos, q, chosen in result["wrong_items"]:
            with st.expander(
                f"Q{pos + 1} · #{q.id} · {q.exam_section or '(uncategorized)'}",
                expanded=False,
            ):
                st.markdown(q.question, unsafe_allow_html=True)

                # Your answer
                if chosen is None:
                    st.markdown("**Your answer:** _(unanswered)_")
                elif isinstance(chosen, set):
                    your_text = ", ".join(q.options[i] for i in sorted(chosen))
                    st.markdown(f"**Your answer:** {your_text}")
                else:
                    st.markdown(f"**Your answer:** {q.options[chosen]}")

                # Correct answer
                if isinstance(q.answer, list):
                    correct_text = "\n".join(f"- {q.options[i]}" for i in q.answer)
                    st.markdown(f"**Correct answer(s):**\n{correct_text}")
                else:
                    st.markdown(f"**Correct answer:** {q.options[q.answer]}")

                if q.explanation:
                    st.markdown("**Explanation:**")
                    st.markdown(q.explanation, unsafe_allow_html=True)

    # ---- Reset ----
    st.divider()
    if st.button("🔄 Take another mock", type="primary"):
        _reset_state()
        st.rerun()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    st.set_page_config(page_title="Mock Exam", page_icon="⏱️", layout="wide")
    set_css_style(Path("style.css"))
    _init_state()

    st.title("⏱️ Mock Exam")

    phase = st.session_state.mock_phase
    if phase == "idle":
        st.caption("Pick a mock — you'll get a 2-hour timer and 50 questions. No explanations until you submit.")
        _render_idle()
    elif phase == "running":
        _render_running()
    elif phase == "submitted":
        _render_submitted()
    else:
        _reset_state()
        st.rerun()


if __name__ == "__main__":
    main()
