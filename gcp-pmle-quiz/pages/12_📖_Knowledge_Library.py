"""Phase 5 Move 2 — Knowledge Library.

Searchable / browsable cards for concepts, products, decision trees. Each
card carries a ``canonical_url`` pointing at the public source it
summarizes (Google Cloud docs, Skills Boost path, etc.).
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from utils import set_css_style
from utils.profile_ui import render_sidebar
from utils.knowledge import (
    KnowledgeCard,
    all_cards,
    count_questions_for_card,
    filter_by_section,
    load_knowledge,
    related_cards,
    search_cards,
)


def _render_card(card: KnowledgeCard, payload) -> None:
    title_prefix = "🏆 " if card.high_yield else ""
    with st.container(border=True):
        st.markdown(f"### {title_prefix}{card.title}")
        st.markdown(card.blurb)
        if card.tags:
            tag_chips = " ".join(f"`{t}`" for t in card.tags)
            st.caption(tag_chips)

        # Phase 6a.5: question count + related cards back-references
        meta_cols = st.columns([2, 2, 6])
        n_questions = count_questions_for_card(card)
        with meta_cols[0]:
            st.caption(f"🤔 {n_questions} questions in bank")
        related = related_cards(card, payload)
        with meta_cols[1]:
            st.caption(f"🔗 {len(related)} related cards")

        if related:
            with st.expander("🔗 Related cards"):
                for rc in related[:8]:
                    rc_prefix = "🏆 " if rc.high_yield else ""
                    st.markdown(f"- {rc_prefix}**{rc.title}** — {rc.blurb}")

        if card.canonical_url:
            st.markdown(f"📖 [Read the canonical source ↗]({card.canonical_url})")


def _render_card_list(cards: list[KnowledgeCard], payload) -> None:
    if not cards:
        st.info("No cards match.")
        return
    # High-yield first
    cards = sorted(cards, key=lambda c: (not c.high_yield, c.title))
    for c in cards:
        _render_card(c, payload)


def main() -> None:
    st.set_page_config(page_title="Knowledge Library", page_icon="📖", layout="wide")
    set_css_style(Path("style.css"))
    render_sidebar()

    st.title("📖 Knowledge Library")
    st.caption(
        "Quick-reference cards for the concepts, products, and decision trees the "
        "exam covers. 🏆 = high-yield distinguishing topic. Each card links to the "
        "canonical public source it summarizes."
    )

    payload = load_knowledge()
    total = len(payload.concepts) + len(payload.products) + len(payload.decision_trees)
    st.caption(
        f"{len(payload.concepts)} concepts · {len(payload.products)} products · "
        f"{len(payload.decision_trees)} decision trees · {total} total cards."
    )

    with st.sidebar:
        st.header("🔍 Filter")
        query = st.text_input("Search title / blurb / tags", value="", key="kl_query")
        section_options = sorted(
            {
                t for c in all_cards(payload) for t in c.tags if t.startswith("§")
            }
        )
        sections_selected = st.multiselect(
            "Filter by exam section",
            options=section_options,
            default=[],
            key="kl_sections",
        )

    base = search_cards(query, payload) if query else all_cards(payload)
    if sections_selected:
        wanted = set(sections_selected)
        base = [c for c in base if any(t in wanted for t in c.tags)]

    high_yield_only = [c for c in base if c.high_yield]
    concept_ids = {c.id for c in payload.concepts}
    product_ids = {c.id for c in payload.products}
    dtree_ids = {c.id for c in payload.decision_trees}

    tabs = st.tabs([
        f"🧠 Concepts ({sum(1 for c in base if c.id in concept_ids)})",
        f"🏷 Products ({sum(1 for c in base if c.id in product_ids)})",
        f"🌳 Decision Trees ({sum(1 for c in base if c.id in dtree_ids)})",
        f"🏆 High-yield ({len(high_yield_only)})",
    ])

    with tabs[0]:
        _render_card_list([c for c in base if c.id in concept_ids], payload)
    with tabs[1]:
        _render_card_list([c for c in base if c.id in product_ids], payload)
    with tabs[2]:
        _render_card_list([c for c in base if c.id in dtree_ids], payload)
    with tabs[3]:
        _render_card_list(high_yield_only, payload)


if __name__ == "__main__":
    main()
