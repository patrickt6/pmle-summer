"""🏠 Home — hero + study soundtrack + lab banner + progress dashboard.

Phase 6a kept this as the Streamlit home (root file) for the familiar
landing-page feel. The wayfinding lives at ``pages/0_📍_Today.py``;
this page is the "open the app and orient yourself" landing.

Per-profile progress data is read via the (profile-aware) ``utils``
helpers, so switching profile in the sidebar updates the metrics +
knowledge-gap charts here without code changes.
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from dashboard import show_dashboard
from utils import reset_progress, save_progress, set_css_style
from utils.labs import lab_completion_summary
from utils.profile_ui import render_sidebar
from utils.profiles import current_profile

st.set_page_config(
    page_title="GCP PMLE — Patrick & Matty Boy",
    page_icon="☁️",
    initial_sidebar_state="expanded",
    layout="wide",
)

MEME_IMAGE_URL = "https://i.imgur.com/7kyduZy.png"
STUDY_AUDIO_URL = "https://www.youtube.com/watch?v=74cOUSKXMz0&t=0s"


def render_hero() -> None:
    profile = current_profile()
    st.markdown(
        "<h1 style='text-align:center;margin-bottom:0;'>"
        "☁️ Google Cloud Platform <span style='color:#4285F4'>P</span>"
        "<span style='color:#EA4335'>M</span>"
        "<span style='color:#FBBC05'>L</span>"
        "<span style='color:#34A853'>E</span>"
        "</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='text-align:center;font-size:1.2em;margin-top:0;'>"
        f"Studying together as <b>Patrick</b> &amp; <b>Matty Boy</b> — "
        f"active profile: <span style='color:{profile.color};font-weight:700;'>"
        f"{profile.display_name}</span> 🚀"
        f"</p>",
        unsafe_allow_html=True,
    )
    st.caption(
        "<p style='text-align:center;'>PMLE v3.1 · 12-week sprint · 60–75 study hours · "
        "841 practice questions · 14 research reports</p>",
        unsafe_allow_html=True,
    )

    cols = st.columns([3, 2, 3])
    with cols[1]:
        st.image(MEME_IMAGE_URL, caption="The PMLE journey, summarized.", width=320)


def render_study_audio() -> None:
    cols = st.columns([2, 3, 2])
    with cols[1]:
        st.subheader("🎧 Study soundtrack")
        st.caption("Hit play, lock in, drill questions.")
        st.video(STUDY_AUDIO_URL)


def render_quick_links() -> None:
    cols = st.columns(3)
    with cols[0]:
        st.page_link("pages/0_📍_Today.py", label="📍 Today — what to do right now", use_container_width=True)
    with cols[1]:
        st.page_link("pages/14_🗺_Plan.py", label="🗺 12-Week Plan", use_container_width=True)
    with cols[2]:
        st.page_link("pages/13_🧪_Labs.py", label="🧪 Labs", use_container_width=True)


def render_lab_banner() -> None:
    try:
        summary = lab_completion_summary()
    except Exception:
        return
    st.markdown(
        f"<p style='text-align:center;margin-top:0;'>"
        f"🧪 Labs done: <b>{summary['completed_must']} / {summary['must_labs']} must-rated</b> · "
        f"{summary['completed_total']} / {summary['total_labs']} total · "
        f"{summary['hours_logged']:g}h logged"
        f"</p>",
        unsafe_allow_html=True,
    )


def render_actions(stats: dict) -> None:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Start quiz round", type="primary", use_container_width=True):
            if stats["total"] == 0:
                st.warning("⚠️ No quizzes found in data/quizzes.jsonl")
                return
            st.session_state.quiz_in_progress = False
            st.session_state.quizzes = None
            st.session_state.quiz_mode_pos = 0
            st.session_state.quiz_mode_round_progress = {}
            st.session_state.quiz_mode_answered = False
            st.switch_page("pages/3_🤔_Quiz_Mode.py")

    with col2:
        with st.popover("‼️ Reset progress (active profile only)", use_container_width=True):
            st.warning(
                f"This clears all progress for **{current_profile().display_name}** and cannot be undone.",
                icon="⚠️",
            )
            if st.button("Yes, reset", icon="🚨", key="confirm_reset"):
                reset_progress()
                save_progress({})
                st.toast("Progress reset for active profile.")
                st.rerun()


def main() -> None:
    set_css_style(Path("style.css"))
    render_sidebar()

    render_hero()
    st.divider()
    render_quick_links()
    st.divider()
    render_study_audio()
    st.divider()
    render_lab_banner()
    st.subheader("📊 Progress dashboard")
    stats = show_dashboard()
    render_actions(stats)


if __name__ == "__main__":
    main()
