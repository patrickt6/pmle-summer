import json
import logging
import os
from pathlib import Path

import streamlit as st

from models.questions import Question

_APP_DIR = Path(__file__).resolve().parent.parent  # gcp-pmle-quiz/
DATA_DIR = _APP_DIR / "data"
QUIZ_FILE = DATA_DIR / "quizzes.jsonl"

# Legacy per-clone progress file. Phase 6a routes progress through the
# active profile (data/profiles/<name>/progress.json) instead — see
# `utils.profiles`. The legacy path stays as a fallback for code paths
# that run before profiles have been initialized (fresh tests, first
# launch on a clone where the migration hasn't been run yet).
LEGACY_PROGRESS_FILE = DATA_DIR / "progress.json"

logger = logging.getLogger(__name__)


def _current_progress_file() -> Path:
    """Resolve the active profile's progress.json.

    Lazily imports `utils.profiles` to avoid a circular import at module
    load time. Falls back to the legacy data/progress.json if no
    profiles have been materialized yet (so the app keeps working on
    pre-migration clones).
    """
    from utils.profiles import list_profiles, profile_path

    if list_profiles():
        return profile_path("progress.json")
    return LEGACY_PROGRESS_FILE


def load_quizzes(progress: dict[int, bool]) -> tuple[list[Question], list[Question], list[Question]]:
    quizzes_answered_correctly: list[Question] = []
    quizzes_not_answered: list[Question] = []
    quizzes_answered_incorrectly: list[Question] = []

    if not QUIZ_FILE.exists():
        return quizzes_answered_incorrectly, quizzes_not_answered, quizzes_answered_correctly

    with QUIZ_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            try:
                question = Question.parse_raw(line)
                if question.id in progress:
                    if progress[question.id]:
                        quizzes_answered_correctly.append(question)
                    else:
                        quizzes_answered_incorrectly.append(question)
                else:
                    quizzes_not_answered.append(question)
            except Exception as e:
                logger.error(f"Failed to parse question line: {e}")
                continue
    return quizzes_answered_incorrectly, quizzes_not_answered, quizzes_answered_correctly


def load_progress() -> dict[int, bool]:
    pfile = _current_progress_file()
    if not pfile.exists():
        return {}
    try:
        with pfile.open("r", encoding="utf-8") as f:
            progress = json.load(f)
        return {int(k): v for k, v in (progress or {}).items()}
    except Exception:
        return {}


def save_progress(progress: dict[int, bool]) -> None:
    pfile = _current_progress_file()
    pfile.parent.mkdir(parents=True, exist_ok=True)
    tmp = pfile.with_suffix(pfile.suffix + ".tmp")
    tmp.write_text(
        json.dumps(progress, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    os.replace(tmp, pfile)


def compute_stats(round_progress):
    asked = len(round_progress)
    correct = sum(1 for v in round_progress.values() if v)
    wrong = sum(1 for v in round_progress.values() if not v)
    pct = (correct / asked * 100) if asked else 0.0
    return asked, correct, wrong, pct


def reset_progress() -> None:
    pfile = _current_progress_file()
    if pfile.exists():
        # Keep the file at the per-profile path; clear contents.
        pfile.write_text("{}", encoding="utf-8")


def set_css_style(css_path: Path | None = None):
    if css_path is None:
        css_path = _APP_DIR / "style.css"
    elif not css_path.is_absolute() and not css_path.exists():
        # Existing pages pass Path("style.css") relative to their CWD,
        # which breaks on Streamlit Cloud where CWD = repo root. Resolve
        # against the app dir as a fallback.
        candidate = _APP_DIR / css_path
        if candidate.exists():
            css_path = candidate
    if not css_path.exists():
        return
    with css_path.open("r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
