"""FastAPI entrypoint for the Sprechen AI backend."""
from __future__ import annotations

import os
from contextlib import asynccontextmanager

import structlog
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from core.config import get_settings
from core.logger import RequestLoggingMiddleware, configure_logging
from models.database import AsyncSessionLocal, init_db
from models.orm_models import Lesson
from routers.admin_routes import router as admin_router
from routers.ai_routes import conversation_router, voice_router
from routers.analytics_routes import router as analytics_router
from routers.exam_routes import router as exam_router
from routers.lesson_routes import router as lesson_router
from routers.progress_routes import router as progress_router
from sqlalchemy import func, select

logger = structlog.get_logger(__name__)


async def _maybe_seed_lessons() -> None:
    """Seed default lessons if the table is empty and a seeder module exists."""
    try:
        from data.lesson_seeds import seed_default_lessons  # type: ignore
    except Exception:
        return

    async with AsyncSessionLocal() as session:
        count = (await session.execute(select(func.count(Lesson.id)))).scalar_one()
        if count and count > 0:
            return
        try:
            await seed_default_lessons(session)
            await session.commit()
            logger.info("seeded_default_lessons")
        except Exception as exc:
            logger.error("seed_failed", error=str(exc))
            await session.rollback()


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    os.makedirs(settings.audio_cache_dir, exist_ok=True)
    await init_db()
    await _maybe_seed_lessons()
    logger.info(
        "sprechen_startup",
        app=settings.app_name,
        cache_dir=settings.audio_cache_dir,
    )
    yield
    logger.info("sprechen_shutdown")


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(debug=settings.debug)
    app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

    app.add_middleware(RequestLoggingMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://localhost:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    os.makedirs(settings.audio_cache_dir, exist_ok=True)
    app.mount(
        "/audio",
        StaticFiles(directory=settings.audio_cache_dir),
        name="audio",
    )

    app.include_router(voice_router)
    app.include_router(conversation_router)
    app.include_router(progress_router)
    app.include_router(lesson_router)
    app.include_router(exam_router)
    app.include_router(analytics_router)
    app.include_router(admin_router)

    @app.get("/health")
    async def health() -> dict:
        return {
            "status": "ok",
            "services": {
                "stt": "groq-whisper-large-v3",
                "pronunciation": "whisper+groq-llm",
                "llm": settings.groq_llm_model,
                "tts": "edge-tts",
            },
        }

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
