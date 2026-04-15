"""HTTP-level tests for routers.ai_routes (all externals mocked)."""
from __future__ import annotations

import json
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

client = TestClient(app)


# ---------- shared fakes ----------
def _fake_transcription() -> TranscriptionResponse:
    return TranscriptionResponse(
        transcript="Guten Morgen, ich hätte gerne ein Brötchen.",
        language="de",
        confidence=0.95,
        word_timestamps=[
            {"word": "Guten", "start": 0.0, "end": 0.4, "probability": 0.9}
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
            {"word": "Brötchen", "translation": "roll", "example": "x"}
        ],
    )


def _fake_tts() -> TTSResponse:
    return TTSResponse(
        audio_url="/audio/abc123.mp3",
        duration_seconds=1.8,
        text="Guten Morgen!",
    )


# ---------- /transcribe ----------
def test_transcribe_endpoint() -> None:
    with patch("routers.ai_routes.get_stt_service") as m:
        svc = AsyncMock()
        svc.transcribe = AsyncMock(return_value=_fake_transcription())
        m.return_value = svc
        r = client.post(
            "/api/v1/voice/transcribe",
            files={"file": ("hello.webm", b"fake", "audio/webm")},
            data={"language": "de"},
        )
    assert r.status_code == 200
    body = r.json()
    assert body["transcript"].startswith("Guten Morgen")
    assert body["language"] == "de"
    assert body["duration_seconds"] == 2.1


def test_transcribe_passes_format_from_filename() -> None:
    captured = {}

    async def fake_transcribe(audio_bytes, audio_format="webm", language="de"):
        captured["audio_format"] = audio_format
        captured["language"] = language
        return _fake_transcription()

    with patch("routers.ai_routes.get_stt_service") as m:
        svc = AsyncMock()
        svc.transcribe = fake_transcribe
        m.return_value = svc
        r = client.post(
            "/api/v1/voice/transcribe",
            files={"file": ("audio.mp3", b"fake", "audio/mpeg")},
            data={"language": "de"},
        )
    assert r.status_code == 200
    assert captured["audio_format"] == "mp3"
    assert captured["language"] == "de"


# ---------- /score-pronunciation ----------
def test_score_pronunciation_endpoint() -> None:
    with patch("routers.ai_routes.get_pronunciation_service") as m:
        svc = AsyncMock()
        svc.score_pronunciation = AsyncMock(return_value=_fake_pronunciation())
        m.return_value = svc
        r = client.post(
            "/api/v1/voice/score-pronunciation",
            files={"file": ("a.webm", b"fake", "audio/webm")},
            data={"reference_text": "Guten Morgen"},
        )
    assert r.status_code == 200
    body = r.json()
    assert body["pronunciation_score"] == 87.5
    assert body["problem_phonemes"] == ["ç"]
    assert len(body["phoneme_scores"]) == 2


def test_score_pronunciation_requires_reference_text() -> None:
    r = client.post(
        "/api/v1/voice/score-pronunciation",
        files={"file": ("a.webm", b"fake", "audio/webm")},
    )
    assert r.status_code == 422


# ---------- /full-exercise ----------
def test_full_exercise_runs_all_three_stages() -> None:
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
    assert body["transcription"]["transcript"]
    assert body["pronunciation"]["phoneme_scores"]
    assert body["conversation"]["reply"]
    assert body["conversation"]["audio_url"].endswith(".mp3")


def test_full_exercise_survives_tts_failure() -> None:
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
        tts.synthesize = AsyncMock(side_effect=RuntimeError("tts down"))
        m_tts.return_value = tts

        r = client.post(
            "/api/v1/voice/full-exercise",
            files={"file": ("a.webm", b"fake", "audio/webm")},
            data={
                "reference_text": "Hallo",
                "level": "B1",
                "scenario": "bakery",
            },
        )
    assert r.status_code == 200
    body = r.json()
    # The conversation reply should still be present, just without audio_url.
    assert body["conversation"]["reply"]


# ---------- /tts ----------
def test_tts_endpoint() -> None:
    with patch("routers.ai_routes.get_tts_service") as m:
        svc = AsyncMock()
        svc.synthesize = AsyncMock(return_value=_fake_tts())
        m.return_value = svc
        r = client.post(
            "/api/v1/voice/tts",
            json={
                "text": "Guten Morgen!",
                "voice": "de-DE-KatjaNeural",
                "rate": "+0%",
            },
        )
    assert r.status_code == 200
    body = r.json()
    assert body["audio_url"].endswith(".mp3")
    assert body["text"] == "Guten Morgen!"


# ---------- /voices ----------
def test_voices_endpoint() -> None:
    r = client.get("/api/v1/voice/voices")
    assert r.status_code == 200
    body = r.json()
    assert "de-DE-KatjaNeural" in body
    assert "de-DE-ConradNeural" in body


# ---------- /chat ----------
def test_chat_endpoint() -> None:
    with patch("routers.ai_routes.get_conversation_service") as m:
        svc = AsyncMock()
        svc.chat = AsyncMock(return_value=_fake_conversation())
        m.return_value = svc
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
    assert body["reply"].startswith("Guten Morgen")
    assert body["new_vocabulary"][0]["word"] == "Brötchen"


def test_chat_rejects_invalid_level() -> None:
    r = client.post(
        "/api/v1/conversation/chat",
        json={"message": "Hi", "history": [], "level": "Z9", "formality": "du"},
    )
    assert r.status_code == 422


# ---------- /chat/stream ----------
def test_chat_stream_emits_sse() -> None:
    async def fake_stream(req):
        for t in ["Hal", "lo", "!"]:
            yield t

    with patch("routers.ai_routes.get_conversation_service") as m:
        svc = AsyncMock()
        svc.stream_chat = fake_stream
        m.return_value = svc
        with client.stream(
            "POST",
            "/api/v1/conversation/chat/stream",
            json={"message": "Hallo", "history": [], "level": "B1", "formality": "du"},
        ) as r:
            assert r.status_code == 200
            assert r.headers["content-type"].startswith("text/event-stream")
            chunks = list(r.iter_text())

    full = "".join(chunks)
    assert 'data: {"token": "Hal"}' in full
    assert 'data: {"token": "lo"}' in full
    assert "data: [DONE]" in full


# ---------- /evaluate-writing ----------
def test_evaluate_writing_endpoint() -> None:
    fake = {
        "score": 13,
        "grade": "gut",
        "feedback": "Gut gemacht.",
        "strengths": ["Wortschatz"],
        "improvements": ["Kommas"],
    }
    with patch("routers.ai_routes.get_conversation_service") as m:
        svc = AsyncMock()
        svc.evaluate_writing = AsyncMock(return_value=fake)
        m.return_value = svc
        r = client.post(
            "/api/v1/conversation/evaluate-writing",
            data={
                "text": "Mein Text ist gut.",
                "task": "Schreib einen Text",
                "level": "B1",
            },
        )
    assert r.status_code == 200
    assert r.json() == fake


# ---------- /generate-dialogue ----------
def test_generate_dialogue_endpoint() -> None:
    fake = [
        {"speaker": "A", "german": "Hallo!", "english": "Hello!"},
        {"speaker": "B", "german": "Hi!", "english": "Hi!"},
    ]
    with patch("routers.ai_routes.get_conversation_service") as m:
        svc = AsyncMock()
        svc.generate_lesson_dialogue = AsyncMock(return_value=fake)
        m.return_value = svc
        r = client.post(
            "/api/v1/conversation/generate-dialogue",
            data={
                "scenario": "bakery",
                "level": "A2",
                "topic": "Brot kaufen",
                "num_exchanges": 2,
            },
        )
    assert r.status_code == 200
    body = r.json()
    assert body == {"dialogue": fake}


def test_generate_dialogue_rejects_unknown_scenario() -> None:
    r = client.post(
        "/api/v1/conversation/generate-dialogue",
        data={
            "scenario": "spaceship",
            "level": "B1",
            "topic": "warp drive",
            "num_exchanges": 4,
        },
    )
    assert r.status_code == 400
    assert "spaceship" in r.json()["detail"]
