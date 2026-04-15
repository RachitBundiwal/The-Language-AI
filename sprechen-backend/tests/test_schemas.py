"""Tests for the Pydantic schemas in models.schemas."""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from models.schemas import (
    CEFRLevel,
    ConversationMessage,
    ConversationRequest,
    ConversationResponse,
    PhonemeScore,
    PronunciationResponse,
    TranscriptionResponse,
    TTSRequest,
    TTSResponse,
    VoiceExerciseResult,
)


def test_cefr_level_values() -> None:
    assert {l.value for l in CEFRLevel} == {"A1", "A2", "B1", "B2", "C1", "C2"}


def test_transcription_defaults() -> None:
    t = TranscriptionResponse(transcript="Hallo")
    assert t.language == "de"
    assert t.confidence == 0.9
    assert t.word_timestamps == []
    assert t.duration_seconds == 0.0


def test_phoneme_score_optional_feedback() -> None:
    p = PhonemeScore(phoneme="ç", score=0.5)
    assert p.feedback is None
    p2 = PhonemeScore(phoneme="ç", score=0.5, feedback="hint")
    assert p2.feedback == "hint"


def test_pronunciation_response_minimum() -> None:
    r = PronunciationResponse(
        overall_score=80,
        pronunciation_score=80,
        fluency_score=85,
        accuracy_score=82,
        completeness_score=100,
    )
    assert r.prosody_score is None
    assert r.phoneme_scores == []
    assert r.problem_phonemes == []
    assert r.ai_feedback == ""


def test_conversation_request_defaults() -> None:
    r = ConversationRequest(message="Hallo")
    assert r.history == []
    assert r.level == CEFRLevel.B1
    assert r.scenario is None
    assert r.formality == "du"


def test_conversation_request_with_history() -> None:
    r = ConversationRequest(
        message="Wie geht's?",
        history=[
            ConversationMessage(role="user", content="Hallo"),
            ConversationMessage(role="assistant", content="Hallo!"),
        ],
        level=CEFRLevel.A2,
        scenario="bakery",
        formality="Sie",
    )
    assert len(r.history) == 2
    assert r.level == CEFRLevel.A2


def test_conversation_message_role_validation() -> None:
    with pytest.raises(ValidationError):
        ConversationMessage(role="ghost", content="boo")


def test_conversation_response_defaults() -> None:
    r = ConversationResponse(reply="Hallo")
    assert r.translation is None
    assert r.corrections == []
    assert r.new_vocabulary == []
    assert r.audio_url is None


def test_tts_request_defaults() -> None:
    r = TTSRequest(text="Guten Tag")
    assert r.voice == "de-DE-KatjaNeural"
    assert r.rate == "+0%"


def test_tts_response_round_trip() -> None:
    r = TTSResponse(audio_url="/audio/x.mp3", duration_seconds=1.2, text="x")
    assert r.audio_url.endswith(".mp3")


def test_voice_exercise_result_optional_conversation() -> None:
    v = VoiceExerciseResult(
        transcription=TranscriptionResponse(transcript="Hi"),
        pronunciation=PronunciationResponse(
            overall_score=1,
            pronunciation_score=1,
            fluency_score=1,
            accuracy_score=1,
            completeness_score=1,
        ),
    )
    assert v.conversation is None
