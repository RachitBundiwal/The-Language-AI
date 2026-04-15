"""Tests for core.logger RequestLoggingMiddleware."""
from __future__ import annotations

import asyncio
import time
from unittest.mock import MagicMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.responses import Response

from core.logger import RequestLoggingMiddleware


def _make_app() -> FastAPI:
    """Build a minimal FastAPI app with the middleware for testing."""
    test_app = FastAPI()
    test_app.add_middleware(RequestLoggingMiddleware)

    @test_app.get("/ok")
    async def ok_route():
        return {"status": "ok"}

    @test_app.get("/slow")
    async def slow_route():
        await asyncio.sleep(0)  # yields but doesn't actually wait
        return {"status": "slow"}

    @test_app.get("/error")
    async def error_route():
        raise RuntimeError("boom")

    @test_app.get("/server-error")
    async def server_error_route():
        return Response(status_code=500, content="internal error")

    return test_app


class TestRequestLoggingMiddleware:
    def setup_method(self):
        self.app = _make_app()
        self.client = TestClient(self.app, raise_server_exceptions=False)

    @patch("core.logger._logger")
    def test_normal_request_logs_info(self, mock_logger):
        resp = self.client.get("/ok")
        assert resp.status_code == 200
        mock_logger.info.assert_called()
        call_args = mock_logger.info.call_args
        assert call_args[0][0] == "request"

    @patch("core.logger._logger")
    def test_request_includes_method_and_path(self, mock_logger):
        self.client.get("/ok")
        call_kwargs = mock_logger.info.call_args[1]
        assert call_kwargs["method"] == "GET"
        assert call_kwargs["path"] == "/ok"
        assert "duration_ms" in call_kwargs

    @patch("core.logger._logger")
    def test_error_request_logs_error(self, mock_logger):
        resp = self.client.get("/error")
        assert resp.status_code == 500
        mock_logger.error.assert_called()
        call_args = mock_logger.error.call_args
        assert call_args[0][0] == "request_failed"
        assert "traceback" in call_args[1]

    @patch("core.logger._logger")
    def test_5xx_response_logs_server_error(self, mock_logger):
        resp = self.client.get("/server-error")
        assert resp.status_code == 500
        mock_logger.error.assert_called()
        call_args = mock_logger.error.call_args
        assert call_args[0][0] == "request_server_error"

    @patch("core.logger._logger")
    def test_slow_request_detection(self, mock_logger):
        """Simulate a slow request by making time.monotonic jump 3s between calls."""
        import core.logger as logger_mod

        original_monotonic = time.monotonic
        call_count = [0]

        def fake_monotonic():
            call_count[0] += 1
            real = original_monotonic()
            # On even calls (measuring end-time), add 3 seconds
            if call_count[0] % 2 == 0:
                return real + 3.0
            return real

        saved = logger_mod.time
        try:
            # Replace the `time` module reference inside core.logger
            fake_time = MagicMock(wraps=time)
            fake_time.monotonic = fake_monotonic
            logger_mod.time = fake_time
            resp = self.client.get("/ok")
        finally:
            logger_mod.time = saved

        assert resp.status_code == 200
        mock_logger.warning.assert_called()
        call_args = mock_logger.warning.call_args
        assert call_args[0][0] == "request_slow"
