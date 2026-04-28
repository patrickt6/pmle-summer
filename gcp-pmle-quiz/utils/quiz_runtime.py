"""Shared timed-quiz runtime: scoring + render helpers.

Used by `pages/9_⏱️_Mock_Exam.py` and `pages/10_📋_Week_Quizzes.py`. The two
pages are functionally identical — countdown timer, no in-quiz explanations,
score + per-section breakdown at submit — but differ in question pool and
duration. Parameterizing on `state_prefix` keeps their session_state keys
namespaced so two timed quizzes never collide.

State keys, given prefix `P`:
  P_phase            "idle" | "running" | "submitted"
  P_questions        list[Question]
  P_pos              int — current question index
  P_responses        dict[int, set[int] | int]   pos -> answer
  P_started_at       float — wall-clock seconds at start
  P_finished_at      float | None
  P_duration_s       int — total countdown
  P_meta             dict — quiz-specific extras (e.g. mock_num, attempt_id)
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable

import streamlit as st

from models.questions import Question


@dataclass
class ScoreResult:
    correct: int
    total: int
    pct: float
    by_section_total: dict[str, int] = field(default_factory=dict)
    by_section_correct: dict[str, int] = field(default_factory=dict)
    wrong_items: list[tuple[int, Question, set[int] | int | None]] = field(default_factory=list)


def score(questions: list[Question], responses: dict[int, set[int] | int | None]) -> ScoreResult:
    """Compute score, per-section breakdown, and wrong-answer list.

    `responses` maps question position (0-indexed) to either a set of indices
    (multi-choice) or a single index (single-choice). Missing keys = unanswered.
    """
    correct = 0
    by_section_total: dict[str, int] = {}
    by_section_correct: dict[str, int] = {}
    wrong_items: list[tuple[int, Question, set[int] | int | None]] = []

    for pos, q in enumerate(questions):
        section = q.exam_section or "(uncategorized)"
        by_section_total[section] = by_section_total.get(section, 0) + 1
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
            by_section_correct[section] = by_section_correct.get(section, 0) + 1
        else:
            wrong_items.append((pos, q, chosen))

    total = len(questions)
    pct = correct / total if total else 0.0
    return ScoreResult(
        correct=correct,
        total=total,
        pct=pct,
        by_section_total=by_section_total,
        by_section_correct=by_section_correct,
        wrong_items=wrong_items,
    )


def format_clock(seconds: int) -> str:
    if seconds < 0:
        seconds = 0
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def seconds_remaining(state_prefix: str) -> int:
    started = st.session_state.get(f"{state_prefix}started_at")
    duration = st.session_state.get(f"{state_prefix}duration_s", 0)
    if started is None or duration <= 0:
        return duration
    elapsed = int(time.time() - started)
    return max(0, duration - elapsed)


def init_state(state_prefix: str) -> None:
    st.session_state.setdefault(f"{state_prefix}phase", "idle")
    st.session_state.setdefault(f"{state_prefix}questions", [])
    st.session_state.setdefault(f"{state_prefix}pos", 0)
    st.session_state.setdefault(f"{state_prefix}responses", {})
    st.session_state.setdefault(f"{state_prefix}started_at", None)
    st.session_state.setdefault(f"{state_prefix}finished_at", None)
    st.session_state.setdefault(f"{state_prefix}duration_s", 0)
    st.session_state.setdefault(f"{state_prefix}meta", {})


def reset_state(state_prefix: str) -> None:
    for suffix in (
        "phase",
        "questions",
        "pos",
        "responses",
        "started_at",
        "finished_at",
        "duration_s",
        "meta",
    ):
        key = f"{state_prefix}{suffix}"
        if key in st.session_state:
            del st.session_state[key]
    init_state(state_prefix)


def start(
    state_prefix: str,
    questions: list[Question],
    duration_s: int,
    meta: dict | None = None,
) -> None:
    """Transition to running with the given questions + duration."""
    st.session_state[f"{state_prefix}phase"] = "running"
    st.session_state[f"{state_prefix}questions"] = questions
    st.session_state[f"{state_prefix}pos"] = 0
    st.session_state[f"{state_prefix}responses"] = {}
    st.session_state[f"{state_prefix}started_at"] = time.time()
    st.session_state[f"{state_prefix}finished_at"] = None
    st.session_state[f"{state_prefix}duration_s"] = duration_s
    st.session_state[f"{state_prefix}meta"] = dict(meta or {})


def submit(state_prefix: str) -> None:
    st.session_state[f"{state_prefix}phase"] = "submitted"
    st.session_state[f"{state_prefix}finished_at"] = time.time()


def render_running(state_prefix: str, *, header_label: str = "") -> None:
    """Render the in-progress timed-quiz UI. Auto-submits when timer hits zero."""
    questions: list[Question] = st.session_state.get(f"{state_prefix}questions", [])
    if not questions:
        st.warning("No questions loaded.")
        return

    pos = st.session_state.get(f"{state_prefix}pos", 0)
    n_total = len(questions)
    duration_s = st.session_state.get(f"{state_prefix}duration_s", 0)
    remaining = seconds_remaining(state_prefix)

    if remaining <= 0:
        st.error("⏰ Time's up — auto-submitting.")
        submit(state_prefix)
        st.rerun()
        return

    pct_used = 1 - remaining / duration_s if duration_s else 0
    cols = st.columns([2, 2, 1])
    cols[0].metric("⏱️ Time remaining", format_clock(remaining))
    cols[1].metric("Question", f"{min(pos + 1, n_total)} / {n_total}")
    cols[2].metric("Progress", f"{int(pct_used * 100)}%")
    st.progress(pct_used)
    if header_label:
        st.caption(header_label)

    if pos >= n_total:
        st.success("All questions answered. Review or submit.")
        col1, col2 = st.columns(2)
        if col1.button("✅ Submit", type="primary", use_container_width=True, key=f"{state_prefix}submit_btn"):
            submit(state_prefix)
            st.rerun()
        if col2.button("⬅️ Back to last question", use_container_width=True, key=f"{state_prefix}back_btn"):
            st.session_state[f"{state_prefix}pos"] = n_total - 1
            st.rerun()
        return

    q = questions[pos]
    st.divider()
    st.subheader(f"Question {pos + 1}")
    st.markdown(q.question, unsafe_allow_html=True)

    chosen = st.session_state[f"{state_prefix}responses"].get(pos)
    choice_key = f"{state_prefix}choice_{pos}"

    if q.mode == "single_choice":
        default_idx = None
        if chosen is not None:
            default_idx = next(iter(chosen)) if isinstance(chosen, set) else chosen
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
            cb_values.append(st.checkbox(opt, value=(i in existing), key=f"{choice_key}_{i}"))
        new_response = {i for i, v in enumerate(cb_values) if v}
        if not new_response:
            new_response = None

    nav = st.columns([1, 1, 1, 1])
    if nav[0].button("⬅️ Previous", disabled=(pos == 0), key=f"{state_prefix}prev_{pos}"):
        if new_response is not None:
            st.session_state[f"{state_prefix}responses"][pos] = new_response
        st.session_state[f"{state_prefix}pos"] = max(0, pos - 1)
        st.rerun()

    if nav[1].button("⏭️ Skip", key=f"{state_prefix}skip_{pos}"):
        st.session_state[f"{state_prefix}pos"] = pos + 1
        st.rerun()

    next_label = "✅ Save & Next" if pos < n_total - 1 else "✅ Save & Review"
    if nav[2].button(next_label, type="primary", key=f"{state_prefix}next_{pos}"):
        if new_response is not None:
            st.session_state[f"{state_prefix}responses"][pos] = new_response
        st.session_state[f"{state_prefix}pos"] = pos + 1
        st.rerun()

    if nav[3].button("🏁 End early", key=f"{state_prefix}end_{pos}"):
        if new_response is not None:
            st.session_state[f"{state_prefix}responses"][pos] = new_response
        submit(state_prefix)
        st.rerun()

    st.divider()
    answered = sorted(st.session_state[f"{state_prefix}responses"].keys())
    st.caption(
        f"Answered so far: **{len(answered)} / {n_total}** · "
        f"Skipped/unanswered: **{n_total - len(answered)}**"
    )

    with st.expander("🧭 Jump to a specific question"):
        target = st.number_input(
            "Question number",
            min_value=1,
            max_value=n_total,
            value=pos + 1,
            step=1,
            key=f"{state_prefix}jump_{pos}",
        )
        if st.button("Go", key=f"{state_prefix}go_{pos}"):
            if new_response is not None:
                st.session_state[f"{state_prefix}responses"][pos] = new_response
            st.session_state[f"{state_prefix}pos"] = int(target) - 1
            st.rerun()


def render_submitted(
    state_prefix: str,
    threshold: float,
    *,
    on_finalize: Callable[[ScoreResult, dict], None] | None = None,
    reset_label: str = "🔄 Take another",
) -> ScoreResult:
    """Render the submitted score view.

    `on_finalize(score_result, meta)` is invoked once after submit so the
    caller can persist the attempt. Tracked via a flag in session_state to
    avoid duplicate writes on rerun.
    """
    questions: list[Question] = st.session_state.get(f"{state_prefix}questions", [])
    responses: dict = st.session_state.get(f"{state_prefix}responses", {})
    started = st.session_state.get(f"{state_prefix}started_at")
    finished = st.session_state.get(f"{state_prefix}finished_at") or time.time()
    elapsed = int(finished - started) if started else 0

    result = score(questions, responses)
    meta = st.session_state.get(f"{state_prefix}meta", {})

    finalize_flag = f"{state_prefix}finalized"
    if on_finalize is not None and not st.session_state.get(finalize_flag):
        try:
            on_finalize(result, meta)
        finally:
            st.session_state[finalize_flag] = True

    if result.pct >= threshold:
        st.success(f"🎉 PASS — {result.correct} / {result.total} ({result.pct:.1%})")
    else:
        st.error(f"❌ Below threshold — {result.correct} / {result.total} ({result.pct:.1%})")

    cols = st.columns(4)
    cols[0].metric("Score", f"{result.pct:.1%}")
    cols[1].metric("Correct", f"{result.correct}/{result.total}")
    cols[2].metric("Pass threshold", f"{threshold:.0%}")
    cols[3].metric("Time elapsed", format_clock(elapsed))

    if result.pct < threshold:
        gap = threshold - result.pct
        n_more = int(round(gap * result.total)) + 1
        st.warning(
            f"You needed **{n_more}** more correct to clear the threshold. "
            f"Drill the wrong-answer list below in Quiz Mode, then retake.",
            icon="🔁",
        )

    st.divider()
    st.subheader("📊 Per-section breakdown")
    rows = []
    for sec, total in sorted(result.by_section_total.items()):
        sec_correct = result.by_section_correct.get(sec, 0)
        sec_pct = sec_correct / total if total else 0.0
        rows.append({
            "Section": sec,
            "Correct": sec_correct,
            "Total": total,
            "Accuracy": f"{sec_pct:.0%}",
            "Status": "🟢" if sec_pct >= threshold else ("🟡" if sec_pct >= 0.5 else "🔴"),
        })
    if rows:
        st.dataframe(rows, hide_index=True, use_container_width=True)

    weakest = sorted(
        result.by_section_total.items(),
        key=lambda kv: result.by_section_correct.get(kv[0], 0) / max(1, kv[1]),
    )[:3]
    if weakest:
        st.markdown(
            "**Weakest 3 sections:** "
            + ", ".join(
                f"`{s}` ({result.by_section_correct.get(s, 0)}/{t})" for s, t in weakest
            )
            + ". Use these as wrong-answer-drill targets in Weekly Overview / Quiz Mode."
        )

    st.divider()
    st.subheader(f"🔎 Wrong / unanswered questions ({len(result.wrong_items)})")
    if not result.wrong_items:
        st.success("Nothing wrong — clean sweep.")
    else:
        for pos, q, chosen in result.wrong_items:
            with st.expander(
                f"Q{pos + 1} · #{q.id} · {q.exam_section or '(uncategorized)'}",
                expanded=False,
            ):
                st.markdown(q.question, unsafe_allow_html=True)
                if chosen is None:
                    st.markdown("**Your answer:** _(unanswered)_")
                elif isinstance(chosen, set):
                    your_text = ", ".join(q.options[i] for i in sorted(chosen))
                    st.markdown(f"**Your answer:** {your_text}")
                else:
                    st.markdown(f"**Your answer:** {q.options[chosen]}")
                if isinstance(q.answer, list):
                    correct_text = "\n".join(f"- {q.options[i]}" for i in q.answer)
                    st.markdown(f"**Correct answer(s):**\n{correct_text}")
                else:
                    st.markdown(f"**Correct answer:** {q.options[q.answer]}")
                if q.explanation:
                    st.markdown("**Explanation:**")
                    st.markdown(q.explanation, unsafe_allow_html=True)

    st.divider()
    if st.button(reset_label, type="primary", key=f"{state_prefix}reset_btn"):
        reset_state(state_prefix)
        st.rerun()

    return result
