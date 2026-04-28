"""Phase 6a — Plan: full 12-week roadmap with three view modes.

Reads ``data/study_plan.json`` (parsed from ``study_plan.md``) and the
active profile's cursor. Lets the user inspect any week/day, jump there
via the manual override, or sweep the whole plan as a calendar grid or
flat task list.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import streamlit as st

from utils import set_css_style
from utils.profiles import current_profile, ensure_default_profiles
from utils.study_plan import Day, Week, load_study_plan
from utils.today import (
    DAY_LABELS,
    day_id,
    expected_position,
    load_cursor,
    set_manual_override,
)

st.set_page_config(
    page_title="GCP PMLE — Plan",
    page_icon="🗺",
    initial_sidebar_state="collapsed",
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

STATUS_STYLE = {
    "done": ("✅", "#bbf7d0"),
    "skipped": ("⏭", "#fde68a"),
    "current": ("📍", "#bfdbfe"),
    "missed": ("⚠", "#fecaca"),
    "future": ("·", "#e5e7eb"),
}


def _day_status(week_num: int, day_index: int, cursor, expected_w: int, expected_d: int) -> str:
    did = day_id(week_num, day_index)
    if did in cursor.completed_days:
        return "done"
    if did in cursor.skipped_days:
        return "skipped"
    if (week_num, day_index) == (expected_w, expected_d):
        return "current"
    if (week_num, day_index) < (expected_w, expected_d):
        return "missed"
    return "future"


def _resolve_day(week: Week, day_index: int) -> Day | None:
    if day_index < 5:
        return next((d for d in week.days if d.day_index == day_index), None)
    if day_index == 5:
        return week.saturday or next((d for d in week.days if d.day_index == 5), None)
    if day_index == 6:
        return week.sunday
    return None


def _render_day_block(week: Week, day: Day | None, day_index: int, status: str) -> None:
    icon, bg = STATUS_STYLE[status]
    label = DAY_LABELS[day_index]
    if day is None:
        st.markdown(
            f"<div style='background:{bg};padding:6px 10px;border-radius:6px;'>"
            f"{icon} <b>{label}</b> — (no scheduled tasks)</div>",
            unsafe_allow_html=True,
        )
        return
    head = f"{icon} <b>{label}</b>"
    if day.estimated_min:
        head += f" · ~{day.estimated_min} min"
    st.markdown(
        f"<div style='background:{bg};padding:6px 10px;border-radius:6px;'>{head}</div>",
        unsafe_allow_html=True,
    )
    for t in day.tasks:
        sub_cols = st.columns([1, 10])
        with sub_cols[0]:
            st.markdown(f"<div style='font-size:1.5em;'>{TASK_ICONS.get(t.type, '•')}</div>", unsafe_allow_html=True)
        with sub_cols[1]:
            if t.ref and t.ref.startswith("http"):
                st.markdown(f"[{t.label}]({t.ref})")
            else:
                st.markdown(t.label)


def render_week_view(plan, cursor, expected_w: int, expected_d: int) -> None:
    if not plan.weeks:
        st.info("No plan loaded — run `python scripts/parse_study_plan.py`.")
        return
    week_options = {f"Week {w.num} — {w.theme}": w.num for w in plan.weeks}
    default_label = next(
        (lbl for lbl, n in week_options.items() if n == expected_w),
        list(week_options.keys())[0],
    )
    selected = st.selectbox(
        "Pick a week",
        list(week_options.keys()),
        index=list(week_options.keys()).index(default_label),
        key="plan_week_select",
    )
    week = next(w for w in plan.weeks if w.num == week_options[selected])

    head_cols = st.columns([4, 1, 1, 1, 1])
    with head_cols[0]:
        st.markdown(f"### Week {week.num} — {week.theme}")
        st.caption(
            f"§: {', '.join(week.exam_sections) or '—'} · "
            f"~{week.estimated_hours or 0:.1f}h · "
            f"target: {int(week.sunday_quiz_target * 100) if week.sunday_quiz_target else '—'}%"
        )
    with head_cols[1]:
        if st.button("Jump → Mon", key=f"plan_jump_w{week.num}"):
            set_manual_override(day_id(week.num, 0))
            st.toast(f"Jumped to Week {week.num} Mon. Open 📍 Today.")

    if week.saturday_lab_label:
        if week.saturday_lab_url:
            st.markdown(f"🧪 **Saturday lab:** [{week.saturday_lab_label}]({week.saturday_lab_url})")
        else:
            st.markdown(f"🧪 **Saturday lab:** {week.saturday_lab_label}")

    with st.expander(f"📦 Hard deliverables ({len(week.deliverables)})"):
        for d in week.deliverables:
            st.markdown(f"- {d.label}")
    if week.concept_anchors:
        with st.expander(f"🧠 Concept anchors ({len(week.concept_anchors)})"):
            for a in week.concept_anchors:
                st.markdown(f"- {a}")

    st.divider()
    for day_index in range(7):
        with st.container(border=True):
            day = _resolve_day(week, day_index)
            status = _day_status(week.num, day_index, cursor, expected_w, expected_d)
            _render_day_block(week, day, day_index, status)
            jump_cols = st.columns([8, 2])
            with jump_cols[1]:
                if st.button(
                    "Set as today",
                    key=f"plan_jump_w{week.num}_d{day_index}",
                    use_container_width=True,
                ):
                    set_manual_override(day_id(week.num, day_index))
                    st.toast(f"📍 Override → Week {week.num} {DAY_LABELS[day_index]}")

    if week.above_and_beyond:
        with st.expander(f"🚀 Above-and-beyond ({len(week.above_and_beyond)})"):
            for a in week.above_and_beyond:
                st.markdown(f"- {a.label}")


def render_calendar(plan, cursor, expected_w: int, expected_d: int) -> None:
    if not plan.weeks:
        st.info("No plan loaded.")
        return
    st.markdown("**Calendar grid** — rows are weeks, columns are days. Click any cell to jump.")

    # Header row
    head = st.columns([1] + [1] * 7)
    head[0].markdown("&nbsp;")
    for i, lbl in enumerate(DAY_LABELS):
        head[i + 1].markdown(f"<div style='text-align:center;font-weight:600;'>{lbl}</div>", unsafe_allow_html=True)

    for week in plan.weeks:
        cols = st.columns([1] + [1] * 7)
        with cols[0]:
            st.markdown(
                f"<div style='font-weight:600;padding-top:6px;'>W{week.num}</div>",
                unsafe_allow_html=True,
            )
        for day_index in range(7):
            status = _day_status(week.num, day_index, cursor, expected_w, expected_d)
            icon, bg = STATUS_STYLE[status]
            with cols[day_index + 1]:
                if st.button(
                    icon,
                    key=f"cal_w{week.num}_d{day_index}",
                    use_container_width=True,
                    help=f"Week {week.num} {DAY_LABELS[day_index]} — {status}",
                ):
                    set_manual_override(day_id(week.num, day_index))
                    st.toast(f"📍 Override → Week {week.num} {DAY_LABELS[day_index]}")

    st.caption(
        " · ".join(
            f"{icon} {label}" for label, (icon, _) in STATUS_STYLE.items()
        )
    )


def render_list(plan, cursor, expected_w: int, expected_d: int) -> None:
    if not plan.weeks:
        st.info("No plan loaded.")
        return
    rows: list[tuple[int, int, Day | None, str]] = []
    for week in plan.weeks:
        for day_index in range(7):
            day = _resolve_day(week, day_index)
            status = _day_status(week.num, day_index, cursor, expected_w, expected_d)
            rows.append((week.num, day_index, day, status))

    only_unfinished = st.checkbox("Hide done + skipped", value=False)
    for week_num, day_index, day, status in rows:
        if only_unfinished and status in ("done", "skipped"):
            continue
        if day is None:
            continue
        icon, _ = STATUS_STYLE[status]
        with st.container(border=True):
            cols = st.columns([1, 9, 2])
            with cols[0]:
                st.markdown(
                    f"<div style='font-size:1.4em;text-align:center;'>{icon}</div>",
                    unsafe_allow_html=True,
                )
            with cols[1]:
                st.markdown(
                    f"**Week {week_num} {DAY_LABELS[day_index]}** — "
                    f"{day.tasks[0].label if day.tasks else '(no tasks)'}"
                )
                meta: list[str] = []
                if day.estimated_min:
                    meta.append(f"~{day.estimated_min} min")
                if day.tasks:
                    meta.append(day.tasks[0].type)
                if meta:
                    st.caption(" · ".join(meta))
            with cols[2]:
                if st.button("Set as today", key=f"list_w{week_num}_d{day_index}"):
                    set_manual_override(day_id(week_num, day_index))
                    st.toast(f"📍 Override → Week {week_num} {DAY_LABELS[day_index]}")


def main() -> None:
    set_css_style(Path("style.css"))
    ensure_default_profiles()

    st.title("🗺 12-Week Plan")
    profile = current_profile()
    plan = load_study_plan()
    cursor = load_cursor()

    try:
        start = date.fromisoformat(profile.study_start_date)
    except ValueError:
        start = date.today()
    expected_w, expected_d, _, _ = expected_position(
        start, date.today(), max(len(plan.weeks), 1)
    )

    head_cols = st.columns([4, 2, 2])
    with head_cols[0]:
        st.caption(
            f"Profile: **{profile.display_name}** · "
            f"Start: {profile.study_start_date} · "
            f"Exam: {profile.exam_target_date}"
        )
    with head_cols[1]:
        completed = len(cursor.completed_days)
        total = len(plan.weeks) * 7
        pct = completed / total if total else 0
        st.metric("Days complete", f"{completed} / {total}", f"{pct * 100:.0f}%")
    with head_cols[2]:
        if cursor.manual_override_day and st.button("Clear override"):
            set_manual_override(None)
            st.rerun()

    mode = st.radio(
        "View",
        ["Week view", "Calendar grid", "Task list"],
        horizontal=True,
        key="plan_view_mode",
    )
    st.divider()

    if mode == "Week view":
        render_week_view(plan, cursor, expected_w, expected_d)
    elif mode == "Calendar grid":
        render_calendar(plan, cursor, expected_w, expected_d)
    else:
        render_list(plan, cursor, expected_w, expected_d)


if __name__ == "__main__":
    main()
