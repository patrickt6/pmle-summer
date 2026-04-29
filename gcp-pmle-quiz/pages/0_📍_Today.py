"""Phase 6a — 📍 Today: the daily wayfinding view.

Lives at the top of the sidebar (numeric prefix 0). Shows the active
profile's "what to do right now" — current week, today's tasks,
on-track delta, days-to-exam, week summary, jump-to-day override.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import streamlit as st

from utils import set_css_style
from utils.labs import lab_completion_summary
from utils.profile_ui import render_sidebar
from utils.profiles import current_profile
from utils.study_plan import load_study_plan
from utils.today import (
    DAY_LABELS,
    compute_today_context,
    day_id,
    mark_day_complete,
    mark_day_skipped,
    set_manual_override,
)

st.set_page_config(
    page_title="GCP PMLE — Today",
    page_icon="📍",
    initial_sidebar_state="expanded",
    layout="wide",
)


TASK_ICONS = {
    "read": "📖",
    "drill": "🤔",
    "lab": "🧪",
    "video": "📺",
    "app": "🎯",
    "external": "🔗",
    "other": "•",
}


def _delta_label(delta: int, is_pre_start: bool, is_post_plan: bool) -> str:
    if is_pre_start:
        return "Pre-start ⏸"
    if is_post_plan:
        return "Plan complete 🎉"
    if delta == 0:
        return "On track ✅"
    if delta > 0:
        return f"{delta} day{'s' if delta != 1 else ''} ahead 🚀"
    n = abs(delta)
    return f"{n} day{'s' if n != 1 else ''} behind ⚠"


def render_header(ctx, profile) -> None:
    today = date.today()
    today_str = today.strftime("%a %b %d, %Y").replace(" 0", " ")

    if ctx.is_pre_start:
        st.warning(
            f"📅 Plan starts on **{profile.study_start_date}**. Use this time to "
            "skim the [v3.1 exam guide PDF](https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english_3.1_final.pdf), "
            "or set a different start date in the sidebar."
        )
        return
    if ctx.is_post_plan:
        st.success("🎉 You've finished the 12-week plan. Take the real exam.")
        return

    week = ctx.target_week
    day = ctx.target_day
    week_label = (
        f"Week {week.num} — {week.theme}" if week else f"Week {ctx.expected_week_num}"
    )
    day_label = day.day_label if day else DAY_LABELS[ctx.expected_day_index]
    delta_text = _delta_label(ctx.delta_days, ctx.is_pre_start, ctx.is_post_plan)

    override_chip = (
        " · <span style='background:#fde68a;border-radius:6px;padding:2px 8px;font-size:0.85em;'>"
        "manual override</span>"
        if ctx.is_override
        else ""
    )

    exam_line = (
        f"<div style='font-size: 0.9em; color: #6b7280;'>{ctx.days_to_exam} days until the real exam</div>"
        if ctx.days_to_exam is not None
        else ""
    )

    st.markdown(
        f"""
        <div style="border-left: 5px solid {profile.color};
                    padding: 8px 18px; margin-bottom: 14px;
                    background: rgba(0,0,0,0.02); border-radius: 6px;">
          <div style="font-size: 1.6em; font-weight: 700;">📍 {today_str}</div>
          <div style="font-size: 1.05em; color: #374151;">
            {week_label} · <b>{day_label}</b> · {delta_text}{override_chip}
          </div>
          {exam_line}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_tasks(ctx) -> None:
    week = ctx.target_week
    day = ctx.target_day

    if ctx.is_pre_start or ctx.is_post_plan:
        return
    if week is None:
        st.error(
            "No structured plan loaded — run `python scripts/parse_study_plan.py` from the gcp-pmle-quiz dir."
        )
        return
    if day is None:
        st.info(
            f"No tasks scheduled for {DAY_LABELS[ctx.expected_day_index]} of Week {week.num}. "
            "(Likely a lighter day — review wrong answers, or read the week's anchors.)"
        )
        return

    head_cols = st.columns([6, 2])
    with head_cols[0]:
        st.subheader(f"🎯 {len(day.tasks)} task{'s' if len(day.tasks) != 1 else ''} today")
    with head_cols[1]:
        if day.estimated_min:
            st.caption(f"⏱ ~{day.estimated_min} min")

    for i, task in enumerate(day.tasks):
        with st.container(border=True):
            cols = st.columns([1, 8, 2])
            with cols[0]:
                st.markdown(
                    f"<div style='font-size: 2em; line-height: 1;'>{TASK_ICONS.get(task.type, '•')}</div>",
                    unsafe_allow_html=True,
                )
            with cols[1]:
                st.markdown(task.label)
                meta_bits: list[str] = [task.type]
                if task.estimated_min:
                    meta_bits.append(f"~{task.estimated_min} min")
                st.caption(" · ".join(meta_bits))
            with cols[2]:
                if task.ref and task.ref.startswith("http"):
                    st.link_button("Open ↗", task.ref, use_container_width=True)
                elif task.ref:
                    st.markdown(f"<code>{task.ref}</code>", unsafe_allow_html=True)

    st.divider()
    btn_cols = st.columns([2, 2, 6])
    with btn_cols[0]:
        if st.button("✅ Mark day complete", type="primary", use_container_width=True):
            mark_day_complete(week.num, day.day_index)
            st.toast("Day marked complete.")
            st.rerun()
    with btn_cols[1]:
        if st.button("⏭ Skip this day", use_container_width=True):
            mark_day_skipped(week.num, day.day_index)
            st.toast("Day marked skipped.")
            st.rerun()


def render_week_summary(ctx) -> None:
    week = ctx.target_week
    if week is None:
        return
    st.subheader(f"📊 Week {week.num} summary")
    cols = st.columns(4)
    with cols[0]:
        st.metric("Hours estimated", f"{week.estimated_hours or 0:.1f} h")
    with cols[1]:
        st.metric("Sections", ", ".join(week.exam_sections) if week.exam_sections else "—")
    with cols[2]:
        st.metric("Deliverables", len(week.deliverables))
    with cols[3]:
        target = (
            f"{int(week.sunday_quiz_target * 100)}%"
            if week.sunday_quiz_target
            else "—"
        )
        st.metric("Sunday target", target)

    if week.concept_anchors:
        with st.expander(f"🧠 Concept anchors ({len(week.concept_anchors)})"):
            for anchor in week.concept_anchors:
                st.markdown(f"- {anchor}")

    if week.deliverables:
        with st.expander(f"📦 Hard deliverables ({len(week.deliverables)})"):
            for d in week.deliverables:
                st.markdown(f"- {d.label}")


def render_jump() -> None:
    st.subheader("🧭 Jump to another day")
    plan = load_study_plan()
    if not plan.weeks:
        st.caption("No plan loaded.")
        return
    cols = st.columns([2, 2, 2, 6])
    with cols[0]:
        weeks = [w.num for w in plan.weeks]
        target_w = st.selectbox("Week", weeks, key="jump_week")
    with cols[1]:
        target_d = st.selectbox("Day", DAY_LABELS, key="jump_day")
    with cols[2]:
        if st.button("Jump", use_container_width=True):
            set_manual_override(day_id(target_w, DAY_LABELS.index(target_d)))
            st.rerun()
    with cols[3]:
        if st.button("Clear override", use_container_width=True):
            set_manual_override(None)
            st.rerun()


def render_lab_banner() -> None:
    try:
        summary = lab_completion_summary()
    except Exception:
        return
    st.caption(
        f"🧪 Labs done: **{summary['completed_must']} / {summary['must_labs']} must-rated** · "
        f"{summary['completed_total']} / {summary['total_labs']} total · "
        f"{summary['hours_logged']:g}h logged"
    )


def main() -> None:
    set_css_style(Path("style.css"))
    render_sidebar()

    profile = current_profile()
    ctx = compute_today_context()

    render_header(ctx, profile)
    render_tasks(ctx)
    render_week_summary(ctx)
    st.divider()
    render_jump()
    st.divider()
    render_lab_banner()


if __name__ == "__main__":
    main()
