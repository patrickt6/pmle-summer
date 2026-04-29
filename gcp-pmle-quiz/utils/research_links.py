"""URL → display label for the public sources cited across the app.

The plan and weeks data once pointed at local ``research/*.md`` files;
they now point at the canonical public sources those files summarize
(Google Cloud docs, Skills Boost path, etc.). This module gives pages a
consistent label to show when rendering one of those URLs as a link.
"""

from __future__ import annotations

# Order: docs cards first, then anchors used by Weekly Overview.
RESEARCH_LABELS: dict[str, str] = {
    "https://docs.cloud.google.com/vertex-ai/docs/model-monitoring/overview":
        "Vertex AI Model Monitoring overview",
    "https://docs.cloud.google.com/vertex-ai/docs/featurestore/latest/overview":
        "Vertex AI Feature Store overview",
    "https://docs.cloud.google.com/vertex-ai/docs/training/hyperparameter-tuning-overview":
        "Vertex AI hyperparameter tuning overview",
    "https://docs.cloud.google.com/vertex-ai/docs/experiments/intro-vertex-ai-experiments":
        "Vertex AI Experiments intro",
    "https://ai.google/principles/":
        "Google AI Principles",
    "https://docs.cloud.google.com/vertex-ai/docs/predictions/overview":
        "Vertex AI predictions overview",
    "https://docs.cloud.google.com/iam/docs/overview":
        "IAM overview",
    "https://docs.cloud.google.com/bigquery/docs/bqml-introduction":
        "BigQuery ML introduction",
    "https://docs.cloud.google.com/vertex-ai/docs/training/configure-compute":
        "Vertex AI training compute config",
    "https://docs.cloud.google.com/vertex-ai/docs/pipelines/introduction":
        "Vertex AI Pipelines introduction",
    "https://cloud.google.com/products/agent-builder":
        "Gemini Enterprise Agent Platform",
    "https://medium.com/@andy_p_/how-i-passed-the-google-cloud-professional-machine-learning-engineer-pmle-exam-in-30-days-and-so-ac9bc1e887d4":
        "Andrei Paraschiv's PMLE pass writeup (Feb 2026)",
    "https://www.skills.google/paths/17":
        "Google Skills ML Engineer learning path",
    "https://github.com/AndyTheFactory/gcp-pmle-quiz":
        "AndyTheFactory gcp-pmle-quiz repo",
}


def label_for(url: str) -> str:
    """Return the curated label for ``url``, or the URL itself as fallback."""
    return RESEARCH_LABELS.get(url, url)
