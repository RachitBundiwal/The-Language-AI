"""Tests for services.tts_service."""
from __future__ import annotations

import os
from unittest.mock import MagicMock, patch

import pytest

from models.schemas import TTSRequest
from services.tts_service import GERMAN_VOICES, TTSService, get_tts_service


def test_german_voices_dict_is_populated() -> None:
    assert "de-DE-KatjaNeural" in GERMAN_VOICES
    assert "de-DE-ConradNeural" in GERMAN_VOICES
    assert "de-AT-IngridNeural" in GERMAN_VOICES
    assert "de-CH-LeniNeural" in GERMAN_VOICES
    assert all(isinstance(v, str) for v in GERMAN_VOICES.values())


def test_make_key_is_stable_and_unique() -> None:
    a = TTSService._make_key("hi", "v1", "+0%")
    b = TTSService._make_key("hi", "v1", "+0%")
    c = TTSService._make_key("hi", "v2", "+0%")
    assert a == b
    assert a != c
    assert len(a) == 32  # md5 hex


def test_list_voices_returns_dict() -> None:
    svc = TTSService()
    assert svc.list_voices() == GERMAN_VOICES


def _fake_communicate(audio_chunks):
    """Build a stand-in for edge_tts.Communicate."""
    fake = MagicMock()

    async def stream():
        for c in audio_chunks:
            yield {"type": "audio", "data": c}
        # also yield a non-audio chunk that should be ignored
        yield {"type": "WordBoundary", "data": b""}

    fake.stream = stream
    return fake


@pytest.mark.asyncio
async def test_synthesize_writes_to_cache_and_returns_url(tmp_path) -> None:
    svc = TTSService()
    svc._settings.audio_cache_dir = str(tmp_path)

    fake_comm = _fake_communicate([b"AUDIO", b"BYTES"])
    with patch(
        "services.tts_service.edge_tts.Communicate", return_value=fake_comm
    ), patch.object(TTSService, "_duration", return_value=1.23):
        resp = await svc.synthesize(
            TTSRequest(text="Guten Morgen", voice="de-DE-KatjaNeural", rate="+0%")
        )

    assert resp.audio_url.startswith("/audio/")
    assert resp.audio_url.endswith(".mp3")
    assert resp.duration_seconds == 1.23
    assert resp.text == "Guten Morgen"

    key = TTSService._make_key("Guten Morgen", "de-DE-KatjaNeural", "+0%")
    cached = os.path.join(tmp_path, f"{key}.mp3")
    assert os.path.exists(cached)
    with open(cached, "rb") as f:
        assert f.read() == b"AUDIOBYTES"


@pytest.mark.asyncio
async def test_synthesize_uses_cache_on_second_call(tmp_path) -> None:
    svc = TTSService()
    svc._settings.audio_cache_dir = str(tmp_path)

    key = TTSService._make_key("Hallo", "de-DE-KatjaNeural", "+0%")
    cached = os.path.join(tmp_path, f"{key}.mp3")
    with open(cached, "wb") as f:
        f.write(b"PRECACHED")

    with patch("services.tts_service.edge_tts.Communicate") as mock_comm, patch.object(
        TTSService, "_duration", return_value=2.0
    ):
        resp = await svc.synthesize(TTSRequest(text="Hallo"))
        mock_comm.assert_not_called()  # cache hit

    assert resp.audio_url == f"/audio/{key}.mp3"
    assert resp.duration_seconds == 2.0


@pytest.mark.asyncio
async def test_synthesize_falls_back_to_gtts(tmp_path) -> None:
    svc = TTSService()
    svc._settings.audio_cache_dir = str(tmp_path)
    with patch(
        "services.tts_service.edge_tts.Communicate",
        side_effect=RuntimeError("network down"),
    ), patch.object(
        TTSService, "_gtts_bytes", return_value=b"FALLBACK_MP3"
    ), patch.object(TTSService, "_duration", return_value=0.5):
        resp = await svc.synthesize(TTSRequest(text="kaputt"))
    assert resp.audio_url.endswith(".mp3")
    assert resp.duration_seconds == 0.5
    key = TTSService._make_key("kaputt", svc._settings.edge_tts_voice, svc._settings.edge_tts_rate)
    with open(os.path.join(tmp_path, f"{key}.mp3"), "rb") as f:
        assert f.read() == b"FALLBACK_MP3"


@pytest.mark.asyncio
async def test_synthesize_raises_when_all_providers_fail(tmp_path) -> None:
    from fastapi import HTTPException
    svc = TTSService()
    svc._settings.audio_cache_dir = str(tmp_path)
    with patch(
        "services.tts_service.edge_tts.Communicate",
        side_effect=RuntimeError("network down"),
    ), patch.object(TTSService, "_gtts_bytes", return_value=b""):
        with pytest.raises(HTTPException) as exc:
            await svc.synthesize(TTSRequest(text="kaputt"))
    assert exc.value.status_code == 503


@pytest.mark.asyncio
async def test_synthesize_to_bytes_collects_chunks() -> None:
    svc = TTSService()
    fake_comm = _fake_communicate([b"AAA", b"BBB"])
    with patch("services.tts_service.edge_tts.Communicate", return_value=fake_comm):
        out = await svc.synthesize_to_bytes("hi")
    assert out == b"AAABBB"


@pytest.mark.asyncio
async def test_synthesize_to_bytes_returns_empty_on_failure() -> None:
    svc = TTSService()
    with patch(
        "services.tts_service.edge_tts.Communicate",
        side_effect=RuntimeError("boom"),
    ), patch.object(TTSService, "_gtts_bytes", return_value=b""):
        out = await svc.synthesize_to_bytes("hi")
    assert out == b""


def test_singleton_tts_service() -> None:
    a = get_tts_service()
    b = get_tts_service()
    assert a is b
