"""Streak / XP / dashboard helpers backed by UserStats."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import desc, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.orm_models import (
    Lesson,
    LessonProgress,
    PronunciationSession,
    UserStats,
    VocabularyCard,
    XPEvent,
)

LEVEL_THRESHOLDS = [
    ("A1", 0),
    ("A2", 500),
    ("B1", 1500),
    ("B2", 3500),
    ("C1", 7000),
    ("C2", 13000),
]


async def _get_or_create_stats(db: AsyncSession) -> UserStats:
    stats: Optional[UserStats] = await db.get(UserStats, 1)
    if stats is None:
        stats = UserStats(id=1)
        db.add(stats)
        try:
            await db.commit()
            await db.refresh(stats)
        except IntegrityError:
            await db.rollback()
            stats = await db.get(UserStats, 1)
    return stats  # type: ignore[return-value]


def _level_for_xp(xp: int) -> str:
    current = "A1"
    for name, threshold in LEVEL_THRESHOLDS:
        if xp >= threshold:
            current = name
        else:
            break
    return current


async def update_streak(db: AsyncSession) -> dict:
    stats = await _get_or_create_stats(db)
    now = datetime.utcnow()
    today = now.date()

    if stats.last_active is None:
        stats.streak_days = 1
    else:
        last_date = stats.last_active.date()
        gap = (today - last_date).days
        if gap == 0:
            pass  # already counted today
        elif gap == 1:
            stats.streak_days = (stats.streak_days or 0) + 1
        else:
            stats.streak_days = 1

    stats.last_active = now
    await db.commit()
    await db.refresh(stats)

    bonus_xp = min(100, (stats.streak_days or 0) * 5)
    return {"streak": stats.streak_days, "bonus_xp": bonus_xp}


async def update_xp(amount: int, db: AsyncSession, reason: str = "") -> dict:
    stats = await _get_or_create_stats(db)
    old_level = stats.current_level or "A1"
    stats.xp_points = (stats.xp_points or 0) + int(amount)
    new_level = _level_for_xp(stats.xp_points)
    level_changed = new_level != old_level
    stats.current_level = new_level
    db.add(XPEvent(amount=int(amount), reason=reason or ""))
    await db.commit()
    await db.refresh(stats)
    return {
        "total_xp": stats.xp_points,
        "level_changed": level_changed,
        "new_level": new_level,
    }


async def add_study_minutes(minutes: int, db: AsyncSession) -> int:
    if minutes <= 0:
        return 0
    stats = await _get_or_create_stats(db)
    stats.total_minutes_studied = int(stats.total_minutes_studied or 0) + int(minutes)
    await db.commit()
    await db.refresh(stats)
    return int(stats.total_minutes_studied)


async def get_dashboard_stats(db: AsyncSession) -> dict:
    stats = await _get_or_create_stats(db)

    lessons_completed = (
        await db.execute(
            select(func.count(LessonProgress.id)).where(
                LessonProgress.completed.is_(True)
            )
        )
    ).scalar_one()

    total_lessons = (
        await db.execute(select(func.count(Lesson.id)))
    ).scalar_one()

    recent_pron_stmt = (
        select(PronunciationSession.overall_score)
        .order_by(desc(PronunciationSession.created_at))
        .limit(30)
    )
    recent_scores = [
        row[0] for row in (await db.execute(recent_pron_stmt)).all()
    ]
    avg_pronunciation = (
        round(sum(recent_scores) / len(recent_scores), 2) if recent_scores else 0.0
    )

    vocab_count = (
        await db.execute(select(func.count(VocabularyCard.id)))
    ).scalar_one()

    vocab_due = (
        await db.execute(
            select(func.count(VocabularyCard.id)).where(
                VocabularyCard.next_review_at <= datetime.utcnow()
            )
        )
    ).scalar_one()

    return {
        "xp": stats.xp_points,
        "streak": stats.streak_days,
        "level": stats.current_level,
        "total_minutes": stats.total_minutes_studied,
        "last_active": stats.last_active.isoformat() if stats.last_active else None,
        "lessons_completed": int(lessons_completed or 0),
        "total_lessons": int(total_lessons or 0),
        "pronunciation_avg": avg_pronunciation,
        "vocabulary_count": int(vocab_count or 0),
        "vocab_due_count": int(vocab_due or 0),
    }
