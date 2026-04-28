"""Phase 5 Move 3 — Labs Integration.

Promotes the 20 Skills Boost items from link-out URLs to first-class study
artifacts. Tracks status (not started / in_progress / completed / skipped),
shared notes (paste-driven, both partners), "ohhh" insights (append-only),
and post-lab drill quizzes (15 Qs sampled from this lab's exam_sections,
graded via the shared utils.quiz_runtime).
"""

from __future__ import annotations

import time
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

from utils import set_css_style
from utils.labs import (
    Lab,
    LabProgress,
    PostLabQuizAttempt,
    lab_completion_summary,
    load_lab_progress,
    load_labs,
    now_iso,
    post_lab_quiz_questions,
    update_lab,
)
from utils.quiz_runtime import (
    init_state,
    render_running,
    render_submitted,
    reset_state,
    start,
)

STATE_PREFIX = "labquiz_"

POST_LAB_QUIZ_DEFAULT_DURATION_S = 20 * 60  # 20 min for a 15-Q drill
POST_LAB_QUIZ_THRESHOLD = 0.70
POST_LAB_QUIZ_SIZE = 15

RATING_ORDER = {"must": 0, "should": 1, "skip": 2}
STATUS_BADGES = {
    "not_started": "🟢 not started",
    "in_progress": "🟡 in progress",
    "completed": "🔵 completed",
    "skipped": "⚪ skipped",
}

SAT_TEMPLATE = """### Saturday paired session — Lab #{id} {name}

**Pre-lab (5 min)**
- [ ] Patrick reads the lab description aloud
- [ ] Matty Boy opens a fresh GCP console window
- [ ] Both agree on the success criterion

**During lab (90 min, switch every 30 min)**
- [ ] 0:00–0:30 — Patrick types, Matty Boy reads steps
- [ ] 0:30–0:60 — switch
- [ ] 0:60–0:90 — switch
- [ ] If blocked > 5 min, post in shared chat, move on

**Post-lab (10 min)**
- [ ] Each names ONE "ohhh" insight (paste in 💡 field above)
- [ ] Run the post-lab drill (15 Qs)
- [ ] Mark this lab ✅ in the app
"""


def _persist_post_lab_attempt(score_result, meta: dict) -> None:
    lab_id = int(meta.get("lab_id", 0))
    if not lab_id:
        return
    progress = load_lab_progress()
    current = progress.get(lab_id) or LabProgress()
    new_attempt = PostLabQuizAttempt(
        timestamp=now_iso(),
        n_questions=score_result.total,
        n_correct=score_result.correct,
        score=round(score_result.pct, 4),
        wrong_ids=[q.id for _, q, _ in score_result.wrong_items],
    )
    current.post_lab_quiz_attempts.append(new_attempt)
    progress[lab_id] = current
    from utils.labs import save_lab_progress

    save_lab_progress(progress)


def _start_post_lab_quiz(lab: Lab) -> None:
    seed = int(time.time())
    questions = post_lab_quiz_questions(lab, n=POST_LAB_QUIZ_SIZE, seed=seed)
    if not questions:
        st.error("No questions in this lab's sections — cannot start drill.")
        return
    start(
        STATE_PREFIX,
        questions=questions,
        duration_s=POST_LAB_QUIZ_DEFAULT_DURATION_S,
        meta={
            "lab_id": lab.id,
            "lab_name": lab.name,
            "seed": seed,
            "threshold": POST_LAB_QUIZ_THRESHOLD,
        },
    )
    if f"{STATE_PREFIX}finalized" in st.session_state:
        del st.session_state[f"{STATE_PREFIX}finalized"]


def _render_lab_card(lab: Lab, prog: LabProgress) -> None:
    title = f"#{lab.id} · {lab.name}"
    badge = STATUS_BADGES.get(prog.status, prog.status)
    rating_emoji = {"must": "🏆", "should": "🟡", "skip": "⏭"}.get(lab.rating, "")
    weeks_str = ", ".join(f"W{w}" for w in lab.weeks) if lab.weeks else "any week"

    with st.expander(f"{rating_emoji} {title} · {badge}", expanded=False):
        # ---- Header strip ----
        cols = st.columns([2, 1, 1, 1])
        cols[0].markdown(
            f"**[{lab.name}]({lab.url})** · _{lab.platform}_"
            if lab.url
            else f"**{lab.name}** · _{lab.platform}_"
        )
        cols[1].metric("Hours", f"{lab.duration_hours:g}")
        cols[2].metric("Rating", lab.rating.title())
        cols[3].metric("Weeks", weeks_str)

        st.caption(
            f"§s: {', '.join(lab.exam_sections)} · "
            f"Console focus: {', '.join(lab.console_focus) if lab.console_focus else 'n/a'} · "
            f"Decay risk: {lab.decay_risk}"
        )
        if lab.exam_yield_note:
            st.caption(f"📝 {lab.exam_yield_note}")

        # ---- Status controls ----
        st.divider()
        st.markdown("**Status**")
        bcols = st.columns(4)
        if bcols[0].button("▶️ Mark started", key=f"start_{lab.id}", disabled=prog.status == "in_progress"):
            update_lab(
                lab.id,
                status="in_progress",
                started_at=prog.started_at or now_iso(),
            )
            st.rerun()
        if bcols[1].button("✅ Mark complete", key=f"complete_{lab.id}", disabled=prog.status == "completed"):
            update_lab(
                lab.id,
                status="completed",
                started_at=prog.started_at or now_iso(),
                completed_at=now_iso(),
            )
            st.rerun()
        if bcols[2].button("⏭ Skip", key=f"skip_{lab.id}", disabled=prog.status == "skipped"):
            update_lab(lab.id, status="skipped")
            st.rerun()
        if bcols[3].button("🔁 Reset", key=f"reset_{lab.id}"):
            update_lab(lab.id, status="not_started", started_at=None, completed_at=None)
            st.rerun()

        # ---- Shared notes ----
        st.divider()
        st.markdown("**📝 Shared notes** (markdown OK; both partners append with `Patrick:` / `Matty Boy:` prefixes)")
        new_notes = st.text_area(
            "Notes",
            value=prog.shared_notes,
            height=140,
            key=f"notes_{lab.id}",
            label_visibility="collapsed",
        )
        if new_notes != prog.shared_notes:
            if st.button("💾 Save notes", key=f"save_notes_{lab.id}"):
                update_lab(lab.id, shared_notes=new_notes)
                st.success("Saved.")
                st.rerun()

        # ---- Ohhh insights ----
        st.divider()
        st.markdown('**💡 "Ohhh" insights** (one bullet per insight, append-only)')
        if prog.ohhh_insights:
            for i, insight in enumerate(prog.ohhh_insights):
                st.markdown(f"- {insight}")
        else:
            st.caption("No insights yet — capture one after the Saturday lab session.")

        new_insight = st.text_input("Add insight", key=f"insight_{lab.id}", placeholder="One short bullet…")
        if st.button("➕ Append", key=f"add_insight_{lab.id}", disabled=not new_insight.strip()):
            update_lab(lab.id, ohhh_insights=[*prog.ohhh_insights, new_insight.strip()])
            st.rerun()

        # ---- Post-lab drill ----
        st.divider()
        st.markdown(
            f"**🎯 Post-lab drill** — {POST_LAB_QUIZ_SIZE} Qs from "
            f"`{', '.join(lab.exam_sections)}` (excludes mock pools, "
            f"≥ {POST_LAB_QUIZ_THRESHOLD:.0%} pass)"
        )
        if st.button("🎯 Start post-lab drill", key=f"drill_{lab.id}", type="primary"):
            _start_post_lab_quiz(lab)
            st.rerun()

        if prog.post_lab_quiz_attempts:
            rows = []
            for a in sorted(prog.post_lab_quiz_attempts, key=lambda x: x.timestamp, reverse=True):
                rows.append({
                    "When": a.timestamp[:16].replace("T", " "),
                    "Score": f"{a.score:.0%}",
                    "Correct": f"{a.n_correct}/{a.n_questions}",
                    "Status": "✅" if a.score >= POST_LAB_QUIZ_THRESHOLD else "❌",
                })
            st.markdown("**Past attempts**")
            st.dataframe(rows, hide_index=True, use_container_width=True)

        # ---- Saturday session template ----
        st.divider()
        with st.expander("📋 Saturday paired-session template", expanded=False):
            st.markdown(SAT_TEMPLATE.format(id=lab.id, name=lab.name))


def _render_idle() -> None:
    summary = lab_completion_summary()
    cols = st.columns(4)
    cols[0].metric(
        "Labs done (total)",
        f"{summary['completed_total']} / {summary['total_labs']}",
    )
    cols[1].metric(
        "Must-rated done",
        f"{summary['completed_must']} / {summary['must_labs']}",
    )
    cols[2].metric("In progress", summary["in_progress"])
    cols[3].metric(
        "Hours logged · must left",
        f"{summary['hours_logged']:g} · {summary['must_hours_remaining']:g}h",
    )

    labs = load_labs()
    progress = load_lab_progress()

    with st.sidebar:
        st.header("Filters")
        rating_filter = st.multiselect(
            "Rating",
            options=["must", "should", "skip"],
            default=["must", "should"],
        )
        status_filter = st.multiselect(
            "Status",
            options=["not_started", "in_progress", "completed", "skipped"],
            default=["not_started", "in_progress", "completed"],
        )
        sort_options = {
            "Skills Boost order": lambda l: l.id,
            "Week": lambda l: (min(l.weeks) if l.weeks else 99, l.id),
            "Rating (must first)": lambda l: (RATING_ORDER.get(l.rating, 9), l.id),
            "Status": lambda l: (
                {"in_progress": 0, "not_started": 1, "completed": 2, "skipped": 3}.get(
                    (progress.get(l.id) or LabProgress()).status, 9
                ),
                l.id,
            ),
        }
        sort_by = st.radio("Sort by", options=list(sort_options.keys()), index=0)

    filtered = [
        l for l in labs
        if l.rating in rating_filter
        and (progress.get(l.id) or LabProgress()).status in status_filter
    ]
    filtered.sort(key=sort_options[sort_by])

    if not filtered:
        st.info("No labs match these filters.")
        return

    for l in filtered:
        prog = progress.get(l.id) or LabProgress()
        _render_lab_card(l, prog)


def main() -> None:
    st.set_page_config(page_title="Labs", page_icon="🧪", layout="wide")
    set_css_style(Path("style.css"))
    init_state(STATE_PREFIX)

    st.title("🧪 Labs")
    st.caption(
        "20 Skills Boost items from `research/labs/skills-boost-path.md`, promoted to "
        "first-class study artifacts. Track status, share notes, capture insights, "
        "and run a 15-Q drill scoped to each lab's exam sections."
    )

    phase = st.session_state.get(f"{STATE_PREFIX}phase", "idle")

    if phase == "running":
        meta = st.session_state.get(f"{STATE_PREFIX}meta", {})
        st.subheader(f"🎯 Post-lab drill — Lab #{meta.get('lab_id')} · {meta.get('lab_name', '')}")
        render_running(STATE_PREFIX, header_label=f"Seed: {meta.get('seed')}")
    elif phase == "submitted":
        meta = st.session_state.get(f"{STATE_PREFIX}meta", {})
        st.subheader(
            f"🎯 Post-lab drill — Lab #{meta.get('lab_id')} results · {meta.get('lab_name', '')}"
        )
        render_submitted(
            STATE_PREFIX,
            threshold=POST_LAB_QUIZ_THRESHOLD,
            on_finalize=_persist_post_lab_attempt,
            reset_label="🔙 Back to labs list",
        )
    else:
        _render_idle()


if __name__ == "__main__":
    main()
