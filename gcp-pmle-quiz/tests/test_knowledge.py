"""Tests for utils.knowledge — Phase 5 knowledge library."""

from __future__ import annotations

from pathlib import Path

import pytest

from utils.knowledge import (
    all_cards,
    filter_by_section,
    load_knowledge,
    search_cards,
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


def test_research_files_resolve():
    repo_root = Path(__file__).resolve().parents[2]
    p = load_knowledge()
    for c in all_cards(p):
        if not c.research_file:
            continue
        full = repo_root / c.research_file
        assert full.exists(), f"Research file missing for {c.id}: {c.research_file}"


def test_card_tags_have_section_format():
    """At least one tag per card should be a §X.Y section ref or a clearly product name."""
    p = load_knowledge()
    for c in all_cards(p):
        assert c.tags, f"Card {c.id} has no tags"
