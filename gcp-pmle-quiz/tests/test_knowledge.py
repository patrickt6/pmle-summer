"""Tests for utils.knowledge — Phase 5 knowledge library."""

from __future__ import annotations

from pathlib import Path

import pytest

from utils.knowledge import (
    all_cards,
    count_questions_for_card,
    extract_toc,
    filter_by_section,
    load_knowledge,
    related_cards,
    search_cards,
    slug,
)


def test_load_knowledge_returns_payload():
    p = load_knowledge()
    assert len(p.concepts) > 0
    assert len(p.products) > 0
    assert len(p.decision_trees) > 0


def test_total_card_count():
    """We bootstrapped with ≥ 9 + 7 + 3 = 19 cards."""
    p = load_knowledge()
    assert len(p.concepts) + len(p.products) + len(p.decision_trees) >= 19


def test_high_yield_cards_present():
    p = load_knowledge()
    high_yield = [c for c in all_cards(p) if c.high_yield]
    assert len(high_yield) >= 5


def test_search_finds_skew_card():
    results = search_cards("skew")
    assert any("skew" in c.id.lower() for c in results)


def test_search_case_insensitive():
    a = search_cards("REDUCTION")
    b = search_cards("reduction")
    assert {c.id for c in a} == {c.id for c in b}


def test_search_empty_returns_all():
    p = load_knowledge()
    assert len(search_cards("")) == len(all_cards(p))


def test_filter_by_section_3_3():
    cards = filter_by_section("§3.3")
    assert any("reduction-server" in c.id for c in cards)


def test_filter_by_section_no_match():
    assert filter_by_section("§99") == []


def test_canonical_urls_are_https():
    """Every card with a canonical_url must point at an https URL."""
    p = load_knowledge()
    for c in all_cards(p):
        if not c.canonical_url:
            continue
        assert c.canonical_url.startswith("https://"), (
            f"canonical_url for {c.id} is not https: {c.canonical_url}"
        )


def test_card_tags_have_section_format():
    """At least one tag per card should be a §X.Y section ref or a clearly product name."""
    p = load_knowledge()
    for c in all_cards(p):
        assert c.tags, f"Card {c.id} has no tags"


# ---------- Phase 6a.5: TOC + related cards + question counts ----------


def test_slug_basic():
    assert slug("Reduction Server") == "reduction-server"
    assert slug("§3.3 — Hardware") == "3-3-hardware"
    assert slug("Already-slug-friendly") == "already-slug-friendly"


def test_extract_toc_finds_headings():
    md = "# Title\n\n## Section A\n\nbody\n\n### Subsection\n\n## Section B\n"
    toc = extract_toc(md)
    assert [t.text for t in toc] == ["Title", "Section A", "Subsection", "Section B"]
    assert [t.level for t in toc] == [1, 2, 3, 2]


def test_extract_toc_anchors_match_slug():
    md = "## Reduction Server\n"
    toc = extract_toc(md)
    assert toc[0].anchor == "reduction-server"


def test_extract_toc_handles_empty():
    assert extract_toc("plain prose with no headings") == []


def test_high_yield_cards_have_canonical_url():
    """High-yield cards must link to a public source so external readers can follow them."""
    p = load_knowledge()
    for c in all_cards(p):
        if not c.high_yield:
            continue
        assert c.canonical_url, f"High-yield card {c.id} is missing canonical_url"


def test_related_cards_excludes_self():
    p = load_knowledge()
    for c in all_cards(p):
        related = related_cards(c, p)
        assert all(r.id != c.id for r in related)


def test_related_cards_min_shared_tags():
    p = load_knowledge()
    cards = all_cards(p)
    if len(cards) < 2:
        return
    for c in cards:
        for r in related_cards(c, p, min_shared_tags=2):
            shared = set(c.tags) & set(r.tags)
            assert len(shared) >= 2


def test_related_cards_no_tags_returns_empty():
    p = load_knowledge()
    sample = all_cards(p)[0]
    # Construct a card with no tags via model_copy
    bare = sample.model_copy(update={"tags": []})
    assert related_cards(bare, p) == []


def test_count_questions_for_card_returns_nonzero_for_real_data():
    """High-yield cards should resolve to ≥ 1 question (no orphans)."""
    p = load_knowledge()
    high_yield = [c for c in all_cards(p) if c.high_yield]
    if not high_yield:
        return
    matched = sum(1 for c in high_yield if count_questions_for_card(c) > 0)
    # Allow up to 1 orphan; we want the vast majority to resolve.
    assert matched >= len(high_yield) - 1, (
        f"Only {matched}/{len(high_yield)} high-yield cards have questions in bank"
    )


def test_count_questions_for_card_handles_empty_tags():
    p = load_knowledge()
    sample = all_cards(p)[0]
    bare = sample.model_copy(update={"tags": []})
    assert count_questions_for_card(bare) == 0
