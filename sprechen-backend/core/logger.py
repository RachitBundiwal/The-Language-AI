"""Structured logging configuration and FastAPI request-log middleware."""
from __future__ import annotations

import logging
import logging.handlers
import os
import time
import traceback
from typing import Callable

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

_LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
_LOG_FILE = os.path.join(_LOG_DIR, "sprechen.log")

_configured = False


def configure_logging(debug: bool = True) -> None:
    """Configure structlog + stdlib logging once at startup."""
    global _configured
    if _configured:
        return

    os.makedirs(_LOG_DIR, exist_ok=True)

    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
    ]

    structlog.configure(
        processors=shared_processors
        + [
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    console_formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.dev.ConsoleRenderer(colors=True)
            if debug
            else structlog.processors.JSONRenderer(),
        ],
    )

    file_formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.processors.JSONRenderer(),
        ],
    )

    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(logging.INFO)

    console = logging.StreamHandler()
    console.setFormatter(console_formatter)
    root.addHandler(console)

    file_handler = logging.handlers.RotatingFileHandler(
        _LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(file_formatter)
    root.addHandler(file_handler)

    # Tame noisy libraries
    for noisy in ("uvicorn.access", "httpx", "sqlalchemy.engine"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    _configured = True


def get_logger(name: str) -> structlog.BoundLogger:
    if not _configured:
        configure_logging()
    return structlog.get_logger(name)


# ---------------------------------------------------------------------------
# FastAPI middleware
# ---------------------------------------------------------------------------

_logger = structlog.get_logger("sprechen.http")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable
    ) -> Response:
        start = time.monotonic()
        method = request.method
        path = request.url.path
        try:
            response = await call_next(request)
        except Exception as exc:
            duration_ms = int((time.monotonic() - start) * 1000)
            _logger.error(
                "request_failed",
                method=method,
                path=path,
                duration_ms=duration_ms,
                error=str(exc),
                traceback=traceback.format_exc(),
            )
            raise

        duration_ms = int((time.monotonic() - start) * 1000)
        status = response.status_code

        payload = {
            "method": method,
            "path": path,
            "status_code": status,
            "duration_ms": duration_ms,
        }

        if status >= 500:
            _logger.error("request_server_error", **payload)
        elif duration_ms > 2000:
            _logger.warning("request_slow", **payload)
        else:
            _logger.info("request", **payload)

        return response
