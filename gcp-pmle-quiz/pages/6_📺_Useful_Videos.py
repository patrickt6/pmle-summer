"""Useful Videos — curated YouTube clips for PMLE prep.

Add new entries to VIDEOS below. Each entry:
  {"title": str, "url": str, "section": str | None, "note": str | None}
"""

from pathlib import Path

import streamlit as st

from utils import set_css_style
from utils.profile_ui import render_sidebar

VIDEOS: list[dict[str, str | None]] = [
    {
        "title": "PMLE study reference clip",
        "url": "https://www.youtube.com/watch?v=M4-iqESGPns&t=0s",
        "section": None,
        "note": None,
    },
]


def main():
    st.set_page_config(page_title="Useful Videos", page_icon="📺", layout="wide")
    set_css_style(Path("style.css"))
    render_sidebar()

    st.title("📺 Useful Videos")
    st.caption(
        "Curated YouTube videos for PMLE prep. "
        "Add more by editing the `VIDEOS` list at the top of this file."
    )
    st.divider()

    if not VIDEOS:
        st.info("No videos added yet.")
        return

    for i, v in enumerate(VIDEOS):
        st.subheader(v["title"])
        meta_bits = []
        if v.get("section"):
            meta_bits.append(f"Section **{v['section']}**")
        if v.get("note"):
            meta_bits.append(v["note"])
        if meta_bits:
            st.caption(" · ".join(meta_bits))
        st.video(v["url"])
        if i < len(VIDEOS) - 1:
            st.divider()


if __name__ == "__main__":
    main()
