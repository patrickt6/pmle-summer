"""Tests for utils.profiles — Phase 6a profile management."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import utils.profiles as profiles_mod
from utils.profiles import (
    DEFAULT_BLUEPRINT_WEIGHTS,
    DEFAULT_PROFILES,
    AppSettings,
    Profile,
    create_profile,
    current_profile,
    ensure_default_profiles,
    get_current_profile_name,
    get_profile,
    list_profiles,
    load_app_settings,
    profile_dir,
    profile_path,
    save_app_settings,
    set_current_profile,
    update_profile,
)


@pytest.fixture
def tmp_profiles(tmp_path: Path, monkeypatch):
    """Redirect profiles dir + app settings to a tmp path."""
    profiles_dir = tmp_path / "profiles"
    settings_file = tmp_path / "app_settings.json"
    monkeypatch.setattr(profiles_mod, "PROFILES_DIR", profiles_dir)
    monkeypatch.setattr(profiles_mod, "APP_SETTINGS_FILE", settings_file)
    monkeypatch.setattr(profiles_mod, "DATA_DIR", tmp_path)
    return tmp_path


# ---------- Profile model ----------


def test_default_profiles_have_required_fields():
    for raw in DEFAULT_PROFILES:
        p = Profile.model_validate(raw)
        assert p.name
        assert p.display_name
        assert p.study_start_date
        assert p.exam_target_date
        assert p.color.startswith("#")


def test_default_profiles_include_patrick_and_matt():
    names = {raw["name"] for raw in DEFAULT_PROFILES}
    assert names == {"patrick", "matt"}


# ---------- Default seeding ----------


def test_ensure_default_creates_two(tmp_profiles):
    ensure_default_profiles()
    names = {p.name for p in list_profiles()}
    assert names == {"patrick", "matt"}


def test_ensure_default_idempotent(tmp_profiles):
    ensure_default_profiles()
    ensure_default_profiles()
    assert len(list_profiles()) == 2


def test_profile_skeleton_files_created(tmp_profiles):
    ensure_default_profiles()
    pdir = profile_dir("patrick")
    for fname in ("profile.json", "progress.json", "journal.json", "srs.json", "cursor.json"):
        assert (pdir / fname).exists(), f"missing {fname}"


def test_progress_skeleton_is_empty_dict(tmp_profiles):
    ensure_default_profiles()
    progress_file = profile_path("progress.json", "patrick")
    assert json.loads(progress_file.read_text()) == {}


def test_journal_skeleton_is_empty_list(tmp_profiles):
    ensure_default_profiles()
    journal_file = profile_path("journal.json", "patrick")
    assert json.loads(journal_file.read_text()) == []


def test_srs_skeleton_is_empty_dict(tmp_profiles):
    ensure_default_profiles()
    srs_file = profile_path("srs.json", "patrick")
    assert json.loads(srs_file.read_text()) == {}


def test_cursor_skeleton_has_required_fields(tmp_profiles):
    ensure_default_profiles()
    cursor_file = profile_path("cursor.json", "patrick")
    cursor = json.loads(cursor_file.read_text())
    assert cursor["completed_days"] == []
    assert cursor["skipped_days"] == []
    assert cursor["manual_override_day"] is None
    assert "last_active" in cursor


# ---------- Lookup ----------


def test_list_profiles_empty_when_dir_missing(tmp_profiles):
    assert list_profiles() == []


def test_get_profile_finds_match(tmp_profiles):
    ensure_default_profiles()
    p = get_profile("patrick")
    assert p is not None
    assert p.display_name == "Patrick"


def test_get_profile_missing_returns_none(tmp_profiles):
    ensure_default_profiles()
    assert get_profile("nobody") is None


def test_current_profile_materializes_defaults(tmp_profiles):
    """First call with no profiles on disk should seed defaults instead of crashing."""
    p = current_profile()
    assert p.name in {"patrick", "matt"}
    assert len(list_profiles()) == 2


def test_current_profile_falls_back_when_setting_stale(tmp_profiles):
    ensure_default_profiles()
    # Bypass set_current_profile validation to install a stale name.
    s = load_app_settings()
    s.current_profile = "ghost"
    save_app_settings(s)
    p = current_profile()
    assert p.name in {"patrick", "matt"}


# ---------- Create / switch ----------


def test_create_profile_validates_name(tmp_profiles):
    bad = Profile(
        name="Bad-Name!",
        display_name="Bad",
        study_start_date="2026-04-27",
        exam_target_date="2026-07-26",
    )
    with pytest.raises(ValueError):
        create_profile(bad)


def test_create_profile_persists(tmp_profiles):
    ensure_default_profiles()
    new = Profile(
        name="alice",
        display_name="Alice",
        color="#FBBC05",
        study_start_date="2026-05-01",
        exam_target_date="2026-08-01",
    )
    create_profile(new)
    assert get_profile("alice") is not None
    assert (profile_dir("alice") / "progress.json").exists()


def test_profile_path_resolves_under_current_profile(tmp_profiles):
    ensure_default_profiles()
    set_current_profile("patrick")
    assert profile_path("progress.json").parent.name == "patrick"
    set_current_profile("matt")
    assert profile_path("progress.json").parent.name == "matt"


def test_set_current_profile_invalid_raises(tmp_profiles):
    ensure_default_profiles()
    with pytest.raises(ValueError):
        set_current_profile("nobody")


def test_get_current_profile_name_after_switch(tmp_profiles):
    ensure_default_profiles()
    set_current_profile("matt")
    assert get_current_profile_name() == "matt"


# ---------- App settings ----------


def test_app_settings_round_trip(tmp_profiles):
    settings = load_app_settings()
    assert settings.current_profile == "patrick"
    assert settings.blueprint_weights["§5"] == 0.22
    settings.passing_target = 0.85
    save_app_settings(settings)
    reloaded = load_app_settings()
    assert reloaded.passing_target == 0.85


def test_blueprint_weights_sum_to_one():
    s = AppSettings()
    total = sum(s.blueprint_weights.values())
    assert abs(total - 1.0) < 1e-9


def test_blueprint_weights_match_v31():
    """Blueprint % weights must mirror the v3.1 exam guide (§5 highest at 22%)."""
    weights = DEFAULT_BLUEPRINT_WEIGHTS
    assert weights["§5"] == 0.22
    assert weights["§4"] == 0.20
    assert weights["§3"] == 0.18
    assert weights["§2"] == 0.14
    assert weights["§1"] == weights["§6"] == 0.13


# ---------- Atomic writes ----------


def test_no_partial_files_left_after_save(tmp_profiles):
    save_app_settings(AppSettings(passing_target=0.81))
    tmp = profiles_mod.APP_SETTINGS_FILE.with_suffix(
        profiles_mod.APP_SETTINGS_FILE.suffix + ".tmp"
    )
    assert not tmp.exists()


# ---------- Integration with utils.load_progress ----------


def test_utils_load_progress_uses_active_profile(tmp_profiles):
    """utils.load_progress must read from data/profiles/<current>/progress.json."""
    import utils as utils_mod

    ensure_default_profiles()
    set_current_profile("patrick")
    profile_path("progress.json", "patrick").write_text(
        '{"42": true, "100": false}', encoding="utf-8"
    )
    progress = utils_mod.load_progress()
    assert progress == {42: True, 100: False}

    # Switch profiles → utils.load_progress reads the other file.
    set_current_profile("matt")
    progress = utils_mod.load_progress()
    assert progress == {}


def test_utils_save_progress_writes_to_active_profile(tmp_profiles):
    import utils as utils_mod

    ensure_default_profiles()
    set_current_profile("matt")
    utils_mod.save_progress({1: True, 2: False})
    matt_data = json.loads(
        profile_path("progress.json", "matt").read_text(encoding="utf-8")
    )
    assert matt_data == {"1": True, "2": False}

    # Patrick should be untouched.
    patrick_data = json.loads(
        profile_path("progress.json", "patrick").read_text(encoding="utf-8")
    )
    assert patrick_data == {}


def test_update_profile_persists_dates(tmp_profiles):
    ensure_default_profiles()
    updated = update_profile(
        "patrick",
        study_start_date="2026-05-04",
        exam_target_date="2026-08-02",
    )
    assert updated.study_start_date == "2026-05-04"
    assert updated.exam_target_date == "2026-08-02"
    reloaded = get_profile("patrick")
    assert reloaded is not None
    assert reloaded.study_start_date == "2026-05-04"
    assert reloaded.exam_target_date == "2026-08-02"


def test_update_profile_partial(tmp_profiles):
    ensure_default_profiles()
    update_profile("matt", display_name="Matthew the Magnificent")
    p = get_profile("matt")
    assert p is not None
    assert p.display_name == "Matthew the Magnificent"
    # study_start should be unchanged
    assert p.study_start_date == "2026-04-27"


def test_update_profile_missing_raises(tmp_profiles):
    ensure_default_profiles()
    with pytest.raises(ValueError):
        update_profile("ghost", study_start_date="2026-05-04")


def test_utils_reset_progress_clears_only_active_profile(tmp_profiles):
    import utils as utils_mod

    ensure_default_profiles()
    profile_path("progress.json", "patrick").write_text('{"1": true}', encoding="utf-8")
    profile_path("progress.json", "matt").write_text('{"2": false}', encoding="utf-8")

    set_current_profile("patrick")
    utils_mod.reset_progress()

    assert json.loads(profile_path("progress.json", "patrick").read_text()) == {}
    assert json.loads(profile_path("progress.json", "matt").read_text()) == {"2": False}
