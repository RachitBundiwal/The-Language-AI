"""Pydantic schemas for the Goethe Institut exam simulator."""
from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

ExamSection = Literal["Lesen", "Hören", "Schreiben", "Sprechen"]


# ---------- Lesen ----------
class ReadingText(BaseModel):
    title: str
    text: str
    source_note: Optional[str] = None


class ReadingQuestion(BaseModel):
    question: str
    options: List[str]
    correct_index: int
    question_type: str = "multiple_choice"  # multiple_choice / true_false / gap_fill


class ReadingPart(BaseModel):
    part_number: int
    instruction: str
    texts: List[ReadingText] = Field(default_factory=list)
    questions: List[ReadingQuestion]
    max_points: int


# ---------- Hören ----------
class ListeningScript(BaseModel):
    title: str
    script: str
    speaker_context: str


class ListeningQuestion(BaseModel):
    question: str
    options: List[str]
    correct_index: int


class ListeningPart(BaseModel):
    part_number: int
    instruction: str
    scripts: List[ListeningScript]
    questions: List[ListeningQuestion]
    max_points: int


# ---------- Schreiben ----------
class WritingTask(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    task_number: int
    instruction: str
    prompt: str
    min_words: int
    max_words: int
    format_hint: str
    model_answer: str
    max_points: int


# ---------- Sprechen ----------
class SpeakingCard(BaseModel):
    card_number: int
    task_type: str
    prompt: str
    supporting_questions: List[str] = Field(default_factory=list)
    time_allowed_seconds: int


# ---------- Paper ----------
ExamPart = Union[ReadingPart, ListeningPart, WritingTask, SpeakingCard]


class ExamPaper(BaseModel):
    level: str
    section: str
    time_limit_minutes: int
    max_score: int
    instructions: str
    parts: List[Any]  # heterogenous; concrete validation done by section logic


# ---------- Submissions ----------
class WritingAnswer(BaseModel):
    task_number: int
    text: str


class WritingSubmission(BaseModel):
    level: str
    answers: List[WritingAnswer]
    duration_seconds: int = 0


class SpeakingSubmission(BaseModel):
    level: str
    card_number: int
    duration_seconds: int = 0


class MCAnswer(BaseModel):
    question_id: int
    answer_index: int


class MCSubmission(BaseModel):
    level: str
    answers: List[MCAnswer]
    duration_seconds: int = 0


# ---------- Result ----------
class ExamResult(BaseModel):
    level: str
    section: str
    score: float
    max_score: float
    percentage: float
    passed: bool
    grade: str
    detailed_results: List[Dict[str, Any]] = Field(default_factory=list)
    feedback: str = ""
    strengths: List[str] = Field(default_factory=list)
    improvements: List[str] = Field(default_factory=list)


# ---------- Readiness ----------
class ExamReadiness(BaseModel):
    overall: float
    by_section: Dict[str, float]
    recommendation: str
    predicted_weeks: int
