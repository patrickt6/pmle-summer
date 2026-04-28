"""Phase 5 Move 2 — Knowledge Library.

Searchable / browsable cards for concepts, products, decision trees. Bridges
the gap between long-form research/ markdown and a need for quick reference.
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from utils import set_css_style
from utils.knowledge import (
    KnowledgeCard,
    all_cards,
    filter_by_section,
    load_knowledge,
    search_cards,
)

REPO_ROOT = Path(__file__).resolve().parents[2]


def _resolve_research(rel_path: str) -> Path:
    return REPO_ROOT / rel_path


def _render_card(card: KnowledgeCard) -> None:
    title_prefix = "🏆 " if card.high_yield else ""
    with st.container(border=True):
        st.markdown(f"### {title_prefix}{card.title}")
        st.markdown(card.blurb)
        if card.tags:
            tag_chips = " ".join(f"`{t}`" for t in card.tags)
            st.caption(tag_chips)
        if card.research_file:
            with st.expander("📖 Read full research"):
                fpath = _resolve_research(card.research_file)
                if fpath.exists():
                    st.markdown(fpath.read_text(encoding="utf-8"), unsafe_allow_html=True)
                else:
                    st.warning(f"Missing file: {card.research_file}")


def _render_card_list(cards: list[KnowledgeCard]) -> None:
    if not cards:
        st.info("No cards match.")
        return
    # High-yield first
    cards = sorted(cards, key=lambda c: (not c.high_yield, c.title))
    for c in cards:
        _render_card(c)


def main() -> None:
    st.set_page_config(page_title="Knowledge Library", page_icon="📖", layout="wide")
    set_css_style(Path("style.css"))

    st.title("📖 Knowledge Library")
    st.caption(
        "Quick-reference cards for the concepts, products, and decision trees that "
        "the research reports cover. 🏆 = high-yield distinguishing topic. Click any "
        "card's expander to read the full report inline."
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
        _render_card_list([c for c in base if c.id in concept_ids])
    with tabs[1]:
        _render_card_list([c for c in base if c.id in product_ids])
    with tabs[2]:
        _render_card_list([c for c in base if c.id in dtree_ids])
    with tabs[3]:
        _render_card_list(high_yield_only)


if __name__ == "__main__":
    main()
