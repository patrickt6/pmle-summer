"""Streamlit-aware sidebar helpers for the active profile.

Kept separate from ``utils/profiles.py`` so the headless core stays
Streamlit-free and unit-testable. Pages call ``render_sidebar()`` to
get the consistent profile picker + editable dates.
"""

from __future__ import annotations

from datetime import date

import streamlit as st

from utils.profiles import (
    current_profile,
    ensure_default_profiles,
    list_profiles,
    set_current_profile,
    update_profile,
)


def render_sidebar() -> None:
    ensure_default_profiles()
    profiles = list_profiles()
    cur = current_profile()
    label_to_name = {p.display_name: p.name for p in profiles}
    labels = list(label_to_name.keys())
    current_label = cur.display_name if cur.display_name in labels else labels[0]
    default_idx = labels.index(current_label)

    with st.sidebar:
        st.subheader("👤 Profile")
        choice = st.radio(
            "Active profile",
            labels,
            index=default_idx,
            key="profile_picker",
        )
        chosen_name = label_to_name[choice]
        if chosen_name != cur.name:
            set_current_profile(chosen_name)
            st.rerun()

        st.caption(
            f"📅 Start: **{cur.study_start_date}**  \n"
            f"🎯 Exam: **{cur.exam_target_date}**"
        )

        with st.expander("⚙ Edit dates", expanded=False):
            try:
                cur_start = date.fromisoformat(cur.study_start_date)
            except ValueError:
                cur_start = date.today()
            try:
                cur_exam = date.fromisoformat(cur.exam_target_date)
            except ValueError:
                cur_exam = date.today()

            new_start = st.date_input(
                "Study start date",
                value=cur_start,
                key=f"start_input_{cur.name}",
                help="Day 1 of Week 1 — changing this re-anchors 📍 Today and the Plan.",
            )
            new_exam = st.date_input(
                "Exam target date",
                value=cur_exam,
                key=f"exam_input_{cur.name}",
                help="The booked PMLE exam date — drives the days-to-exam countdown.",
            )

            dirty = (
                new_start.isoformat() != cur.study_start_date
                or new_exam.isoformat() != cur.exam_target_date
            )
            if dirty and st.button("💾 Save dates", key=f"save_dates_{cur.name}"):
                update_profile(
                    cur.name,
                    study_start_date=new_start.isoformat(),
                    exam_target_date=new_exam.isoformat(),
                )
                st.toast("Dates updated — re-anchoring Today.")
                st.rerun()
