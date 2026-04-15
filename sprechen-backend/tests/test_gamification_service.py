"""Tests for services.gamification_service."""
from __future__ import annotations

from datetime import datetime, timedelta

import pytest
from sqlalchemy import select
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
from services.gamification_service import (
    ACHIEVEMENTS,
    GamificationService,
    _level_for_xp,
)

# Re-use shared DB fixture
from tests.conftest_db import db_session  # noqa: F401


@pytest.fixture
def svc() -> GamificationService:
    return GamificationService()


# ---------------------------------------------------------------------------
# _level_for_xp
# ---------------------------------------------------------------------------


class TestLevelForXP:
    def test_zero_xp_is_a1(self):
        assert _level_for_xp(0) == "A1"

    def test_just_below_a2(self):
        assert _level_for_xp(499) == "A1"

    def test_exactly_a2(self):
        assert _level_for_xp(500) == "A2"

    def test_b1(self):
        assert _level_for_xp(1500) == "B1"

    def test_c2(self):
        assert _level_for_xp(13000) == "C2"

    def test_huge_xp(self):
        assert _level_for_xp(999999) == "C2"


# ---------------------------------------------------------------------------
# award_xp
# ---------------------------------------------------------------------------


class TestAwardXP:
    async def test_basic_award(self, db_session: AsyncSession, svc):
        result = await svc.award_xp(50, "lesson_complete", db_session)
        assert result["new_xp"] == 50
        assert result["level_changed"] is False

    async def test_level_transition(self, db_session: AsyncSession, svc):
        # Award enough to cross A1 -> A2 boundary
        await svc.award_xp(490, "warmup", db_session)
        result = await svc.award_xp(20, "push_over", db_session)
        assert result["new_xp"] == 510
        assert result["level_changed"] is True
        assert result["new_level"] == "A2"

    async def test_xp_event_recorded(self, db_session: AsyncSession, svc):
        await svc.award_xp(100, "test_reason", db_session)
        rows = (await db_session.execute(select(XPEvent))).scalars().all()
        assert len(rows) == 1
        assert rows[0].amount == 100
        assert rows[0].reason == "test_reason"

    async def test_cumulative_xp(self, db_session: AsyncSession, svc):
        await svc.award_xp(100, "a", db_session)
        result = await svc.award_xp(200, "b", db_session)
        assert result["new_xp"] == 300


# ---------------------------------------------------------------------------
# update_streak
# ---------------------------------------------------------------------------


class TestUpdateStreak:
    async def test_first_ever_streak(self, db_session: AsyncSession, svc):
        result = await svc.update_streak(db_session)
        assert result["streak"] == 1
        assert result["is_new_high"] is True

    async def test_same_day_no_increment(self, db_session: AsyncSession, svc):
        await svc.update_streak(db_session)
        result = await svc.update_streak(db_session)
        assert result["streak"] == 1

    async def test_consecutive_day_increments(self, db_session: AsyncSession, svc):
        # First day
        await svc.update_streak(db_session)
        # Simulate yesterday's last_active
        stats = await db_session.get(UserStats, 1)
        stats.last_active = datetime.utcnow() - timedelta(days=1)
        await db_session.commit()
        result = await svc.update_streak(db_session)
        assert result["streak"] == 2

    async def test_gap_resets_streak(self, db_session: AsyncSession, svc):
        await svc.update_streak(db_session)
        stats = await db_session.get(UserStats, 1)
        stats.streak_days = 10
        stats.last_active = datetime.utcnow() - timedelta(days=3)
        await db_session.commit()
        result = await svc.update_streak(db_session)
        assert result["streak"] == 1

    async def test_bonus_xp_capped_at_100(self, db_session: AsyncSession, svc):
        await svc.update_streak(db_session)
        stats = await db_session.get(UserStats, 1)
        stats.streak_days = 50
        stats.last_active = datetime.utcnow() - timedelta(days=1)
        await db_session.commit()
        result = await svc.update_streak(db_session)
        # streak goes to 51, bonus_xp = min(51*5, 100) = 100
        assert result["bonus_xp"] == 100


# ---------------------------------------------------------------------------
# check_and_award_achievements
# ---------------------------------------------------------------------------


class TestCheckAndAwardAchievements:
    async def test_no_achievements_initially(self, db_session: AsyncSession, svc):
        newly = await svc.check_and_award_achievements("lesson_complete", db_session)
        assert newly == []

    async def test_first_lesson_achievement(self, db_session: AsyncSession, svc):
        # Seed a completed lesson
        db_session.add(
            LessonProgress(
                lesson_id=1,
                completed=True,
                score=80.0,
                attempts=1,
                last_attempt_at=datetime.utcnow(),
            )
        )
        await db_session.commit()
        newly = await svc.check_and_award_achievements("lesson_complete", db_session)
        ids = [a.achievement_id for a in newly]
        assert "first_lesson" in ids

    async def test_idempotent_no_duplicates(self, db_session: AsyncSession, svc):
        db_session.add(
            LessonProgress(
                lesson_id=1,
                completed=True,
                score=80.0,
                attempts=1,
                last_attempt_at=datetime.utcnow(),
            )
        )
        await db_session.commit()
        first = await svc.check_and_award_achievements("lesson_complete", db_session)
        second = await svc.check_and_award_achievements("lesson_complete", db_session)
        assert len(first) > 0
        assert len(second) == 0

    async def test_pronunciation_90_achievement(self, db_session: AsyncSession, svc):
        db_session.add(
            PronunciationSession(
                reference_text="test",
                overall_score=92.0,
                pronunciation_score=91.0,
                fluency_score=90.0,
                accuracy_score=93.0,
            )
        )
        await db_session.commit()
        newly = await svc.check_and_award_achievements("pronunciation", db_session)
        ids = [a.achievement_id for a in newly]
        assert "pronunciation_90" in ids

    async def test_exam_pass_achievement(self, db_session: AsyncSession, svc):
        db_session.add(
            ExamAttempt(
                exam_level="B1",
                section="Lesen",
                score=80.0,
                max_score=100.0,
                passed=True,
                answers_json={},
            )
        )
        await db_session.commit()
        newly = await svc.check_and_award_achievements("exam", db_session)
        ids = [a.achievement_id for a in newly]
        assert "exam_pass" in ids

    async def test_level_up_achievement(self, db_session: AsyncSession, svc):
        # Give enough XP to be A2
        await svc.award_xp(600, "test", db_session)
        newly = await svc.check_and_award_achievements("xp", db_session)
        ids = [a.achievement_id for a in newly]
        assert "level_up" in ids


# ---------------------------------------------------------------------------
# get_achievements
# ---------------------------------------------------------------------------


class TestGetAchievements:
    async def test_returns_all_achievement_defs(self, db_session: AsyncSession, svc):
        result = await svc.get_achievements(db_session)
        assert len(result) == len(ACHIEVEMENTS)

    async def test_earned_flag(self, db_session: AsyncSession, svc):
        # Seed one earned achievement
        db_session.add(
            Achievement(
                achievement_id="first_lesson",
                title="Erster Schritt",
                emoji="🎓",
                earned_at=datetime.utcnow(),
            )
        )
        await db_session.commit()
        result = await svc.get_achievements(db_session)
        earned = [a for a in result if a["earned"]]
        locked = [a for a in result if not a["earned"]]
        assert len(earned) == 1
        assert earned[0]["achievement_id"] == "first_lesson"
        assert earned[0]["earned_at"] is not None
        assert len(locked) == len(ACHIEVEMENTS) - 1
