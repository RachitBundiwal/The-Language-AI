"""Tests for services.analytics_service."""
from __future__ import annotations

from datetime import datetime, timedelta

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from core.cache import _default_cache
from models.orm_models import (
    LessonProgress,
    PronunciationSession,
    VocabularyCard,
    XPEvent,
)
from services.analytics_service import AnalyticsService, _heatmap_level

from tests.conftest_db import db_session  # noqa: F401


@pytest.fixture
def svc() -> AnalyticsService:
    return AnalyticsService()


@pytest.fixture(autouse=True)
def clear_cache():
    _default_cache.clear()
    yield
    _default_cache.clear()


# ---------------------------------------------------------------------------
# _heatmap_level
# ---------------------------------------------------------------------------


class TestHeatmapLevel:
    def test_zero(self):
        assert _heatmap_level(0) == 0

    def test_low(self):
        assert _heatmap_level(1) == 1
        assert _heatmap_level(2) == 1

    def test_medium(self):
        assert _heatmap_level(3) == 2
        assert _heatmap_level(5) == 2

    def test_high(self):
        assert _heatmap_level(6) == 3
        assert _heatmap_level(10) == 3

    def test_very_high(self):
        assert _heatmap_level(11) == 4
        assert _heatmap_level(999) == 4

    def test_negative(self):
        assert _heatmap_level(-5) == 0


# ---------------------------------------------------------------------------
# get_weekly_stats
# ---------------------------------------------------------------------------


class TestGetWeeklyStats:
    async def test_empty_db(self, db_session: AsyncSession, svc):
        result = await svc.get_weekly_stats(db_session)
        assert result["lessons_this_week"] == 0
        assert result["vocab_learned"] == 0
        assert result["pronunciation_sessions"] == 0
        assert result["xp_earned"] == 0
        assert result["avg_pronunciation"] is None
        assert len(result["per_day"]) == 7

    async def test_counts_recent_lessons(self, db_session: AsyncSession, svc):
        now = datetime.utcnow()
        db_session.add(
            LessonProgress(
                lesson_id=1,
                completed=True,
                score=80.0,
                attempts=1,
                last_attempt_at=now - timedelta(hours=2),
            )
        )
        db_session.add(
            LessonProgress(
                lesson_id=2,
                completed=True,
                score=70.0,
                attempts=1,
                last_attempt_at=now - timedelta(days=10),
            )
        )
        await db_session.commit()
        result = await svc.get_weekly_stats(db_session)
        assert result["lessons_this_week"] == 1

    async def test_per_day_has_7_entries(self, db_session: AsyncSession, svc):
        result = await svc.get_weekly_stats(db_session)
        assert len(result["per_day"]) == 7
        for entry in result["per_day"]:
            assert "date" in entry
            assert "lessons" in entry

    async def test_xp_earned_sums_recent(self, db_session: AsyncSession, svc):
        now = datetime.utcnow()
        db_session.add(XPEvent(amount=50, reason="a", created_at=now - timedelta(hours=1)))
        db_session.add(XPEvent(amount=30, reason="b", created_at=now - timedelta(hours=2)))
        db_session.add(XPEvent(amount=999, reason="old", created_at=now - timedelta(days=30)))
        await db_session.commit()
        result = await svc.get_weekly_stats(db_session)
        assert result["xp_earned"] == 80


# ---------------------------------------------------------------------------
# get_pronunciation_trend
# ---------------------------------------------------------------------------


class TestGetPronunciationTrend:
    async def test_empty(self, db_session: AsyncSession, svc):
        result = await svc.get_pronunciation_trend(30, db_session)
        assert result == []

    async def test_buckets_by_date(self, db_session: AsyncSession, svc):
        now = datetime.utcnow()
        today = now.replace(hour=10, minute=0, second=0, microsecond=0)
        db_session.add(
            PronunciationSession(
                reference_text="a",
                overall_score=80.0,
                pronunciation_score=80.0,
                fluency_score=80.0,
                accuracy_score=80.0,
                created_at=today,
            )
        )
        db_session.add(
            PronunciationSession(
                reference_text="b",
                overall_score=90.0,
                pronunciation_score=90.0,
                fluency_score=90.0,
                accuracy_score=90.0,
                created_at=today + timedelta(hours=2),
            )
        )
        await db_session.commit()
        result = await svc.get_pronunciation_trend(30, db_session)
        assert len(result) == 1
        assert result[0]["avg_score"] == 85.0
        assert result[0]["session_count"] == 2


# ---------------------------------------------------------------------------
# get_study_heatmap
# ---------------------------------------------------------------------------


class TestGetStudyHeatmap:
    async def test_returns_365_cells(self, db_session: AsyncSession, svc):
        result = await svc.get_study_heatmap(db_session)
        assert len(result) == 365

    async def test_all_zeros_when_empty(self, db_session: AsyncSession, svc):
        result = await svc.get_study_heatmap(db_session)
        for cell in result:
            assert cell["count"] == 0
            assert cell["level"] == 0

    async def test_merges_sources(self, db_session: AsyncSession, svc):
        now = datetime.utcnow()
        db_session.add(
            LessonProgress(
                lesson_id=1,
                completed=True,
                score=80.0,
                attempts=1,
                last_attempt_at=now,
            )
        )
        db_session.add(
            PronunciationSession(
                reference_text="x",
                overall_score=85.0,
                pronunciation_score=85.0,
                fluency_score=85.0,
                accuracy_score=85.0,
                created_at=now,
            )
        )
        db_session.add(
            VocabularyCard(
                german_word="Hund",
                english_translation="dog",
                created_at=now,
            )
        )
        await db_session.commit()
        result = await svc.get_study_heatmap(db_session)
        today_str = now.date().isoformat()
        today_cell = next(c for c in result if c["date"] == today_str)
        assert today_cell["count"] == 3
        assert today_cell["level"] == 2  # 3 activities -> level 2


# ---------------------------------------------------------------------------
# get_level_progression
# ---------------------------------------------------------------------------


class TestGetLevelProgression:
    async def test_empty(self, db_session: AsyncSession, svc):
        result = await svc.get_level_progression(db_session)
        assert result == []

    async def test_cumulative_sum(self, db_session: AsyncSession, svc):
        now = datetime.utcnow()
        db_session.add(XPEvent(amount=100, reason="a", created_at=now - timedelta(hours=3)))
        db_session.add(XPEvent(amount=200, reason="b", created_at=now - timedelta(hours=2)))
        db_session.add(XPEvent(amount=300, reason="c", created_at=now - timedelta(hours=1)))
        await db_session.commit()
        result = await svc.get_level_progression(db_session)
        assert len(result) == 3
        assert result[0]["cumulative_xp"] == 100
        assert result[1]["cumulative_xp"] == 300
        assert result[2]["cumulative_xp"] == 600

    async def test_level_at_time(self, db_session: AsyncSession, svc):
        now = datetime.utcnow()
        db_session.add(XPEvent(amount=600, reason="big", created_at=now))
        await db_session.commit()
        result = await svc.get_level_progression(db_session)
        assert result[0]["level_at_time"] == "A2"


# ---------------------------------------------------------------------------
# level_thresholds (static)
# ---------------------------------------------------------------------------


class TestLevelThresholds:
    def test_returns_all_levels(self):
        t = AnalyticsService.level_thresholds()
        assert "A1" in t and "C2" in t
        assert t["A1"] == 0
        assert t["C2"] == 13000
