"""Phase 2 Move 4: stratified-sample 100 questions into mock1-pool and 100 into mock2-pool.

Run from gcp-pmle-quiz/ directory:
    python3 scripts/tag_mock_pools.py             # apply
    python3 scripts/tag_mock_pools.py --dry-run   # preview, no write
    python3 scripts/tag_mock_pools.py --reset     # clear all mock_pool tags first, then re-sample

Per-section per-pool target counts (from v3.1 weights):
    §1: 13   §2: 14   §3: 18   §4: 20   §5: 22   §6: 13     total: 100

Within a parent section we distribute proportionally across populated subsections.

Reproducible: random.seed(42). Same input → same 200 IDs assigned to same pools.
Atomic: write to .tmp then os.replace().
"""
from __future__ import annotations

import argparse
import json
import os
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
QUIZ_FILE = DATA_DIR / "quizzes.jsonl"
TMP_FILE = QUIZ_FILE.with_suffix(".jsonl.tmp")

PER_POOL_TARGETS = {"§1": 13, "§2": 14, "§3": 18, "§4": 20, "§5": 22, "§6": 13}
SEED = 42
POOLS = ["mock1-pool", "mock2-pool"]


def load_records() -> list[dict]:
    with QUIZ_FILE.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def atomic_write(records: list[dict]) -> None:
    with TMP_FILE.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(TMP_FILE, QUIZ_FILE)


def split_target(parent_target: int, sub_counts: dict[str, int]) -> dict[str, int]:
    """Distribute parent's per-pool target across populated subsections, proportional to subsection size.

    Each subsection target is capped by half the available pool (floor(pool/2)) so that two pools can
    be drawn disjoint. We use floor + redistribute remainder by largest fractional remainders.
    """
    total = sum(sub_counts.values())
    if total == 0:
        return {}
    # Cap each subsection's per-pool target by floor(available/2) so both pools fit disjointly
    raw = {sec: parent_target * n / total for sec, n in sub_counts.items()}
    floors = {sec: int(v) for sec, v in raw.items()}
    remaining = parent_target - sum(floors.values())
    # Distribute remainders by largest fractional part (deterministic tiebreak by section name)
    fractional = sorted(
        ((raw[sec] - floors[sec], sec) for sec in raw),
        key=lambda x: (-x[0], x[1]),
    )
    for _, sec in fractional[:remaining]:
        floors[sec] += 1
    # Cap at floor(available / 2) so both pools fit disjointly
    capped = {}
    leftover = 0
    for sec, want in floors.items():
        avail = sub_counts[sec]
        cap = avail // 2
        take = min(want, cap)
        capped[sec] = take
        leftover += want - take
    if leftover > 0:
        # Push leftover to other subsections that still have headroom
        for sec in sorted(capped, key=lambda s: -(sub_counts[s] // 2 - capped[s])):
            headroom = sub_counts[sec] // 2 - capped[sec]
            if headroom <= 0:
                continue
            grab = min(headroom, leftover)
            capped[sec] += grab
            leftover -= grab
            if leftover == 0:
                break
    return capped


def assign_pools(
    records: list[dict],
) -> tuple[dict[str, list[str]], dict[str, dict[str, int]]]:
    """Return mapping pool_name → list[question_id_str] and per-pool per-subsection counts."""
    random.seed(SEED)

    # Group by parent section (§1..§6) → subsection (§1.1, §1.2, ...) → list of records
    by_parent: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for r in records:
        sec = r.get("exam_section")
        if not sec:
            continue
        parent = sec.split(".")[0]
        by_parent[parent][sec].append(r)

    pools: dict[str, list[str]] = {p: [] for p in POOLS}
    breakdown: dict[str, dict[str, int]] = {p: Counter() for p in POOLS}

    for parent, target in PER_POOL_TARGETS.items():
        sub_groups = by_parent.get(parent, {})
        if not sub_groups:
            print(f"  WARNING: no records for {parent}", file=sys.stderr)
            continue
        sub_counts = {sec: len(rs) for sec, rs in sub_groups.items()}
        per_sub = split_target(target, sub_counts)
        for sec, take in per_sub.items():
            if take == 0:
                continue
            shuffled = sub_groups[sec][:]
            random.shuffle(shuffled)
            picked = shuffled[: take * 2]  # 2x take for two disjoint pools
            mock1 = picked[:take]
            mock2 = picked[take : take * 2]
            for r in mock1:
                pools["mock1-pool"].append(r["id"])
                breakdown["mock1-pool"][sec] += 1
            for r in mock2:
                pools["mock2-pool"].append(r["id"])
                breakdown["mock2-pool"][sec] += 1
    return pools, breakdown


def apply_pools(records: list[dict], pools: dict[str, list[int]], reset: bool) -> int:
    id_to_pool: dict[int, str] = {}
    for pool_name, ids in pools.items():
        for qid in ids:
            id_to_pool[qid] = pool_name
    set_count = 0
    for r in records:
        if reset:
            r["mock_pool"] = None
        if r.get("mock_pool"):
            continue  # idempotent: don't reassign
        if r["id"] in id_to_pool:
            r["mock_pool"] = [id_to_pool[r["id"]]]
            set_count += 1
    return set_count


def main() -> int:
    parser = argparse.ArgumentParser(description="Tag mock pools (Phase 2 Move 4)")
    parser.add_argument("--dry-run", action="store_true", help="preview, do not write")
    parser.add_argument("--reset", action="store_true", help="clear all mock_pool tags before re-sampling")
    args = parser.parse_args()

    if not QUIZ_FILE.exists():
        print(f"ERROR: {QUIZ_FILE} not found", file=sys.stderr)
        return 1

    records = load_records()
    pools, breakdown = assign_pools(records)

    print("Pool sizes:")
    for p in POOLS:
        print(f"  {p}: {len(pools[p])}")
    print()
    print("Per-pool, per-subsection breakdown:")
    for p in POOLS:
        print(f"  {p}:")
        for sec in sorted(breakdown[p]):
            print(f"    {sec}  {breakdown[p][sec]:3d}")
    print()
    overlap = set(pools["mock1-pool"]) & set(pools["mock2-pool"])
    print(f"mock1 ∩ mock2 overlap: {len(overlap)} (expected 0)")

    if args.dry_run:
        print("\n[dry-run; no write]")
        return 0

    set_count = apply_pools(records, pools, reset=args.reset)
    atomic_write(records)
    print(f"\nWrote {set_count} new mock_pool assignments to {QUIZ_FILE.name}.")

    # Verification: post-write state
    records_after = load_records()
    pool_counts = Counter()
    for r in records_after:
        for tag in r.get("mock_pool") or []:
            pool_counts[tag] += 1
    none_count = sum(1 for r in records_after if not r.get("mock_pool"))
    print(f"Post-write: mock1-pool={pool_counts['mock1-pool']}, mock2-pool={pool_counts['mock2-pool']}, normal-mode={none_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
