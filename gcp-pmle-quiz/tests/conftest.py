"""Shared pytest fixtures.

Adds the gcp-pmle-quiz/ root to sys.path so tests can `import models.questions`,
`import utils.weekly`, etc. without packaging the app.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

APP_ROOT = Path(__file__).resolve().parent.parent
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))


@pytest.fixture
def app_root() -> Path:
    return APP_ROOT
