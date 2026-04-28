"""Phase 6a — Multi-profile support.

Each profile (Patrick, Matt, …) gets its own data directory under
``data/profiles/<name>/``:

  - ``profile.json``   metadata (display name, color, study/exam dates)
  - ``progress.json``  per-question correct/wrong (Phase 6a)
  - ``cursor.json``    today/plan position (Phase 6a)
  - ``journal.json``   wrong-answer journal (Phase 6b)
  - ``srs.json``       Leitner box state (Phase 6b)

Shared across profiles (``data/...``):

  - ``lab_progress.json``      labs are co-authored, not personal
  - ``week_quiz_results.json`` history of timed week-quizzes (any profile)

App-level settings live in ``data/app_settings.json`` and store the
current profile name plus the v3.1 blueprint weights driving the
projected-score dashboard.

The personal files (``progress``, ``journal``, ``srs``, ``cursor``) and
``app_settings.json`` are gitignored; ``profile.json`` is tracked so a
fresh clone has the same profile shells.
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field

from utils import DATA_DIR

PROFILES_DIR = DATA_DIR / "profiles"
APP_SETTINGS_FILE = DATA_DIR / "app_settings.json"

DEFAULT_BLUEPRINT_WEIGHTS: dict[str, float] = {
    "§1": 0.13,
    "§2": 0.14,
    "§3": 0.18,
    "§4": 0.20,
    "§5": 0.22,
    "§6": 0.13,
}

DEFAULT_PROFILES: list[dict] = [
    {
        "name": "patrick",
        "display_name": "Patrick",
        "color": "#3B82F6",
        "study_start_date": "2026-04-27",
        "exam_target_date": "2026-07-26",
    },
    {
        "name": "matt",
        "display_name": "Matty Boy",
        "color": "#EA4335",
        "study_start_date": "2026-04-27",
        "exam_target_date": "2026-07-26",
    },
]

NAME_PATTERN = re.compile(r"^[a-z0-9_]+$")


class Profile(BaseModel):
    name: str
    display_name: str
    color: str = "#3B82F6"
    study_start_date: str  # YYYY-MM-DD
    exam_target_date: str  # YYYY-MM-DD
    created_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class AppSettings(BaseModel):
    current_profile: str = "patrick"
    blueprint_weights: dict[str, float] = Field(
        default_factory=lambda: dict(DEFAULT_BLUEPRINT_WEIGHTS)
    )
    passing_target: float = 0.80
    high_score_target: float = 0.85


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    os.replace(tmp, path)


# ---------- App settings ----------


def _ensure_app_settings() -> None:
    if APP_SETTINGS_FILE.exists():
        return
    _atomic_write(
        APP_SETTINGS_FILE,
        json.dumps(AppSettings().model_dump(), indent=2, ensure_ascii=False),
    )


def load_app_settings() -> AppSettings:
    _ensure_app_settings()
    with APP_SETTINGS_FILE.open("r", encoding="utf-8") as f:
        return AppSettings.model_validate(json.load(f))


def save_app_settings(settings: AppSettings) -> None:
    _atomic_write(
        APP_SETTINGS_FILE,
        json.dumps(settings.model_dump(), indent=2, ensure_ascii=False),
    )


def get_current_profile_name() -> str:
    return load_app_settings().current_profile


def set_current_profile(name: str) -> None:
    if get_profile(name) is None:
        raise ValueError(f"Profile '{name}' does not exist")
    settings = load_app_settings()
    settings.current_profile = name
    save_app_settings(settings)


# ---------- Profile management ----------


def list_profiles() -> list[Profile]:
    if not PROFILES_DIR.exists():
        return []
    out: list[Profile] = []
    for child in sorted(PROFILES_DIR.iterdir()):
        if not child.is_dir():
            continue
        pfile = child / "profile.json"
        if not pfile.exists():
            continue
        try:
            with pfile.open("r", encoding="utf-8") as f:
                out.append(Profile.model_validate(json.load(f)))
        except Exception:
            continue
    return out


def get_profile(name: str) -> Profile | None:
    for p in list_profiles():
        if p.name == name:
            return p
    return None


def current_profile() -> Profile:
    """Return the active profile, materializing defaults on first run."""
    profiles = list_profiles()
    if not profiles:
        ensure_default_profiles()
        profiles = list_profiles()
    name = get_current_profile_name()
    for p in profiles:
        if p.name == name:
            return p
    # Stale setting (deleted profile, etc.) — fall back to first available.
    return profiles[0]


def profile_dir(name: str | None = None) -> Path:
    name = name or get_current_profile_name()
    return PROFILES_DIR / name


def profile_path(filename: str, profile_name: str | None = None) -> Path:
    return profile_dir(profile_name) / filename


def _initialize_profile_files(pdir: Path) -> None:
    pdir.mkdir(parents=True, exist_ok=True)
    skeletons: dict[str, str] = {
        "progress.json": "{}",
        "journal.json": "[]",
        "srs.json": "{}",
        "cursor.json": json.dumps(
            {
                "completed_days": [],
                "skipped_days": [],
                "manual_override_day": None,
                "last_active": datetime.now(timezone.utc).isoformat(),
            },
            indent=2,
        ),
    }
    for fname, content in skeletons.items():
        target = pdir / fname
        if not target.exists():
            target.write_text(content, encoding="utf-8")


def create_profile(profile: Profile) -> Profile:
    if not NAME_PATTERN.match(profile.name):
        raise ValueError(
            f"Invalid profile name '{profile.name}': must match {NAME_PATTERN.pattern}"
        )
    pdir = profile_dir(profile.name)
    pdir.mkdir(parents=True, exist_ok=True)
    pfile = pdir / "profile.json"
    pfile.write_text(
        json.dumps(profile.model_dump(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    _initialize_profile_files(pdir)
    return profile


def ensure_default_profiles() -> None:
    """Idempotent: create the canonical Patrick + Matt profiles if absent."""
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    for raw in DEFAULT_PROFILES:
        if get_profile(raw["name"]) is None:
            create_profile(Profile.model_validate(raw))


def update_profile(name: str, **fields) -> Profile:
    """Merge fields into ``data/profiles/<name>/profile.json`` and persist.

    Validates the merged record against the :class:`Profile` schema. Used
    by the sidebar settings expander to let the user edit the study and
    exam dates without hand-editing JSON.
    """
    existing = get_profile(name)
    if existing is None:
        raise ValueError(f"Profile '{name}' does not exist")
    data = existing.model_dump()
    data.update(fields)
    updated = Profile.model_validate(data)
    pfile = profile_dir(name) / "profile.json"
    _atomic_write(
        pfile,
        json.dumps(updated.model_dump(), indent=2, ensure_ascii=False),
    )
    return updated
