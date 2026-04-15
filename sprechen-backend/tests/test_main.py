"""Tests for the FastAPI application wiring in main.py."""
from __future__ import annotations

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    services = body["services"]
    for key in ("stt", "pronunciation", "llm", "tts"):
        assert key in services


def test_cors_allows_vite_origin() -> None:
    r = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert r.status_code in (200, 204)
    assert r.headers.get("access-control-allow-origin") == "http://localhost:5173"


def test_cors_allows_localhost_3000() -> None:
    r = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert r.status_code in (200, 204)
    assert r.headers.get("access-control-allow-origin") == "http://localhost:3000"


def test_audio_static_mount_exists() -> None:
    # Unknown audio file should 404 (not 500), proving the mount is wired.
    r = client.get("/audio/does-not-exist.mp3")
    assert r.status_code == 404


def test_routers_are_registered() -> None:
    paths = {route.path for route in app.routes}
    assert "/api/v1/voice/transcribe" in paths
    assert "/api/v1/voice/score-pronunciation" in paths
    assert "/api/v1/voice/full-exercise" in paths
    assert "/api/v1/voice/tts" in paths
    assert "/api/v1/voice/voices" in paths
    assert "/api/v1/conversation/chat" in paths
    assert "/api/v1/conversation/chat/stream" in paths
    assert "/api/v1/conversation/evaluate-writing" in paths
    assert "/api/v1/conversation/generate-dialogue" in paths
