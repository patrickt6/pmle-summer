"""Phase 5 — Knowledge library loader (extended in Phase 6a.5).

Reads ``data/knowledge.json`` (concepts + products + decision-trees with
tags and a ``canonical_url`` pointing at the public source the card
summarizes — Google Cloud docs, Skills Boost path, etc.). Phase 6a.5
adds related-card discovery and question-count back-references so the
Library page can be navigated as a hub.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from pydantic import BaseModel, Field

from utils import DATA_DIR, QUIZ_FILE

KNOWLEDGE_FILE = DATA_DIR / "knowledge.json"

# H1–H4 markdown headings; ``re.MULTILINE`` so ``^`` anchors per line.
HEADING_RE = re.compile(r"^(#{1,4})\s+(.+?)\s*$", re.MULTILINE)
ANCHOR_NORMALIZE_RE = re.compile(r"[^a-z0-9]+")


class KnowledgeCard(BaseModel):
    id: str
    title: str
    blurb: str
    tags: list[str] = Field(default_factory=list)
    canonical_url: str = ""
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


# ---------- Phase 6a.5: TOC / related cards / question counts ----------


class TocEntry(BaseModel):
    level: int
    text: str
    anchor: str


def slug(text: str) -> str:
    """GitHub-style anchor slug for a heading."""
    return ANCHOR_NORMALIZE_RE.sub("-", text.lower()).strip("-")


def extract_toc(md_text: str) -> list[TocEntry]:
    """Pull H1–H4 headings out of a markdown blob in document order."""
    out: list[TocEntry] = []
    for m in HEADING_RE.finditer(md_text):
        level = len(m.group(1))
        text = m.group(2).strip()
        # Skip common false positives like fenced code blocks indenting "#"
        out.append(TocEntry(level=level, text=text, anchor=slug(text)))
    return out


def related_cards(
    card: KnowledgeCard,
    payload: KnowledgePayload | None = None,
    min_shared_tags: int = 2,
) -> list[KnowledgeCard]:
    """Cards sharing at least ``min_shared_tags`` tags with ``card``.

    The card itself is excluded. Results are sorted by number of shared
    tags (descending) then title.
    """
    own_tags = set(card.tags)
    if not own_tags:
        return []
    out: list[tuple[int, KnowledgeCard]] = []
    for c in all_cards(payload):
        if c.id == card.id:
            continue
        shared = len(own_tags & set(c.tags))
        if shared >= min_shared_tags:
            out.append((shared, c))
    out.sort(key=lambda pair: (-pair[0], pair[1].title))
    return [c for _, c in out]


def _question_tag_haystack(question: dict) -> str:
    parts: list[str] = []
    for field in ("gcp_topics", "gcp_products", "ml_topics"):
        val = question.get(field) or []
        if isinstance(val, list):
            parts.extend(str(v) for v in val)
        elif isinstance(val, str):
            parts.append(val)
    sec = question.get("exam_section")
    if sec:
        parts.append(str(sec))
    return " ".join(parts).lower()


def count_questions_for_card(
    card: KnowledgeCard, quiz_file: Path | None = None
) -> int:
    """Count quizzes whose tag fields match any of this card's tags.

    Substring match is intentional: cards have human-friendly tags like
    "Reduction Server" while questions use list fields with the same
    label. Skips mock-pool questions so the calibration set isn't
    leaked.
    """
    qf = quiz_file or QUIZ_FILE
    if not qf.exists() or not card.tags:
        return 0
    tags_lower = [t.lower() for t in card.tags]
    n = 0
    with qf.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("mock_pool"):
                continue
            haystack = _question_tag_haystack(rec)
            if any(t in haystack for t in tags_lower):
                n += 1
    return n
