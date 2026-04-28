"""Phase 4 — Per-week mock-style timed quizzes.

Three deterministic attempts per week (A/B/C) plus a Remix button for endless
fresh attempts. Same scoring + countdown UI as Mock Exam, but scoped to the
current week's exam sections via `sample_quiz_for_week`. Results write to
`data/week_quiz_results.json` (NOT `progress.json` — week quiz attempts stay
distinct from Quiz Mode round tracking).

Mock-pool questions are excluded by default so Mock #1 / #2 calibration stays
intact in Weeks 11–12.
"""

from __future__ import annotations

import time
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

from utils import set_css_style
from utils.quiz_runtime import (
    init_state,
    render_running,
    render_submitted,
    reset_state,
    start,
)
from utils.week_results import (
    WeekQuizResult,
    append_week_quiz_result,
    attempts_for_week,
)
from utils.weekly import (
    Week,
    current_week_number,
    load_weeks,
    quizzes_for_week,
    sample_quiz_for_week,
)

STATE_PREFIX = "weekquiz_"

PRESET_LETTERS = ["A", "B", "C"]
DEFAULT_PARAMS = {"n_questions": 20, "duration_s": 30 * 60, "threshold": 0.70}
MOCK_WEEK_PARAMS = {"n_questions": 30, "duration_s": 45 * 60, "threshold": 0.75}
MOCK_WEEKS = {11, 12}


def _params_for_week(week: Week) -> dict:
    return MOCK_WEEK_PARAMS if week.week in MOCK_WEEKS else DEFAULT_PARAMS


def _seed_for_attempt(week_num: int, letter: str) -> int:
    idx = PRESET_LETTERS.index(letter) + 1
    return week_num * 1000 + idx


def _is_remix(attempt_id: str) -> bool:
    return attempt_id.startswith("remix-")


def _attempt_label(attempt_id: str) -> str:
    if _is_remix(attempt_id):
        return f"🔀 Remix · {attempt_id.split('-')[-1]}"
    return f"Quiz {attempt_id}"


def _persist_result(score_result, meta: dict) -> None:
    """Callback fired exactly once after submit; writes the result to disk."""
    week_num = meta.get("week")
    if week_num is None:
        return
    started = st.session_state.get(f"{STATE_PREFIX}started_at")
    finished = st.session_state.get(f"{STATE_PREFIX}finished_at") or time.time()
    duration_s = int(finished - started) if started else 0
    started_iso = (
        datetime.fromtimestamp(started, tz=timezone.utc).isoformat() if started else ""
    )
    finished_iso = datetime.fromtimestamp(finished, tz=timezone.utc).isoformat()
    by_section: dict[str, list[int]] = {}
    for sec, total in score_result.by_section_total.items():
        by_section[sec] = [score_result.by_section_correct.get(sec, 0), total]
    result = WeekQuizResult(
        week=int(week_num),
        attempt_id=meta.get("attempt_id", "unknown"),
        seed=int(meta.get("seed", 0)),
        started_at=started_iso,
        finished_at=finished_iso,
        duration_s=duration_s,
        n_questions=score_result.total,
        n_correct=score_result.correct,
        pct=round(score_result.pct, 4),
        passed=score_result.pct >= float(meta.get("threshold", 0.70)),
        by_section=by_section,
        wrong_question_ids=[q.id for _, q, _ in score_result.wrong_items],
    )
    append_week_quiz_result(result)


def _start_attempt(week: Week, attempt_id: str, seed: int, params: dict) -> None:
    questions = sample_quiz_for_week(
        week,
        n_questions=params["n_questions"],
        seed=seed,
        exclude_mock=True,
    )
    if not questions:
        st.error("No questions available for this week. Check Phase 2 tagging.")
        return
    start(
        STATE_PREFIX,
        questions=questions,
        duration_s=params["duration_s"],
        meta={
            "week": week.week,
            "attempt_id": attempt_id,
            "seed": seed,
            "threshold": params["threshold"],
            "n_questions": params["n_questions"],
        },
    )
    if f"{STATE_PREFIX}finalized" in st.session_state:
        del st.session_state[f"{STATE_PREFIX}finalized"]


def _render_attempt_card(week: Week, letter: str, params: dict) -> None:
    seed = _seed_for_attempt(week.week, letter)
    attempt_id = f"{week.week}{letter}"
    prior = attempts_for_week(week.week)
    matching = [r for r in prior if r.attempt_id == attempt_id]
    matching.sort(key=lambda r: r.finished_at, reverse=True)
    latest = matching[0] if matching else None

    with st.container(border=True):
        st.markdown(f"**Quiz {attempt_id}**")
        st.caption(
            f"{params['n_questions']} Qs · {params['duration_s'] // 60} min · "
            f"Pass ≥ {params['threshold']:.0%}"
        )
        if latest is None:
            st.markdown("Status: 🟢 not yet attempted")
        elif latest.passed:
            st.markdown(f"Status: 🔵 best {latest.pct:.0%} (passed)")
        else:
            st.markdown(f"Status: 🟡 last {latest.pct:.0%}")

        if st.button("▶️ Start", key=f"start_{attempt_id}", use_container_width=True):
            _start_attempt(week, attempt_id, seed, params)
            st.rerun()


def _render_idle(week: Week) -> None:
    params = _params_for_week(week)
    n_in_scope = len(quizzes_for_week(week))

    st.subheader(f"Week {week.week} — {week.title}")
    cap_parts = [
        f"{week.primary_section} focus",
        f"{n_in_scope} Qs in scope",
        f"{week.hours_target:g}h target",
    ]
    if week.milestone:
        cap_parts.append(f"🏁 {week.milestone}")
    st.caption(" · ".join(cap_parts))

    if n_in_scope < 60:
        st.warning(
            f"Limited question pool — only {n_in_scope} non-mock questions in scope. "
            "Quiz attempts may overlap.",
            icon="⚠️",
        )

    if week.week in MOCK_WEEKS:
        st.info(
            "Mock weeks use a longer **30 Q / 45 min / ≥ 75 %** quiz format — closer to "
            "real-exam pacing. The held-out 50-question Mock pools live on the **Mock Exam** "
            "page (`pages/9_⏱️_Mock_Exam.py`).",
            icon="ℹ️",
        )

    st.divider()

    cols = st.columns(3)
    for letter, col in zip(PRESET_LETTERS, cols):
        with col:
            _render_attempt_card(week, letter, params)

    # Remix
    st.divider()
    rcol1, rcol2 = st.columns([3, 1])
    rcol1.markdown(
        "**🔀 Remix** — new seed each click. Use after exhausting A/B/C if you want endless "
        "fresh practice on this week's content."
    )
    if rcol2.button("🔀 Remix", type="primary", use_container_width=True):
        seed = int(time.time())
        attempt_id = f"remix-{seed}"
        _start_attempt(week, attempt_id, seed, params)
        st.rerun()

    # History
    st.divider()
    st.subheader("📜 History")
    history = sorted(attempts_for_week(week.week), key=lambda r: r.finished_at, reverse=True)
    if not history:
        st.caption("No attempts yet for this week.")
        return
    rows = []
    for r in history:
        rows.append({
            "When": r.finished_at[:16].replace("T", " "),
            "Attempt": _attempt_label(r.attempt_id),
            "Score": f"{r.pct:.0%}",
            "Correct": f"{r.n_correct}/{r.n_questions}",
            "Status": "✅ pass" if r.passed else "❌ retry",
            "Time": f"{r.duration_s // 60}m {r.duration_s % 60}s",
        })
    st.dataframe(rows, hide_index=True, use_container_width=True)


def _resume_or_start_caption(week_num_in_state: int | None, selected_week_num: int) -> None:
    if (
        st.session_state.get(f"{STATE_PREFIX}phase") == "running"
        and week_num_in_state is not None
        and week_num_in_state != selected_week_num
    ):
        st.warning(
            f"⚠️ A quiz is in progress for **Week {week_num_in_state}** "
            f"(`{st.session_state[f'{STATE_PREFIX}meta'].get('attempt_id')}`). "
            "Switching weeks while running will lose progress on submit.",
            icon="🔁",
        )
        if st.button("🛑 Discard in-progress quiz"):
            reset_state(STATE_PREFIX)
            st.rerun()


def main() -> None:
    st.set_page_config(page_title="Week Quizzes", page_icon="📋", layout="wide")
    set_css_style(Path("style.css"))
    init_state(STATE_PREFIX)

    st.title("📋 Per-week timed quizzes")

    weeks = load_weeks()
    if not weeks:
        st.error("`data/weeks.json` is missing or empty. Run Phase 3 Move 1 first.")
        return

    if "weekquiz_selected_week" not in st.session_state:
        st.session_state.weekquiz_selected_week = current_week_number()

    week_options = [w.week for w in weeks]
    week_labels = {w.week: f"Week {w.week} — {w.title}" for w in weeks}
    try:
        default_idx = week_options.index(st.session_state.weekquiz_selected_week)
    except ValueError:
        default_idx = 0

    selected = st.selectbox(
        "Pick a study week",
        options=week_options,
        index=default_idx,
        format_func=lambda x: week_labels[x],
        key="weekquiz_selected_week",
    )
    week = next(w for w in weeks if w.week == selected)

    in_progress_week = st.session_state.get(f"{STATE_PREFIX}meta", {}).get("week")
    _resume_or_start_caption(in_progress_week, week.week)

    phase = st.session_state.get(f"{STATE_PREFIX}phase", "idle")

    if phase == "running":
        meta = st.session_state.get(f"{STATE_PREFIX}meta", {})
        header_label = (
            f"Week {meta.get('week')} · {_attempt_label(meta.get('attempt_id', '?'))} · "
            f"seed {meta.get('seed')}"
        )
        render_running(STATE_PREFIX, header_label=header_label)
    elif phase == "submitted":
        meta = st.session_state.get(f"{STATE_PREFIX}meta", {})
        threshold = float(meta.get("threshold", 0.70))
        st.subheader(
            f"Week {meta.get('week')} · {_attempt_label(meta.get('attempt_id', '?'))} — results"
        )
        render_submitted(
            STATE_PREFIX,
            threshold=threshold,
            on_finalize=_persist_result,
            reset_label="🔄 Back to week selector",
        )
    else:
        _render_idle(week)


if __name__ == "__main__":
    main()
