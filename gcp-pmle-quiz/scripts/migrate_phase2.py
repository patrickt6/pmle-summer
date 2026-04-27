"""Phase 2 migration: tag the 841-question Andy bank with `source` and `exam_section`.

Run from the gcp-pmle-quiz/ directory:
    python3 scripts/migrate_phase2.py             # apply
    python3 scripts/migrate_phase2.py --audit     # audit only, no write

Idempotent: only writes a field if it is currently None / missing. Safe to re-run.
Atomic: writes to data/quizzes.jsonl.tmp then os.replace().
Preserves all existing fields (incl. ml_topics / gcp_products / gcp_topics that aren't in the Pydantic model).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
QUIZ_FILE = DATA_DIR / "quizzes.jsonl"
TMP_FILE = QUIZ_FILE.with_suffix(".jsonl.tmp")
MAPPING_FILE = DATA_DIR / "section-mapping.json"

SOURCE_TAG = "AndyTheFactory"


def load_mapping() -> list[dict]:
    with MAPPING_FILE.open() as f:
        return json.load(f)["rules"]


def build_corpus(record: dict) -> str:
    parts: list[str] = []
    for field in ("gcp_topics", "ml_topics", "gcp_products"):
        for tag in record.get(field) or []:
            if isinstance(tag, str):
                parts.append(tag)
    return " || ".join(parts).lower()


_PATTERN_CACHE: dict[str, re.Pattern[str]] = {}


def _compile(pat: str) -> re.Pattern[str]:
    p = _PATTERN_CACHE.get(pat)
    if p is None:
        # Word boundary on both sides, case-insensitive. Escape pattern so '/' etc. are literal.
        p = re.compile(r"\b" + re.escape(pat.lower()) + r"\b")
        _PATTERN_CACHE[pat] = p
    return p


def infer_section(record: dict, rules: list[dict]) -> str | None:
    corpus = build_corpus(record)
    if not corpus:
        return None
    for rule in rules:
        for pat in rule["patterns"]:
            if _compile(pat).search(corpus):
                return rule["section"]
    return None


def audit(records: list[dict]) -> None:
    gcp_topics: Counter[str] = Counter()
    ml_topics: Counter[str] = Counter()
    gcp_products: Counter[str] = Counter()
    for r in records:
        for t in r.get("gcp_topics") or []:
            gcp_topics[t] += 1
        for t in r.get("ml_topics") or []:
            ml_topics[t] += 1
        for t in r.get("gcp_products") or []:
            gcp_products[t] += 1
    print(f"Total records: {len(records)}")
    print(f"  gcp_topics:   {len(gcp_topics)} unique  | top 20: {gcp_topics.most_common(20)}")
    print(f"  ml_topics:    {len(ml_topics)} unique  | top 20: {ml_topics.most_common(20)}")
    print(f"  gcp_products: {len(gcp_products)} unique  | top 20: {gcp_products.most_common(20)}")


def apply_migration(
    records: list[dict],
    rules: list[dict],
    force_section: bool = False,
) -> tuple[int, int, Counter[str], list[int]]:
    set_source = 0
    set_section = 0
    section_counts: Counter[str] = Counter()
    orphan_ids: list[int] = []
    for r in records:
        if r.get("source") is None:
            r["source"] = SOURCE_TAG
            set_source += 1
        if force_section or r.get("exam_section") is None:
            section = infer_section(r, rules)
            r["exam_section"] = section
            if section is not None:
                set_section += 1
            else:
                orphan_ids.append(r["id"])
        else:
            if r.get("exam_section") is None:
                orphan_ids.append(r["id"])
        if r.get("exam_section"):
            section_counts[r["exam_section"]] += 1
    return set_source, set_section, section_counts, orphan_ids


def atomic_write(records: list[dict]) -> None:
    with TMP_FILE.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(TMP_FILE, QUIZ_FILE)


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 2 migration for Andy bank")
    parser.add_argument("--audit", action="store_true", help="audit only, do not write")
    parser.add_argument(
        "--force-section",
        action="store_true",
        help="re-infer exam_section for ALL records, overriding existing values (use when refining rules)",
    )
    args = parser.parse_args()

    if not QUIZ_FILE.exists():
        print(f"ERROR: {QUIZ_FILE} not found", file=sys.stderr)
        return 1
    if not MAPPING_FILE.exists():
        print(f"ERROR: {MAPPING_FILE} not found", file=sys.stderr)
        return 1

    records: list[dict] = []
    with QUIZ_FILE.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))

    if args.audit:
        audit(records)
        return 0

    rules = load_mapping()
    set_source, set_section, section_counts, orphan_ids = apply_migration(
        records, rules, force_section=args.force_section
    )
    atomic_write(records)

    total = len(records)
    null_section = total - sum(section_counts.values())

    print(f"Processed {total} records.")
    print(f"  source set on this run: {set_source}")
    print(f"  exam_section set on this run: {set_section}")
    print(f"  records still with exam_section=null: {null_section} ({null_section / total * 100:.1f}%)")
    print()

    section_groups: dict[str, int] = defaultdict(int)
    for sec, n in section_counts.items():
        parent = sec.split(".")[0]
        section_groups[parent] += n

    print("Per-subsection counts:")
    for sec in sorted(section_counts):
        n = section_counts[sec]
        print(f"  {sec:6s}  {n:4d}  ({n / total * 100:.1f}%)")
    print()
    print("Per-section (parent) counts:")
    targets = {"§1": 13, "§2": 14, "§3": 18, "§4": 20, "§5": 22, "§6": 13}
    for sec in sorted(section_groups):
        n = section_groups[sec]
        target_pct = targets.get(sec)
        target_n = round(target_pct / 100 * total) if target_pct is not None else None
        target_str = f" target~{target_n} ({target_pct}%)" if target_n is not None else ""
        print(f"  {sec}  {n:4d}  ({n / total * 100:.1f}%){target_str}")

    if orphan_ids:
        sample = orphan_ids[: min(15, len(orphan_ids))]
        print()
        print(f"First {len(sample)} orphan IDs (exam_section=null): {sample}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
