"""Shared pytest fixtures for the Sprechen test suite."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

# Make the project root importable when running `pytest` from any cwd.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Provide harmless defaults so Settings() never explodes during import.
os.environ.setdefault("GROQ_API_KEY", "test-groq-key")


@pytest.fixture
def fake_audio_bytes() -> bytes:
    return b"FAKE-AUDIO-BYTES-1234567890"


@pytest.fixture
def reference_text() -> str:
    return "Guten Morgen, ich hätte gerne ein Brötchen."
