"""End-to-end pipeline tests with all external services mocked."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from main import app
from models.schemas import (
    ConversationResponse,
    PhonemeScore,
    PronunciationResponse,
    TranscriptionResponse,
    TTSResponse,
)
from services.conversation_service import SCENARIOS
from services.tts_service import GERMAN_VOICES

client = TestClient(app)


# ---------- helpers ----------
def _fake_transcription() -> TranscriptionResponse:
    return TranscriptionResponse(
        transcript="Guten Morgen, ich hätte gerne ein Brötchen.",
        language="de",
        confidence=0.95,
        word_timestamps=[
            {"word": "Guten", "start": 0.0, "end": 0.4, "probability": 0.9},
            {"word": "Morgen", "start": 0.4, "end": 0.9, "probability": 0.9},
        ],
        duration_seconds=2.1,
    )


def _fake_pronunciation() -> PronunciationResponse:
    return PronunciationResponse(
        overall_score=87.5,
        pronunciation_score=87.5,
        fluency_score=90.0,
        accuracy_score=88.0,
        completeness_score=100.0,
        prosody_score=85.0,
        phoneme_scores=[
            PhonemeScore(phoneme="ç", score=0.55, feedback="ich-Laut"),
            PhonemeScore(phoneme="t", score=0.95, feedback=None),
        ],
        problem_phonemes=["ç"],
        ai_feedback="Achte auf den ich-Laut.",
    )


def _fake_conversation() -> ConversationResponse:
    return ConversationResponse(
        reply="Guten Morgen! Hier ist Ihr Brötchen.",
        translation="Good morning! Here is your roll.",
        corrections=[],
        new_vocabulary=[
            {"word": "Brötchen", "translation": "bread roll", "example": "Ich esse ein Brötchen."}
        ],
    )


def _fake_tts() -> TTSResponse:
    return TTSResponse(
        audio_url="/audio/abc123.mp3",
        duration_seconds=1.8,
        text="Guten Morgen!",
    )


# ---------- tests ----------
def test_health() -> None:
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "services" in body
    assert "stt" in body["services"]


def test_transcribe() -> None:
    with patch(
        "routers.ai_routes.get_stt_service"
    ) as mock_get:
        svc = AsyncMock()
        svc.transcribe = AsyncMock(return_value=_fake_transcription())
        mock_get.return_value = svc

        r = client.post(
            "/api/v1/voice/transcribe",
            files={"file": ("hello.webm", b"fake-audio-bytes", "audio/webm")},
            data={"language": "de"},
        )
    assert r.status_code == 200
    body = r.json()
    assert "transcript" in body
    assert body["transcript"].startswith("Guten Morgen")


def test_pronunciation() -> None:
    with patch(
        "routers.ai_routes.get_pronunciation_service"
    ) as mock_get:
        svc = AsyncMock()
        svc.score_pronunciation = AsyncMock(return_value=_fake_pronunciation())
        mock_get.return_value = svc

        r = client.post(
            "/api/v1/voice/score-pronunciation",
            files={"file": ("a.webm", b"fake", "audio/webm")},
            data={"reference_text": "Guten Morgen"},
        )
    assert r.status_code == 200
    body = r.json()
    assert "phoneme_scores" in body
    assert len(body["phoneme_scores"]) == 2
    assert body["problem_phonemes"] == ["ç"]


def test_chat() -> None:
    with patch(
        "routers.ai_routes.get_conversation_service"
    ) as mock_get:
        svc = AsyncMock()
        svc.chat = AsyncMock(return_value=_fake_conversation())
        mock_get.return_value = svc

        r = client.post(
            "/api/v1/conversation/chat",
            json={
                "message": "Hallo!",
                "history": [],
                "level": "B1",
                "scenario": "bakery",
                "formality": "Sie",
            },
        )
    assert r.status_code == 200
    body = r.json()
    assert "reply" in body
    assert body["reply"].startswith("Guten Morgen")
    assert isinstance(body["new_vocabulary"], list)


def test_tts() -> None:
    with patch(
        "routers.ai_routes.get_tts_service"
    ) as mock_get:
        svc = AsyncMock()
        svc.synthesize = AsyncMock(return_value=_fake_tts())
        mock_get.return_value = svc

        r = client.post(
            "/api/v1/voice/tts",
            json={"text": "Guten Morgen!", "voice": "de-DE-KatjaNeural", "rate": "+0%"},
        )
    assert r.status_code == 200
    body = r.json()
    assert body["audio_url"].endswith(".mp3")


def test_full_pipeline() -> None:
    with patch("routers.ai_routes.get_stt_service") as m_stt, patch(
        "routers.ai_routes.get_pronunciation_service"
    ) as m_pron, patch(
        "routers.ai_routes.get_conversation_service"
    ) as m_conv, patch(
        "routers.ai_routes.get_tts_service"
    ) as m_tts:
        stt = AsyncMock()
        stt.transcribe = AsyncMock(return_value=_fake_transcription())
        m_stt.return_value = stt

        pron = AsyncMock()
        pron.score_pronunciation = AsyncMock(return_value=_fake_pronunciation())
        m_pron.return_value = pron

        conv = AsyncMock()
        conv.chat = AsyncMock(return_value=_fake_conversation())
        m_conv.return_value = conv

        tts = AsyncMock()
        tts.synthesize = AsyncMock(return_value=_fake_tts())
        m_tts.return_value = tts

        r = client.post(
            "/api/v1/voice/full-exercise",
            files={"file": ("a.webm", b"fake-bytes", "audio/webm")},
            data={
                "reference_text": "Guten Morgen, ich hätte gerne ein Brötchen.",
                "level": "B1",
                "scenario": "bakery",
            },
        )
    assert r.status_code == 200
    body = r.json()
    assert "transcription" in body
    assert "pronunciation" in body
    assert "conversation" in body
    assert body["transcription"]["transcript"]
    assert body["pronunciation"]["phoneme_scores"]
    assert body["conversation"]["reply"]
    assert body["conversation"]["audio_url"].endswith(".mp3")


def test_scenarios() -> None:
    expected = {
        "bakery",
        "doctor",
        "job_interview",
        "supermarket",
        "train_station",
        "restaurant",
        "landlord",
    }
    assert expected.issubset(set(SCENARIOS.keys()))


def test_voices() -> None:
    assert "de-DE-KatjaNeural" in GERMAN_VOICES
    assert "de-DE-ConradNeural" in GERMAN_VOICES
