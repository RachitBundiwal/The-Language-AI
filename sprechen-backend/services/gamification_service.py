"""Gamification: XP, levels, streaks, and achievements."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.orm_models import (
    Achievement,
    ExamAttempt,
    LessonProgress,
    PronunciationSession,
    UserStats,
    VocabularyCard,
    XPEvent,
)

XP_THRESHOLDS: Dict[str, int] = {
    "A1": 0,
    "A2": 500,
    "B1": 1500,
    "B2": 3500,
    "C1": 7000,
    "C2": 13000,
}

ACHIEVEMENTS: Dict[str, Dict[str, str]] = {
    "first_lesson": {
        "title": "Erster Schritt",
        "emoji": "🎓",
        "description": "Erste Lektion abgeschlossen",
    },
    "lessons_10": {
        "title": "Auf Kurs",
        "emoji": "📖",
        "description": "10 Lektionen abgeschlossen",
    },
    "lessons_30": {
        "title": "Lernprofi",
        "emoji": "🏆",
        "description": "30 Lektionen abgeschlossen",
    },
    "streak_7": {
        "title": "Eine Woche dabei",
        "emoji": "🔥",
        "description": "7 Tage Lernstreak",
    },
    "streak_30": {
        "title": "Ein Monat dabei",
        "emoji": "⚡",
        "description": "30 Tage Lernstreak",
    },
    "streak_100": {
        "title": "Unaufhaltsam",
        "emoji": "💪",
        "description": "100 Tage Lernstreak",
    },
    "pronunciation_90": {
        "title": "Ausgezeichnete Aussprache",
        "emoji": "🎤",
        "description": "Aussprache über 90 erzielt",
    },
    "vocabulary_100": {
        "title": "Vokabelmeister",
        "emoji": "📚",
        "description": "100 Vokabeln gelernt",
    },
    "vocabulary_500": {
        "title": "Wortschatzriese",
        "emoji": "🧠",
        "description": "500 Vokabeln gelernt",
    },
    "exam_pass": {
        "title": "Prüfung bestanden",
        "emoji": "📜",
        "description": "Eine Prüfungssimulation bestanden",
    },
    "level_up": {
        "title": "Aufgestiegen!",
        "emoji": "📈",
        "description": "Nächstes Niveau erreicht",
    },
}


def _level_for_xp(xp: int) -> str:
    current = "A1"
    for name, threshold in sorted(XP_THRESHOLDS.items(), key=lambda kv: kv[1]):
        if xp >= threshold:
            current = name
        else:
            break
    return current


async def _get_or_create_stats(db: AsyncSession) -> UserStats:
    stats: Optional[UserStats] = await db.get(UserStats, 1)
    if stats is None:
        stats = UserStats(id=1)
        db.add(stats)
        await db.commit()
        await db.refresh(stats)
    return stats


class GamificationService:
    """Single-user gamification service."""

    async def award_xp(
        self, amount: int, reason: str, db: AsyncSession
    ) -> Dict[str, Any]:
        stats = await _get_or_create_stats(db)
        old_level = stats.current_level or "A1"
        stats.xp_points = int(stats.xp_points or 0) + int(amount)
        new_level = _level_for_xp(stats.xp_points)
        level_changed = new_level != old_level
        stats.current_level = new_level

        db.add(XPEvent(amount=int(amount), reason=reason or ""))
        await db.commit()
        await db.refresh(stats)

        return {
            "new_xp": int(stats.xp_points),
            "level_changed": bool(level_changed),
            "new_level": new_level if level_changed else None,
        }

    async def update_streak(self, db: AsyncSession) -> Dict[str, Any]:
        stats = await _get_or_create_stats(db)
        now = datetime.utcnow()
        today = now.date()
        previous_streak = int(stats.streak_days or 0)

        if stats.last_active is None:
            stats.streak_days = 1
        else:
            last_date = stats.last_active.date()
            gap = (today - last_date).days
            if gap == 0:
                pass
            elif gap == 1:
                stats.streak_days = previous_streak + 1
            else:
                stats.streak_days = 1

        stats.last_active = now
        await db.commit()
        await db.refresh(stats)

        bonus_xp = min(int(stats.streak_days or 0) * 5, 100)
        if bonus_xp > 0:
            await self.award_xp(bonus_xp, "streak_bonus", db)

        is_new_high = int(stats.streak_days or 0) > previous_streak
        return {
            "streak": int(stats.streak_days or 0),
            "is_new_high": bool(is_new_high),
            "bonus_xp": int(bonus_xp),
        }

    async def check_and_award_achievements(
        self, trigger: str, db: AsyncSession
    ) -> List[Achievement]:
        stats = await _get_or_create_stats(db)

        existing_rows = (
            await db.execute(select(Achievement.achievement_id))
        ).all()
        existing_ids = {row[0] for row in existing_rows}

        lessons_completed = int(
            (
                await db.execute(
                    select(func.count(LessonProgress.id)).where(
                        LessonProgress.completed.is_(True)
                    )
                )
            ).scalar_one()
            or 0
        )

        max_pron = (
            await db.execute(
                select(func.max(PronunciationSession.overall_score))
            )
        ).scalar_one()
        max_pron_value = float(max_pron or 0.0)

        vocab_count = int(
            (
                await db.execute(select(func.count(VocabularyCard.id)))
            ).scalar_one()
            or 0
        )

        any_exam_passed = (
            (
                await db.execute(
                    select(func.count(ExamAttempt.id)).where(
                        ExamAttempt.passed.is_(True)
                    )
                )
            ).scalar_one()
            or 0
        ) > 0

        streak = int(stats.streak_days or 0)
        current_level = stats.current_level or "A1"

        candidates: List[str] = []
        if lessons_completed >= 1:
            candidates.append("first_lesson")
        if lessons_completed >= 10:
            candidates.append("lessons_10")
        if lessons_completed >= 30:
            candidates.append("lessons_30")
        if streak >= 7:
            candidates.append("streak_7")
        if streak >= 30:
            candidates.append("streak_30")
        if streak >= 100:
            candidates.append("streak_100")
        if max_pron_value >= 90.0:
            candidates.append("pronunciation_90")
        if vocab_count >= 100:
            candidates.append("vocabulary_100")
        if vocab_count >= 500:
            candidates.append("vocabulary_500")
        if any_exam_passed:
            candidates.append("exam_pass")
        if current_level != "A1":
            candidates.append("level_up")

        newly_earned: List[Achievement] = []
        for aid in candidates:
            if aid in existing_ids or aid not in ACHIEVEMENTS:
                continue
            meta = ACHIEVEMENTS[aid]
            row = Achievement(
                achievement_id=aid,
                title=meta["title"],
                emoji=meta["emoji"],
                earned_at=datetime.utcnow(),
            )
            db.add(row)
            newly_earned.append(row)

        if newly_earned:
            await db.commit()
            for row in newly_earned:
                await db.refresh(row)

        # silence unused trigger argument (kept for caller clarity / future filtering)
        _ = trigger
        return newly_earned

    async def get_achievements(self, db: AsyncSession) -> List[Dict[str, Any]]:
        rows = (await db.execute(select(Achievement))).scalars().all()
        earned_map: Dict[str, Achievement] = {r.achievement_id: r for r in rows}

        out: List[Dict[str, Any]] = []
        for aid, meta in ACHIEVEMENTS.items():
            earned_row = earned_map.get(aid)
            out.append(
                {
                    "achievement_id": aid,
                    "title": meta["title"],
                    "emoji": meta["emoji"],
                    "description": meta["description"],
                    "earned": earned_row is not None,
                    "earned_at": (
                        earned_row.earned_at.isoformat()
                        if earned_row is not None
                        else None
                    ),
                }
            )
        return out


_service: Optional[GamificationService] = None


def get_gamification_service() -> GamificationService:
    global _service
    if _service is None:
        _service = GamificationService()
    return _service
