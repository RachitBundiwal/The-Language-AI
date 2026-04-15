"""HTTP routes for analytics, gamification achievements, and progression."""
from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import get_db
from services.analytics_service import (
    AnalyticsService,
    get_analytics_service,
)
from services.gamification_service import (
    GamificationService,
    get_gamification_service,
)

router = APIRouter(prefix="/api/v1/analytics", tags=["analytics"])


def _analytics() -> AnalyticsService:
    return get_analytics_service()


def _gamification() -> GamificationService:
    return get_gamification_service()


@router.get("/full")
async def full_stats(
    db: AsyncSession = Depends(get_db),
    service: AnalyticsService = Depends(_analytics),
) -> Dict[str, Any]:
    return await service.get_full_stats(db)


@router.get("/weekly")
async def weekly_stats(
    db: AsyncSession = Depends(get_db),
    service: AnalyticsService = Depends(_analytics),
) -> Dict[str, Any]:
    return await service.get_weekly_stats(db)


@router.get("/pronunciation-trend")
async def pronunciation_trend(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
    service: AnalyticsService = Depends(_analytics),
) -> List[Dict[str, Any]]:
    return await service.get_pronunciation_trend(days, db)


@router.get("/heatmap")
async def study_heatmap(
    db: AsyncSession = Depends(get_db),
    service: AnalyticsService = Depends(_analytics),
) -> List[Dict[str, Any]]:
    return await service.get_study_heatmap(db)


@router.get("/xp-progression")
async def xp_progression(
    db: AsyncSession = Depends(get_db),
    service: AnalyticsService = Depends(_analytics),
) -> Dict[str, Any]:
    points = await service.get_level_progression(db)
    return {
        "points": points,
        "thresholds": AnalyticsService.level_thresholds(),
    }


@router.get("/achievements")
async def achievements(
    db: AsyncSession = Depends(get_db),
    service: GamificationService = Depends(_gamification),
) -> List[Dict[str, Any]]:
    return await service.get_achievements(db)
