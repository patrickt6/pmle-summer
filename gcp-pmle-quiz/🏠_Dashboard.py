from pathlib import Path

import streamlit as st

from dashboard import show_dashboard
from utils import reset_progress, save_progress, set_css_style
from utils.labs import lab_completion_summary

st.set_page_config(
    page_title="GCP PMLE — Patrick & Matty Boy",
    page_icon="☁️",
    initial_sidebar_state="collapsed",
    layout="wide",
)

MEME_IMAGE_URL = "https://i.imgur.com/7kyduZy.png"
STUDY_AUDIO_URL = "https://www.youtube.com/watch?v=74cOUSKXMz0&t=0s"


def render_hero():
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
        "<p style='text-align:center;font-size:1.2em;margin-top:0;'>"
        "A study companion for <b>Patrick</b> and <b>Matty Boy</b> 🚀"
        "</p>",
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


def render_study_audio():
    cols = st.columns([2, 3, 2])
    with cols[1]:
        st.subheader("🎧 Study soundtrack")
        st.caption("Hit play, lock in, drill questions.")
        st.video(STUDY_AUDIO_URL)


def main():
    set_css_style(Path("style.css"))

    render_hero()
    st.divider()
    render_study_audio()
    st.divider()

    # Lab completion banner — Phase 5 cross-link
    try:
        labs_summary = lab_completion_summary()
        st.markdown(
            f"<p style='text-align:center;margin-top:0;'>"
            f"🧪 Labs done: <b>{labs_summary['completed_must']} / {labs_summary['must_labs']} must-rated</b> · "
            f"{labs_summary['completed_total']} / {labs_summary['total_labs']} total · "
            f"{labs_summary['hours_logged']:g}h logged"
            f"</p>",
            unsafe_allow_html=True,
        )
    except Exception:
        pass

    st.subheader("📊 Progress dashboard")
    stats = show_dashboard()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Start", type="primary"):
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
        if st.button("‼️ Reset progress"):
            st.warning("This will clear all your progress and cannot be undone.", icon="⚠️")
            if st.button(
                "Yes",
                icon="🚨",
            ):
                reset_progress()
                progress = {}
                save_progress(progress)
                st.rerun()


if __name__ == "__main__":
    main()
