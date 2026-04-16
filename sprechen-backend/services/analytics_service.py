"""Analytics service: weekly stats, trends, heatmap, XP progression."""
from __future__ import annotations

import asyncio
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.cache import cache_response
from models.database import AsyncSessionLocal
from models.orm_models import (
    Achievement,
    GrammarError,
    Lesson,
    LessonProgress,
    PronunciationSession,
    VocabularyCard,
    XPEvent,
)
from services.exam_service import ExamService
from services.gamification_service import (
    ACHIEVEMENTS,
    XP_THRESHOLDS,
    _level_for_xp,
)


def _heatmap_level(count: int) -> int:
    if count <= 0:
        return 0
    if count <= 2:
        return 1
    if count <= 5:
        return 2
    if count <= 10:
        return 3
    return 4


class AnalyticsService:
    def __init__(self, exam_service: Optional[ExamService] = None) -> None:
        self._exam_service: Optional[ExamService] = exam_service

    @property
    def exam_service(self) -> ExamService:
        if self._exam_service is None:
            self._exam_service = ExamService()
        return self._exam_service

    # ------------------------------------------------------------------
    @cache_response(ttl=60)
    async def get_full_stats(self, db: AsyncSession) -> Dict[str, Any]:
        # Each sub-task needs its own AsyncSession — sessions are not safe
        # to share across concurrent tasks.
        async def _isolated(coro_factory):
            async with AsyncSessionLocal() as session:
                return await coro_factory(session)

        weekly, pron_trend, readiness, achievements, weak_grammar = (
            await asyncio.gather(
                _isolated(lambda s: self.get_weekly_stats(s)),
                _isolated(lambda s: self.get_pronunciation_trend(30, s)),
                _isolated(lambda s: self._exam_readiness_safe(s)),
                _isolated(lambda s: self._achievement_summary(s)),
                _isolated(lambda s: self._grammar_weak_areas(s)),
            )
        )
        return {
            "weekly_stats": weekly,
            "pronunciation_trend": pron_trend,
            "exam_readiness": readiness,
            "achievements": achievements,
            "grammar_weak_areas": weak_grammar,
        }

    async def _exam_readiness_safe(self, db: AsyncSession) -> Dict[str, Any]:
        try:
            r = await self.exam_service.get_exam_readiness(db)
            return r.model_dump() if hasattr(r, "model_dump") else dict(r)
        except Exception:
            return {
                "overall": 0.0,
                "by_section": {},
                "recommendation": "",
                "predicted_weeks": 0,
            }

    async def _achievement_summary(self, db: AsyncSession) -> Dict[str, Any]:
        earned_count = int(
            (await db.execute(select(func.count(Achievement.id)))).scalar_one()
            or 0
        )
        return {
            "earned": earned_count,
            "total": len(ACHIEVEMENTS),
        }

    async def _grammar_weak_areas(
        self, db: AsyncSession
    ) -> List[Dict[str, Any]]:
        rows = (
            await db.execute(
                select(
                    GrammarError.rule_id,
                    func.count(GrammarError.id).label("c"),
                )
                .group_by(GrammarError.rule_id)
                .order_by(desc("c"))
                .limit(5)
            )
        ).all()
        return [{"rule_id": r[0], "count": int(r[1])} for r in rows]

    # ------------------------------------------------------------------
    async def get_weekly_stats(self, db: AsyncSession) -> Dict[str, Any]:
        now = datetime.utcnow()
        week_start = now - timedelta(days=7)

        lessons_this_week_rows = (
            await db.execute(
                select(LessonProgress.lesson_id)
                .where(LessonProgress.completed.is_(True))
                .where(LessonProgress.last_attempt_at >= week_start)
            )
        ).all()
        lesson_ids = [r[0] for r in lessons_this_week_rows]
        lessons_this_week = len(lesson_ids)

        minutes_studied = 0
        if lesson_ids:
            min_rows = (
                await db.execute(
                    select(Lesson.id, Lesson.content_json).where(
                        Lesson.id.in_(lesson_ids)
                    )
                )
            ).all()
            for _lid, content in min_rows:
                if isinstance(content, dict):
                    minutes_studied += int(
                        content.get("estimated_minutes") or 0
                    )

        vocab_learned = int(
            (
                await db.execute(
                    select(func.count(VocabularyCard.id)).where(
                        VocabularyCard.created_at >= week_start
                    )
                )
            ).scalar_one()
            or 0
        )

        pronunciation_sessions = int(
            (
                await db.execute(
                    select(func.count(PronunciationSession.id)).where(
                        PronunciationSession.created_at >= week_start
                    )
                )
            ).scalar_one()
            or 0
        )

        avg_pron: Optional[float] = None
        if pronunciation_sessions > 0:
            avg = (
                await db.execute(
                    select(func.avg(PronunciationSession.overall_score)).where(
                        PronunciationSession.created_at >= week_start
                    )
                )
            ).scalar_one()
            avg_pron = round(float(avg or 0.0), 2)

        xp_earned = int(
            (
                await db.execute(
                    select(func.coalesce(func.sum(XPEvent.amount), 0)).where(
                        XPEvent.created_at >= week_start
                    )
                )
            ).scalar_one()
            or 0
        )

        # Per-day breakdown for the last 7 days (oldest -> newest)
        per_day: List[Dict[str, Any]] = []
        today = now.date()
        for offset in range(6, -1, -1):
            day = today - timedelta(days=offset)
            start = datetime.combine(day, datetime.min.time())
            end = start + timedelta(days=1)
            count = int(
                (
                    await db.execute(
                        select(func.count(LessonProgress.id))
                        .where(LessonProgress.completed.is_(True))
                        .where(LessonProgress.last_attempt_at >= start)
                        .where(LessonProgress.last_attempt_at < end)
                    )
                ).scalar_one()
                or 0
            )
            per_day.append({"date": day.isoformat(), "lessons": count})

        return {
            "lessons_this_week": lessons_this_week,
            "minutes_studied": minutes_studied,
            "vocab_learned": vocab_learned,
            "pronunciation_sessions": pronunciation_sessions,
            "avg_pronunciation": avg_pron,
            "xp_earned": xp_earned,
            "per_day": per_day,
        }

    # ------------------------------------------------------------------
    async def get_pronunciation_trend(
        self, days: int, db: AsyncSession
    ) -> List[Dict[str, Any]]:
        cutoff = datetime.utcnow() - timedelta(days=days)
        rows = (
            await db.execute(
                select(PronunciationSession.overall_score, PronunciationSession.created_at)
                .where(PronunciationSession.created_at >= cutoff)
                .order_by(PronunciationSession.created_at.asc())
            )
        ).all()

        buckets: Dict[str, List[float]] = {}
        for score, created in rows:
            if created is None:
                continue
            key = created.date().isoformat()
            buckets.setdefault(key, []).append(float(score or 0.0))

        return [
            {
                "date": d,
                "avg_score": round(sum(scores) / len(scores), 2),
                "session_count": len(scores),
            }
            for d, scores in sorted(buckets.items())
        ]

    # ------------------------------------------------------------------
    async def get_study_heatmap(
        self, db: AsyncSession
    ) -> List[Dict[str, Any]]:
        cutoff = datetime.utcnow() - timedelta(days=365)

        lesson_rows = (
            await db.execute(
                select(LessonProgress.last_attempt_at)
                .where(LessonProgress.completed.is_(True))
                .where(LessonProgress.last_attempt_at >= cutoff)
            )
        ).all()
        pron_rows = (
            await db.execute(
                select(PronunciationSession.created_at).where(
                    PronunciationSession.created_at >= cutoff
                )
            )
        ).all()
        vocab_rows = (
            await db.execute(
                select(VocabularyCard.created_at).where(
                    VocabularyCard.created_at >= cutoff
                )
            )
        ).all()

        counts: Dict[date, int] = {}
        for (ts,) in lesson_rows + pron_rows + vocab_rows:
            if ts is None:
                continue
            d = ts.date() if isinstance(ts, datetime) else ts
            counts[d] = counts.get(d, 0) + 1

        today = datetime.utcnow().date()
        out: List[Dict[str, Any]] = []
        for offset in range(364, -1, -1):
            d = today - timedelta(days=offset)
            c = counts.get(d, 0)
            out.append(
                {"date": d.isoformat(), "count": c, "level": _heatmap_level(c)}
            )
        return out

    # ------------------------------------------------------------------
    async def get_level_progression(
        self, db: AsyncSession
    ) -> List[Dict[str, Any]]:
        rows = (
            await db.execute(
                select(XPEvent.amount, XPEvent.created_at).order_by(
                    XPEvent.created_at.asc()
                )
            )
        ).all()

        cumulative = 0
        out: List[Dict[str, Any]] = []
        for amount, created in rows:
            cumulative += int(amount or 0)
            out.append(
                {
                    "date": (created or datetime.utcnow()).isoformat(),
                    "cumulative_xp": cumulative,
                    "level_at_time": _level_for_xp(cumulative),
                }
            )

        # Always include level boundaries so frontend can draw threshold lines
        return out

    @staticmethod
    def level_thresholds() -> Dict[str, int]:
        return dict(XP_THRESHOLDS)


_service: Optional[AnalyticsService] = None


def get_analytics_service() -> AnalyticsService:
    global _service
    if _service is None:
        _service = AnalyticsService()
    return _service
