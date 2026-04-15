"""Pydantic schemas for the Sprechen AI backend."""
from enum import Enum
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class CEFRLevel(str, Enum):
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"


# ---------- STT ----------
class TranscriptionResponse(BaseModel):
    transcript: str
    language: str = "de"
    confidence: float = 0.9
    word_timestamps: List[dict] = Field(default_factory=list)
    duration_seconds: float = 0.0


# ---------- Pronunciation ----------
class PhonemeScore(BaseModel):
    phoneme: str
    score: float  # 0.0 - 1.0
    feedback: Optional[str] = None


class PronunciationResponse(BaseModel):
    overall_score: float
    pronunciation_score: float
    fluency_score: float
    accuracy_score: float
    completeness_score: float
    prosody_score: Optional[float] = None
    phoneme_scores: List[PhonemeScore] = Field(default_factory=list)
    problem_phonemes: List[str] = Field(default_factory=list)
    ai_feedback: str = ""


# ---------- Conversation ----------
class ConversationMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class ConversationRequest(BaseModel):
    message: str
    history: List[ConversationMessage] = Field(default_factory=list)
    level: CEFRLevel = CEFRLevel.B1
    scenario: Optional[str] = None
    formality: str = "du"


class ConversationResponse(BaseModel):
    reply: str
    translation: Optional[str] = None
    corrections: List[dict] = Field(default_factory=list)
    new_vocabulary: List[dict] = Field(default_factory=list)
    audio_url: Optional[str] = None


# ---------- TTS ----------
class TTSRequest(BaseModel):
    text: str
    voice: str = "de-DE-KatjaNeural"
    rate: str = "+0%"


class TTSResponse(BaseModel):
    audio_url: str
    duration_seconds: float
    text: str


# ---------- Combined ----------
class VoiceExerciseResult(BaseModel):
    transcription: TranscriptionResponse
    pronunciation: PronunciationResponse
    conversation: Optional[ConversationResponse] = None
