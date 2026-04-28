"""Phase 6a — One-time migration from shared progress to per-profile profiles.

Idempotent: re-running does nothing once Patrick has progress.

  data/progress.json          → data/profiles/patrick/progress.json
  data/profiles/matt/         → initialized empty
  data/progress.pre-phase6.json (legacy backup)
  data/app_settings.json      (current_profile = patrick + blueprint weights)

Usage::

    cd gcp-pmle-quiz
    uv run python scripts/migrate_to_profiles.py
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

_APP_DIR = Path(__file__).resolve().parent.parent  # gcp-pmle-quiz/
sys.path.insert(0, str(_APP_DIR))

from utils import DATA_DIR  # noqa: E402
from utils.profiles import (  # noqa: E402
    ensure_default_profiles,
    load_app_settings,
    profile_path,
    save_app_settings,
)

LEGACY_PROGRESS = DATA_DIR / "progress.json"
LEGACY_BACKUP = DATA_DIR / "progress.pre-phase6.json"


def main() -> int:
    print(f"Phase 6a migration → {DATA_DIR / 'profiles'}/")

    # 1. Materialize Patrick + Matt profile shells (idempotent).
    ensure_default_profiles()
    print("✓ default profiles ensured (patrick, matt)")

    patrick_progress = profile_path("progress.json", "patrick")
    try:
        patrick_existing = json.loads(patrick_progress.read_text(encoding="utf-8") or "{}")
    except json.JSONDecodeError:
        patrick_existing = {}

    # 2. Copy legacy progress to Patrick if Patrick is empty.
    if patrick_existing:
        print(
            f"⚠  patrick already has {len(patrick_existing)} progress entries — "
            "leaving them alone"
        )
    elif LEGACY_PROGRESS.exists():
        legacy = json.loads(LEGACY_PROGRESS.read_text(encoding="utf-8") or "{}")
        patrick_progress.write_text(
            json.dumps(legacy, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"✓ migrated {len(legacy)} progress entries → patrick")

        if not LEGACY_BACKUP.exists():
            shutil.copy(LEGACY_PROGRESS, LEGACY_BACKUP)
            print(f"✓ legacy file backed up to {LEGACY_BACKUP.name}")
    else:
        print("✓ no legacy progress.json found; patrick starts fresh")

    # 3. Touch app settings so blueprint weights / current_profile materialize.
    settings = load_app_settings()
    save_app_settings(settings)
    print(f"✓ app_settings.json ready (current_profile={settings.current_profile})")

    print(
        "\nDone. The Streamlit app now reads progress from "
        "data/profiles/<active>/progress.json."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
