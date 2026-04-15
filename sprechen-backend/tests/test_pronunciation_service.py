"""Tests for services.pronunciation_service (Whisper + Groq LLM)."""
from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from models.schemas import TranscriptionResponse
from services.pronunciation_service import (
    PHONEME_TIPS,
    PronunciationService,
    get_pronunciation_service,
)


# ---------- helpers ----------
def _fake_transcription(transcript: str = "Guten Morgen ich hätte gerne ein Brötchen",
                        confidence: float = 0.9) -> TranscriptionResponse:
    words = transcript.split()
    return TranscriptionResponse(
        transcript=transcript,
        language="de",
        confidence=confidence,
        word_timestamps=[
            {"word": w, "start": i * 0.3, "end": (i + 1) * 0.3, "probability": confidence}
            for i, w in enumerate(words)
        ],
        duration_seconds=len(words) * 0.3,
    )


def _fake_llm_response(problem_sounds=None, feedback="Sehr gut!", fluency=85, accuracy=88):
    body = {
        "problem_sounds": problem_sounds or [],
        "feedback_de": feedback,
        "fluency_rating": fluency,
        "accuracy_rating": accuracy,
    }
    choice = MagicMock()
    choice.message.content = json.dumps(body)
    resp = MagicMock()
    resp.choices = [choice]
    return resp


# ---------- unit tests ----------
def test_phoneme_tips_contains_german_sounds() -> None:
    for ph in ["ç", "x", "ü", "ö", "r", "z", "pf"]:
        assert ph in PHONEME_TIPS


def test_normalize() -> None:
    assert PronunciationService._normalize("Hallo, Welt!") == "hallo welt"
    assert PronunciationService._normalize("  Ä Ö Ü  ") == "ä ö ü"


def test_basic_feedback_high() -> None:
    assert "Ausgezeichnet" in PronunciationService._basic_feedback(95)


def test_basic_feedback_mid() -> None:
    fb = PronunciationService._basic_feedback(80)
    assert "Sehr gut" in fb or "verständlich" in fb


def test_basic_feedback_low() -> None:
    fb = PronunciationService._basic_feedback(40)
    assert "üben" in fb.lower() or "langsamer" in fb.lower()


def test_fallback_response() -> None:
    fb = PronunciationService._fallback_response("Hallo")
    assert fb.overall_score == 0.0
    assert fb.phoneme_scores == []
    assert fb.ai_feedback


# ---------- async integration tests ----------
@pytest.mark.asyncio
async def test_score_pronunciation_happy_path(fake_audio_bytes, reference_text) -> None:
    svc = PronunciationService()
    fake_trans = _fake_transcription(reference_text, confidence=0.92)

    with patch("services.pronunciation_service.get_stt_service") as mock_stt:
        mock_stt.return_value.transcribe = AsyncMock(return_value=fake_trans)
        svc._llm = AsyncMock()
        svc._llm.chat.completions.create = AsyncMock(
            return_value=_fake_llm_response(
                problem_sounds=["ö", "r"],
                feedback="Achte auf ö und r.",
                fluency=85,
                accuracy=90,
            )
        )
        result = await svc.score_pronunciation(fake_audio_bytes, reference_text)

    assert result.accuracy_score == 90
    assert result.fluency_score == 85
    assert "ö" in result.problem_phonemes
    assert "r" in result.problem_phonemes
    assert "ö" in result.ai_feedback
    assert result.overall_score > 0


@pytest.mark.asyncio
async def test_score_falls_back_on_empty_transcript(fake_audio_bytes, reference_text) -> None:
    svc = PronunciationService()
    empty = TranscriptionResponse(
        transcript="", language="de", confidence=0.0,
        word_timestamps=[], duration_seconds=0.0,
    )
    with patch("services.pronunciation_service.get_stt_service") as mock_stt:
        mock_stt.return_value.transcribe = AsyncMock(return_value=empty)
        result = await svc.score_pronunciation(fake_audio_bytes, reference_text)

    assert result.overall_score == 0.0


@pytest.mark.asyncio
async def test_score_works_without_llm(fake_audio_bytes, reference_text) -> None:
    """If LLM fails, still get numeric scores from Whisper."""
    svc = PronunciationService()
    fake_trans = _fake_transcription(reference_text)

    with patch("services.pronunciation_service.get_stt_service") as mock_stt:
        mock_stt.return_value.transcribe = AsyncMock(return_value=fake_trans)
        svc._llm = AsyncMock()
        svc._llm.chat.completions.create = AsyncMock(side_effect=RuntimeError("LLM down"))
        result = await svc.score_pronunciation(fake_audio_bytes, reference_text)

    assert result.overall_score > 0
    assert result.ai_feedback  # basic feedback still generated


@pytest.mark.asyncio
async def test_score_falls_back_on_stt_crash(fake_audio_bytes, reference_text) -> None:
    svc = PronunciationService()
    with patch("services.pronunciation_service.get_stt_service") as mock_stt:
        mock_stt.return_value.transcribe = AsyncMock(side_effect=RuntimeError("boom"))
        result = await svc.score_pronunciation(fake_audio_bytes, reference_text)

    assert result.overall_score == 0.0


def test_singleton() -> None:
    a = get_pronunciation_service()
    b = get_pronunciation_service()
    assert a is b
