"""One-shot rewrite: replace all `research/*.md`, `study_plan.md`, and
`CLAUDE.md` references in the Streamlit app's user-facing surface with
canonical public URLs (Google Cloud docs, Skills Boost path, etc.) so
the app is useful for someone without access to the local repo.

Touches:
- ``study_plan.md`` (source of truth for the Plan page)
- ``data/weeks.json``, ``data/knowledge.json``, ``data/labs.json``
- selected Streamlit pages with hard-coded `research/...md` text

After running this, also run::

    uv run python scripts/parse_study_plan.py

to regenerate ``data/study_plan.json`` from the rewritten ``study_plan.md``.

Idempotent: running twice is a no-op (already-replaced URLs no longer match).
"""

from __future__ import annotations

import json
import re
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = APP_DIR.parent

# (canonical URL, display label) per research file. Picked from the
# primary citation in each file's opening sections.
URL_MAP: dict[str, tuple[str, str]] = {
    "research/concepts/skew-vs-drift.md": (
        "https://docs.cloud.google.com/vertex-ai/docs/model-monitoring/overview",
        "Vertex AI Model Monitoring overview",
    ),
    "research/concepts/feature-store.md": (
        "https://docs.cloud.google.com/vertex-ai/docs/featurestore/latest/overview",
        "Vertex AI Feature Store overview",
    ),
    "research/concepts/hyperparameter-tuning.md": (
        "https://docs.cloud.google.com/vertex-ai/docs/training/hyperparameter-tuning-overview",
        "Vertex AI hyperparameter tuning overview",
    ),
    "research/concepts/metadata-lineage.md": (
        "https://docs.cloud.google.com/vertex-ai/docs/experiments/intro-vertex-ai-experiments",
        "Vertex AI Experiments intro",
    ),
    "research/concepts/responsible-ai-security.md": (
        "https://ai.google/principles/",
        "Google AI Principles",
    ),
    "research/concepts/serving-deep-dive.md": (
        "https://docs.cloud.google.com/vertex-ai/docs/predictions/overview",
        "Vertex AI predictions overview",
    ),
    "research/concepts/iam-for-ml.md": (
        "https://docs.cloud.google.com/iam/docs/overview",
        "IAM overview",
    ),
    "research/decision-trees/tabular-modeling.md": (
        "https://docs.cloud.google.com/bigquery/docs/bqml-introduction",
        "BigQuery ML introduction",
    ),
    "research/decision-trees/compute-selection.md": (
        "https://docs.cloud.google.com/vertex-ai/docs/training/configure-compute",
        "Vertex AI training compute config",
    ),
    "research/decision-trees/pipelines-comparison.md": (
        "https://docs.cloud.google.com/vertex-ai/docs/pipelines/introduction",
        "Vertex AI Pipelines introduction",
    ),
    "research/genai/vertex-ai-overview.md": (
        "https://cloud.google.com/products/agent-builder",
        "Gemini Enterprise Agent Platform",
    ),
    "research/anecdotes/recent-passers.md": (
        "https://medium.com/@andy_p_/how-i-passed-the-google-cloud-professional-machine-learning-engineer-pmle-exam-in-30-days-and-so-ac9bc1e887d4",
        "Andrei Paraschiv's PMLE pass writeup (Feb 2026)",
    ),
    "research/labs/skills-boost-path.md": (
        "https://www.skills.google/paths/17",
        "Google Skills ML Engineer learning path",
    ),
    "research/question-banks/audit.md": (
        "https://github.com/AndyTheFactory/gcp-pmle-quiz",
        "AndyTheFactory gcp-pmle-quiz repo",
    ),
}

# Path basename → canonical URL+label, for backtick-wrapped short refs
# like "`tabular-modeling.md`" that elide the directory.
BASENAME_MAP: dict[str, tuple[str, str]] = {
    Path(p).name: v for p, v in URL_MAP.items()
}

MD_LINK_RE = re.compile(r"\[([^\]]+)\]\((research/[^)]+\.md)\)")
BACKTICK_LINK_RE = re.compile(r"\[`([^`]+\.md)`\]\((research/[^)]+\.md)\)")


def _rewrite_md_link(match: re.Match[str]) -> str:
    """Markdown link `[label](research/foo.md)` → `[label-or-canonical](url)`.

    Strategy: if the label looks like a filename (ends in ``.md``) or matches
    the path, swap in the canonical label. Otherwise, keep the label and only
    swap the URL.
    """
    label = match.group(1)
    path = match.group(2)
    entry = URL_MAP.get(path)
    if not entry:
        return match.group(0)
    url, canonical = entry
    label_stripped = label.strip("`")
    if label_stripped.endswith(".md") or label_stripped == path:
        return f"[{canonical}]({url})"
    return f"[{label}]({url})"


def _rewrite_text(text: str) -> str:
    text = MD_LINK_RE.sub(_rewrite_md_link, text)
    # Backtick-only file refs like `` `research/foo.md` `` (not inside an md link)
    # → `[canonical-label](url)`.
    def _backtick_sub(m: re.Match[str]) -> str:
        path = m.group(1)
        if path in URL_MAP:
            url, label = URL_MAP[path]
            return f"[{label}]({url})"
        return m.group(0)

    text = re.sub(r"`(research/[^`]+\.md)`", _backtick_sub, text)
    # Bare `path/file.md` not preceded by ( or ` (rare but in plain prose).
    def _bare_sub(m: re.Match[str]) -> str:
        path = m.group(0)
        if path in URL_MAP:
            url, label = URL_MAP[path]
            return f"[{label}]({url})"
        return path

    text = re.sub(r"(?<![(`/])research/[A-Za-z0-9_\-/]+\.md", _bare_sub, text)
    # Backticked basename-only refs (e.g., `tabular-modeling.md`).
    def _basename_sub(m: re.Match[str]) -> str:
        name = m.group(1)
        if name in BASENAME_MAP:
            url, label = BASENAME_MAP[name]
            return f"[{label}]({url})"
        return m.group(0)

    text = re.sub(r"`([A-Za-z0-9_\-]+\.md)`", _basename_sub, text)
    return text


def _rewrite_json_paths(obj):
    """In-place rewrite of any JSON value that equals a known research path."""
    if isinstance(obj, dict):
        return {k: _rewrite_json_paths(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_rewrite_json_paths(x) for x in obj]
    if isinstance(obj, str):
        if obj in URL_MAP:
            return URL_MAP[obj][0]
        return _rewrite_text(obj)
    return obj


def rewrite_study_plan_md() -> int:
    md = REPO_ROOT / "study_plan.md"
    text = md.read_text(encoding="utf-8")
    new_text = _rewrite_text(text)
    if new_text != text:
        md.write_text(new_text, encoding="utf-8")
    return new_text.count("https://") - text.count("https://")


def rewrite_data_jsons() -> dict[str, int]:
    out: dict[str, int] = {}
    for name in ("weeks.json", "knowledge.json", "labs.json", "study_plan.json"):
        path = APP_DIR / "data" / name
        if not path.exists():
            continue
        before = path.read_text(encoding="utf-8")
        data = json.loads(before)
        new_data = _rewrite_json_paths(data)
        new_text = json.dumps(new_data, indent=2, ensure_ascii=False) + "\n"
        if new_text != before:
            path.write_text(new_text, encoding="utf-8")
        out[name] = new_text.count("https://") - before.count("https://")
    return out


PAGE_FILES = [
    "pages/0_📍_Today.py",
    "pages/7_📚_Resources.py",
    "pages/8_📝_Study_Guide.py",
    "pages/11_🕸_Knowledge_Graph.py",
    "pages/13_🧪_Labs.py",
]


def rewrite_pages() -> dict[str, int]:
    out: dict[str, int] = {}
    for rel in PAGE_FILES:
        path = APP_DIR / rel
        if not path.exists():
            continue
        before = path.read_text(encoding="utf-8")
        new_text = _rewrite_text(before)
        if new_text != before:
            path.write_text(new_text, encoding="utf-8")
        out[rel] = new_text.count("https://") - before.count("https://")
    return out


def main() -> None:
    n_md = rewrite_study_plan_md()
    print(f"study_plan.md: +{n_md} https links")
    for name, n in rewrite_data_jsons().items():
        print(f"data/{name}: +{n} https links")
    for rel, n in rewrite_pages().items():
        print(f"{rel}: +{n} https links")


if __name__ == "__main__":
    main()
