"""SQLAlchemy ORM models for the Sprechen data layer."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from models.database import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, unique=True, nullable=False, index=True)
    level = Column(String, nullable=False, index=True)  # A1..C2
    scenario = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    content_json = Column(JSON, nullable=False, default=dict)
    order_index = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    progress = relationship(
        "LessonProgress", back_populates="lesson", cascade="all, delete-orphan"
    )


class LessonProgress(Base):
    __tablename__ = "lesson_progress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False, index=True)
    completed = Column(Boolean, nullable=False, default=False)
    score = Column(Float, nullable=True)
    attempts = Column(Integer, nullable=False, default=0)
    last_attempt_at = Column(DateTime, nullable=True)

    lesson = relationship("Lesson", back_populates="progress")


class VocabularyCard(Base):
    __tablename__ = "vocabulary_cards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    german_word = Column(String, nullable=False, index=True)
    english_translation = Column(String, nullable=False)
    example_sentence = Column(String, nullable=True)
    phonetic = Column(String, nullable=True)

    next_review_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, index=True
    )
    interval_days = Column(Integer, nullable=False, default=1)
    ease_factor = Column(Float, nullable=False, default=2.5)
    repetitions = Column(Integer, nullable=False, default=0)

    source_lesson_id = Column(
        Integer, ForeignKey("lessons.id"), nullable=True, index=True
    )
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class PronunciationSession(Base):
    __tablename__ = "pronunciation_sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reference_text = Column(String, nullable=False)
    overall_score = Column(Float, nullable=False, default=0.0)
    pronunciation_score = Column(Float, nullable=False, default=0.0)
    fluency_score = Column(Float, nullable=False, default=0.0)
    accuracy_score = Column(Float, nullable=False, default=0.0)
    problem_phonemes = Column(JSON, nullable=False, default=list)
    lesson_id = Column(
        Integer, ForeignKey("lessons.id"), nullable=True, index=True
    )
    created_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, index=True
    )


class ExamAttempt(Base):
    __tablename__ = "exam_attempts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    exam_level = Column(String, nullable=False, index=True)
    section = Column(String, nullable=False)  # Lesen / Hören / Schreiben / Sprechen
    score = Column(Float, nullable=False)
    max_score = Column(Float, nullable=False)
    duration_seconds = Column(Integer, nullable=False, default=0)
    answers_json = Column(JSON, nullable=False, default=dict)
    passed = Column(Boolean, nullable=False, default=False)
    created_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, index=True
    )


class GrammarError(Base):
    __tablename__ = "grammar_errors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_id = Column(String, nullable=False, index=True)
    original_text = Column(String, nullable=False)
    corrected_text = Column(String, nullable=False)
    lesson_id = Column(
        Integer, ForeignKey("lessons.id"), nullable=True, index=True
    )
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class UserStats(Base):
    __tablename__ = "user_stats"

    id = Column(Integer, primary_key=True, default=1)
    xp_points = Column(Integer, nullable=False, default=0)
    streak_days = Column(Integer, nullable=False, default=0)
    last_active = Column(DateTime, nullable=True)
    current_level = Column(String, nullable=False, default="A1")
    total_minutes_studied = Column(Integer, nullable=False, default=0)


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    achievement_id = Column(String, nullable=False, unique=True, index=True)
    title = Column(String, nullable=False)
    emoji = Column(String, nullable=False)
    earned_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class XPEvent(Base):
    __tablename__ = "xp_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Integer, nullable=False, default=0)
    reason = Column(String, nullable=False, default="")
    created_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, index=True
    )
