"""HTTP routes for lessons."""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import get_db
from models.lesson_schemas import LessonDetail
from services.curriculum_service import get_curriculum_service

router = APIRouter(prefix="/api/v1/lessons", tags=["lessons"])


class SubmitExerciseRequest(BaseModel):
    exercise_index: int = Field(..., ge=0)
    user_answer: str


class GenerateExerciseRequest(BaseModel):
    exercise_type: str


class CompleteLessonRequest(BaseModel):
    score: float = Field(..., ge=0, le=100)


@router.get("/")
async def list_all(db: AsyncSession = Depends(get_db)) -> dict:
    return await get_curriculum_service().get_all_lessons(db)


@router.get("/level/{level}")
async def list_by_level(level: str, db: AsyncSession = Depends(get_db)) -> List[dict]:
    return await get_curriculum_service().get_lessons_for_level(level, db)


@router.get("/scenario/{scenario}")
async def list_by_scenario(
    scenario: str, db: AsyncSession = Depends(get_db)
) -> List[dict]:
    return await get_curriculum_service().get_lessons_for_scenario(scenario, db)


@router.get("/{lesson_id}", response_model=LessonDetail)
async def get_lesson(
    lesson_id: int, db: AsyncSession = Depends(get_db)
) -> LessonDetail:
    return await get_curriculum_service().get_lesson(lesson_id, db)


@router.post("/{lesson_id}/submit-exercise")
async def submit_exercise(
    lesson_id: int,
    body: SubmitExerciseRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    return await get_curriculum_service().submit_exercise(
        lesson_id, body.exercise_index, body.user_answer, db
    )


@router.post("/{lesson_id}/generate-exercise")
async def generate_exercise(
    lesson_id: int,
    body: GenerateExerciseRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    return await get_curriculum_service().generate_exercise(
        lesson_id, body.exercise_type, db
    )


@router.post("/{lesson_id}/complete")
async def complete_lesson(
    lesson_id: int,
    body: CompleteLessonRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    # Delegate to the progress router's logic by importing locally to avoid cycles.
    from routers.progress_routes import (
        LessonCompleteRequest,
        complete_lesson as progress_complete_lesson,
    )

    return await progress_complete_lesson(
        lesson_id, LessonCompleteRequest(score=body.score), db
    )
