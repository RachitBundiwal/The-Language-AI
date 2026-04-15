"""HTTP-level tests for analytics + admin routers."""
from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from main import app
from models.database import get_db
from routers.analytics_routes import _analytics, _gamification

client = TestClient(app)


# ---------------------------------------------------------------------------
# Helpers: override FastAPI dependencies
# ---------------------------------------------------------------------------


def _make_fake_analytics(**overrides):
    """Build a mock AnalyticsService with sensible defaults."""
    svc = AsyncMock()
    svc.get_weekly_stats.return_value = overrides.get("weekly", {
        "lessons_this_week": 3,
        "minutes_studied": 45,
        "vocab_learned": 12,
        "pronunciation_sessions": 5,
        "avg_pronunciation": 82.5,
        "xp_earned": 150,
        "per_day": [],
    })
    svc.get_pronunciation_trend.return_value = overrides.get("pron_trend", [
        {"date": "2026-04-01", "avg_score": 85.0, "session_count": 2}
    ])
    svc.get_study_heatmap.return_value = overrides.get("heatmap", [
        {"date": "2026-04-09", "count": 5, "level": 2}
    ])
    svc.get_level_progression.return_value = overrides.get("progression", [
        {"date": "2026-04-09T12:00:00", "cumulative_xp": 500, "level_at_time": "A2"}
    ])
    return svc


def _make_fake_gamification():
    svc = AsyncMock()
    svc.get_achievements.return_value = [
        {
            "achievement_id": "first_lesson",
            "title": "Erster Schritt",
            "emoji": "🎓",
            "description": "Erste Lektion abgeschlossen",
            "earned": True,
            "earned_at": "2026-04-01T10:00:00",
        }
    ]
    return svc


class _FakeDB:
    """Sentinel object that quacks enough to pass through Depends(get_db)."""
    pass


# ---------------------------------------------------------------------------
# Analytics routes
# ---------------------------------------------------------------------------


class TestAnalyticsRoutes:
    def setup_method(self):
        self.fake_analytics = _make_fake_analytics()
        self.fake_gamification = _make_fake_gamification()
        app.dependency_overrides[_analytics] = lambda: self.fake_analytics
        app.dependency_overrides[_gamification] = lambda: self.fake_gamification
        app.dependency_overrides[get_db] = lambda: _FakeDB()

    def teardown_method(self):
        app.dependency_overrides.clear()

    def test_weekly_stats(self):
        resp = client.get("/api/v1/analytics/weekly")
        assert resp.status_code == 200
        data = resp.json()
        assert data["lessons_this_week"] == 3

    def test_pronunciation_trend(self):
        resp = client.get("/api/v1/analytics/pronunciation-trend?days=7")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["avg_score"] == 85.0

    def test_pronunciation_trend_validation(self):
        resp = client.get("/api/v1/analytics/pronunciation-trend?days=0")
        assert resp.status_code == 422  # ge=1 validation

    def test_heatmap(self):
        resp = client.get("/api/v1/analytics/heatmap")
        assert resp.status_code == 200
        data = resp.json()
        assert data[0]["level"] == 2

    def test_xp_progression(self):
        resp = client.get("/api/v1/analytics/xp-progression")
        assert resp.status_code == 200
        data = resp.json()
        assert "points" in data
        assert "thresholds" in data
        assert data["thresholds"]["A1"] == 0
        assert data["thresholds"]["C2"] == 13000

    def test_achievements(self):
        resp = client.get("/api/v1/analytics/achievements")
        assert resp.status_code == 200
        data = resp.json()
        assert data[0]["earned"] is True
        assert data[0]["achievement_id"] == "first_lesson"


# ---------------------------------------------------------------------------
# Admin routes
# ---------------------------------------------------------------------------


class TestAdminRoutes:
    def teardown_method(self):
        app.dependency_overrides.clear()

    @patch("routers.admin_routes.os.path.isfile", return_value=False)
    def test_export_missing_db_returns_404(self, mock_isfile):
        resp = client.get("/api/v1/admin/export")
        assert resp.status_code == 404

    def test_export_returns_file(self, tmp_path):
        import routers.admin_routes as mod

        fake_db = tmp_path / "sprechen.db"
        fake_db.write_bytes(b"SQLITEDATA")
        original_path = mod._DB_PATH
        mod._DB_PATH = str(fake_db)
        try:
            resp = client.get("/api/v1/admin/export")
            assert resp.status_code == 200
            assert "application/octet-stream" in resp.headers.get("content-type", "")
            assert resp.content == b"SQLITEDATA"
        finally:
            mod._DB_PATH = original_path
