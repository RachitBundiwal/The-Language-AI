"""Tests for services.stt_service."""
from __future__ import annotations

import os
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from services.stt_service import STTService, get_stt_service


def _fake_groq_response_dict_words():
    return SimpleNamespace(
        text="Guten Morgen.",
        duration=1.5,
        words=[
            {"word": "Guten", "start": 0.0, "end": 0.4, "probability": 0.95},
            {"word": "Morgen", "start": 0.4, "end": 0.9, "probability": 0.92},
        ],
    )


def _fake_groq_response_obj_words():
    return SimpleNamespace(
        text="Hallo Welt.",
        duration=2.0,
        words=[
            SimpleNamespace(word="Hallo", start=0.0, end=0.4, probability=0.91),
            SimpleNamespace(word="Welt", start=0.4, end=0.8, probability=0.88),
        ],
    )


@pytest.mark.asyncio
async def test_transcribe_with_dict_words(fake_audio_bytes) -> None:
    svc = STTService()
    svc._client.audio = SimpleNamespace(
        transcriptions=SimpleNamespace(
            create=AsyncMock(return_value=_fake_groq_response_dict_words())
        )
    )
    result = await svc.transcribe(fake_audio_bytes, audio_format="webm", language="de")
    assert result.transcript == "Guten Morgen."
    assert result.duration_seconds == 1.5
    assert len(result.word_timestamps) == 2
    assert result.word_timestamps[0]["word"] == "Guten"
    assert result.word_timestamps[0]["probability"] == 0.95
    assert result.language == "de"


@pytest.mark.asyncio
async def test_transcribe_with_object_words(fake_audio_bytes) -> None:
    svc = STTService()
    svc._client.audio = SimpleNamespace(
        transcriptions=SimpleNamespace(
            create=AsyncMock(return_value=_fake_groq_response_obj_words())
        )
    )
    result = await svc.transcribe(fake_audio_bytes)
    assert result.transcript == "Hallo Welt."
    assert len(result.word_timestamps) == 2
    assert result.word_timestamps[1]["word"] == "Welt"


@pytest.mark.asyncio
async def test_transcribe_handles_failure(fake_audio_bytes) -> None:
    svc = STTService()
    svc._client.audio = SimpleNamespace(
        transcriptions=SimpleNamespace(
            create=AsyncMock(side_effect=RuntimeError("groq down"))
        )
    )
    result = await svc.transcribe(fake_audio_bytes)
    assert result.transcript == ""
    assert result.confidence == 0.0
    assert result.word_timestamps == []


@pytest.mark.asyncio
async def test_transcribe_cleans_up_temp_file(fake_audio_bytes) -> None:
    """Temp file must be removed in the finally block, even on success."""
    captured = {}

    real_tempfile = __import__("tempfile")
    orig_named = real_tempfile.NamedTemporaryFile

    def spy_named(*args, **kwargs):
        f = orig_named(*args, **kwargs)
        captured["path"] = f.name
        return f

    svc = STTService()
    svc._client.audio = SimpleNamespace(
        transcriptions=SimpleNamespace(
            create=AsyncMock(return_value=_fake_groq_response_dict_words())
        )
    )
    with patch("services.stt_service.tempfile.NamedTemporaryFile", side_effect=spy_named):
        await svc.transcribe(fake_audio_bytes)

    assert "path" in captured
    assert not os.path.exists(captured["path"])


def test_singleton_returns_same_instance() -> None:
    a = get_stt_service()
    b = get_stt_service()
    assert a is b
