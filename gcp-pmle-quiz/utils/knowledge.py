"""Phase 5 — Knowledge library loader.

Reads `data/knowledge.json` (concepts + products + decision-trees with tags
and links to the underlying research/ markdown).
"""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field

from utils import DATA_DIR

KNOWLEDGE_FILE = DATA_DIR / "knowledge.json"


class KnowledgeCard(BaseModel):
    id: str
    title: str
    blurb: str
    tags: list[str] = Field(default_factory=list)
    research_file: str = ""
    high_yield: bool = False


class KnowledgePayload(BaseModel):
    concepts: list[KnowledgeCard] = Field(default_factory=list)
    products: list[KnowledgeCard] = Field(default_factory=list)
    decision_trees: list[KnowledgeCard] = Field(default_factory=list)


def load_knowledge() -> KnowledgePayload:
    if not KNOWLEDGE_FILE.exists():
        return KnowledgePayload()
    with KNOWLEDGE_FILE.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    return KnowledgePayload(
        concepts=[KnowledgeCard.model_validate(c) for c in payload.get("concepts", [])],
        products=[KnowledgeCard.model_validate(c) for c in payload.get("products", [])],
        decision_trees=[KnowledgeCard.model_validate(c) for c in payload.get("decision_trees", [])],
    )


def all_cards(payload: KnowledgePayload | None = None) -> list[KnowledgeCard]:
    p = payload or load_knowledge()
    return [*p.concepts, *p.products, *p.decision_trees]


def search_cards(query: str, payload: KnowledgePayload | None = None) -> list[KnowledgeCard]:
    """Case-insensitive substring search over title, blurb, tags."""
    q = (query or "").lower().strip()
    if not q:
        return all_cards(payload)
    out: list[KnowledgeCard] = []
    for c in all_cards(payload):
        haystack = " ".join([c.title, c.blurb, *c.tags]).lower()
        if q in haystack:
            out.append(c)
    return out


def filter_by_section(section: str, payload: KnowledgePayload | None = None) -> list[KnowledgeCard]:
    return [c for c in all_cards(payload) if section in c.tags]
