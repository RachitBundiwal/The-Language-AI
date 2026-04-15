"""HTTP routes for progress, vocabulary SRS, pronunciation history, and exam log."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import get_db
from models.orm_models import (
    ExamAttempt,
    Lesson,
    LessonProgress,
    PronunciationSession,
    UserStats,
    VocabularyCard,
)
from models.schemas import PronunciationResponse
from services.gamification_service import get_gamification_service
from services.srs_service import calculate_next_review, get_due_cards
from services.stats_service import (
    _get_or_create_stats,
    add_study_minutes,
    get_dashboard_stats,
    update_streak,
    update_xp,
)

router = APIRouter(prefix="/api/v1/progress", tags=["progress"])


# ---------- request bodies ----------
class LessonCompleteRequest(BaseModel):
    score: float = Field(..., ge=0, le=100)
    time_spent_minutes: int = Field(0, ge=0, le=600)


class SavePronunciationRequest(BaseModel):
    reference_text: str
    pronunciation: PronunciationResponse
    lesson_id: Optional[int] = None


class VocabReviewRequest(BaseModel):
    card_id: int
    quality: int = Field(..., ge=0, le=5)


class VocabAddRequest(BaseModel):
    german_word: str
    english_translation: str
    example_sentence: Optional[str] = None
    phonetic: Optional[str] = None
    source_lesson_id: Optional[int] = None


class ExamSaveRequest(BaseModel):
    level: str
    section: str
    score: float
    max_score: float
    duration_seconds: int = 0
    answers_json: dict = Field(default_factory=dict)
    passed: bool = False


# ---------- /stats ----------
@router.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)) -> dict:
    return await get_dashboard_stats(db)


# ---------- /lessons ----------
@router.get("/lessons")
async def list_lessons(db: AsyncSession = Depends(get_db)) -> List[dict]:
    stmt = (
        select(Lesson, LessonProgress)
        .outerjoin(LessonProgress, LessonProgress.lesson_id == Lesson.id)
        .order_by(Lesson.order_index.asc(), Lesson.id.asc())
    )
    rows = (await db.execute(stmt)).all()
    out: List[dict] = []
    for lesson, progress in rows:
        content = lesson.content_json or {}
        out.append(
            {
                "id": lesson.id,
                "title": lesson.title,
                "level": lesson.level,
                "scenario": lesson.scenario,
                "topic": lesson.topic,
                "estimated_minutes": int(content.get("estimated_minutes", 10)),
                "completed": bool(progress.completed) if progress else False,
                "score": progress.score if progress else None,
                "attempts": int(progress.attempts) if progress else 0,
            }
        )
    return out


@router.post("/lessons/{lesson_id}/complete")
async def complete_lesson(
    lesson_id: int,
    body: LessonCompleteRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    lesson = await db.get(Lesson, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=404, detail="Lesson not found")

    progress = (
        await db.execute(
            select(LessonProgress).where(LessonProgress.lesson_id == lesson_id)
        )
    ).scalar_one_or_none()

    if progress is None:
        progress = LessonProgress(
            lesson_id=lesson_id,
            completed=True,
            score=body.score,
            attempts=1,
            last_attempt_at=datetime.utcnow(),
        )
        db.add(progress)
    else:
        progress.completed = True
        progress.score = body.score
        progress.attempts = (progress.attempts or 0) + 1
        progress.last_attempt_at = datetime.utcnow()

    await db.commit()

    xp_awarded = 50
    if body.score >= 90:
        xp_awarded += 25

    streak_info = await update_streak(db)
    xp_info = await update_xp(xp_awarded, db, reason=f"lesson_{lesson_id}_complete")
    if body.time_spent_minutes:
        await add_study_minutes(body.time_spent_minutes, db)

    newly_earned = await get_gamification_service().check_and_award_achievements(
        "lesson_complete", db
    )

    return {
        "xp_awarded": xp_awarded,
        "total_xp": xp_info["total_xp"],
        "streak": streak_info["streak"],
        "level_changed": xp_info["level_changed"],
        "new_level": xp_info["new_level"],
        "achievements_earned": [
            {"achievement_id": a.achievement_id, "title": a.title, "emoji": a.emoji}
            for a in newly_earned
        ],
    }


# ---------- /pronunciation ----------
@router.post("/pronunciation/save")
async def save_pronunciation(
    body: SavePronunciationRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    p = body.pronunciation
    session = PronunciationSession(
        reference_text=body.reference_text,
        overall_score=p.overall_score,
        pronunciation_score=p.pronunciation_score,
        fluency_score=p.fluency_score,
        accuracy_score=p.accuracy_score,
        problem_phonemes=list(p.problem_phonemes or []),
        lesson_id=body.lesson_id,
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    await get_gamification_service().check_and_award_achievements("pronunciation", db)
    return {"id": session.id, "created_at": session.created_at.isoformat()}


@router.get("/pronunciation/history")
async def pronunciation_history(
    limit: int = 30, db: AsyncSession = Depends(get_db)
) -> dict:
    limit = max(1, min(200, int(limit)))
    stmt = (
        select(PronunciationSession)
        .order_by(desc(PronunciationSession.created_at))
        .limit(limit)
    )
    sessions = list((await db.execute(stmt)).scalars().all())

    items = [
        {
            "id": s.id,
            "reference_text": s.reference_text,
            "overall_score": s.overall_score,
            "pronunciation_score": s.pronunciation_score,
            "fluency_score": s.fluency_score,
            "accuracy_score": s.accuracy_score,
            "problem_phonemes": s.problem_phonemes or [],
            "lesson_id": s.lesson_id,
            "created_at": s.created_at.isoformat(),
        }
        for s in sessions
    ]

    trend = "stable"
    if len(sessions) >= 20:
        recent = [s.overall_score for s in sessions[:10]]
        older = [s.overall_score for s in sessions[10:20]]
        recent_avg = sum(recent) / len(recent)
        older_avg = sum(older) / len(older)
        diff = recent_avg - older_avg
        if diff > 2.0:
            trend = "improving"
        elif diff < -2.0:
            trend = "declining"

    return {"sessions": items, "trend": trend, "count": len(items)}


# ---------- /vocabulary ----------
@router.get("/vocabulary/due")
async def vocabulary_due(db: AsyncSession = Depends(get_db)) -> List[dict]:
    cards = await get_due_cards(db)
    return [_card_to_dict(c) for c in cards]


@router.post("/vocabulary/review")
async def vocabulary_review(
    body: VocabReviewRequest, db: AsyncSession = Depends(get_db)
) -> dict:
    card = await db.get(VocabularyCard, body.card_id)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")

    new_state = calculate_next_review(card, body.quality)
    card.next_review_at = new_state["next_review_at"]
    card.interval_days = new_state["interval_days"]
    card.ease_factor = new_state["ease_factor"]
    card.repetitions = new_state["repetitions"]
    await db.commit()
    await db.refresh(card)

    remaining = (
        await db.execute(
            select(func.count(VocabularyCard.id)).where(
                VocabularyCard.next_review_at <= datetime.utcnow()
            )
        )
    ).scalar_one()

    return {
        "next_review_at": card.next_review_at.isoformat(),
        "interval_days": card.interval_days,
        "ease_factor": card.ease_factor,
        "repetitions": card.repetitions,
        "cards_remaining": int(remaining or 0),
    }


@router.post("/vocabulary/add")
async def vocabulary_add(
    body: VocabAddRequest, db: AsyncSession = Depends(get_db)
) -> dict:
    card = VocabularyCard(
        german_word=body.german_word,
        english_translation=body.english_translation,
        example_sentence=body.example_sentence,
        phonetic=body.phonetic,
        source_lesson_id=body.source_lesson_id,
    )
    db.add(card)
    await db.commit()
    await db.refresh(card)
    await get_gamification_service().check_and_award_achievements("vocab_add", db)
    return _card_to_dict(card)


@router.get("/vocabulary/all")
async def vocabulary_all(db: AsyncSession = Depends(get_db)) -> List[dict]:
    stmt = select(VocabularyCard).order_by(VocabularyCard.created_at.desc())
    cards = list((await db.execute(stmt)).scalars().all())
    return [_card_to_dict(c) for c in cards]


def _card_to_dict(c: VocabularyCard) -> dict:
    return {
        "id": c.id,
        "german_word": c.german_word,
        "english_translation": c.english_translation,
        "example_sentence": c.example_sentence,
        "phonetic": c.phonetic,
        "next_review_at": c.next_review_at.isoformat() if c.next_review_at else None,
        "interval_days": c.interval_days,
        "ease_factor": c.ease_factor,
        "repetitions": c.repetitions,
        "source_lesson_id": c.source_lesson_id,
        "created_at": c.created_at.isoformat() if c.created_at else None,
    }


# ---------- /exam ----------
@router.get("/exam/history")
async def exam_history(db: AsyncSession = Depends(get_db)) -> List[dict]:
    stmt = (
        select(ExamAttempt)
        .order_by(desc(ExamAttempt.created_at))
        .limit(20)
    )
    attempts = list((await db.execute(stmt)).scalars().all())
    return [
        {
            "id": a.id,
            "exam_level": a.exam_level,
            "section": a.section,
            "score": a.score,
            "max_score": a.max_score,
            "duration_seconds": a.duration_seconds,
            "answers_json": a.answers_json or {},
            "passed": a.passed,
            "created_at": a.created_at.isoformat(),
        }
        for a in attempts
    ]


@router.post("/exam/save")
async def exam_save(
    body: ExamSaveRequest, db: AsyncSession = Depends(get_db)
) -> dict:
    attempt = ExamAttempt(
        exam_level=body.level,
        section=body.section,
        score=body.score,
        max_score=body.max_score,
        duration_seconds=body.duration_seconds,
        answers_json=body.answers_json,
        passed=body.passed,
    )
    db.add(attempt)
    await db.commit()
    await db.refresh(attempt)

    xp_info = None
    if body.passed:
        xp_info = await update_xp(200, db, reason=f"exam_{body.level}_{body.section}_passed")

    newly_earned = await get_gamification_service().check_and_award_achievements(
        "exam_save", db
    )

    return {
        "id": attempt.id,
        "created_at": attempt.created_at.isoformat(),
        "passed": attempt.passed,
        "xp_awarded": 200 if body.passed else 0,
        "total_xp": xp_info["total_xp"] if xp_info else None,
        "level_changed": xp_info["level_changed"] if xp_info else False,
        "new_level": xp_info["new_level"] if xp_info else None,
        "achievements_earned": [
            {"achievement_id": a.achievement_id, "title": a.title, "emoji": a.emoji}
            for a in newly_earned
        ],
    }
