"""Curriculum service: lesson lookup, exercise grading and generation, seeding."""
from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional

import structlog
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.cache import cache_response
from core.config import get_settings
from models.lesson_schemas import LessonDetail
from models.orm_models import Lesson, LessonProgress

logger = structlog.get_logger(__name__)


def _normalize(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())


class CurriculumService:
    def __init__(self) -> None:
        self._settings = get_settings()
        # Lazy import to avoid circular import with services package
        from groq import AsyncGroq

        self._client = AsyncGroq(api_key=self._settings.groq_api_key or "missing-key")

    # ---------- fetch ----------
    @cache_response(ttl=300)
    async def get_lesson(self, lesson_id: int, db: AsyncSession) -> LessonDetail:
        lesson = await db.get(Lesson, lesson_id)
        if lesson is None:
            raise HTTPException(status_code=404, detail="Lesson not found")
        content = dict(lesson.content_json or {})
        content.setdefault("id", lesson.id)
        content.setdefault("title", lesson.title)
        content.setdefault("level", lesson.level)
        content.setdefault("scenario", lesson.scenario)
        content.setdefault("topic", lesson.topic)
        return LessonDetail(**content)

    async def get_lessons_for_level(
        self, level: str, db: AsyncSession
    ) -> List[dict]:
        stmt = (
            select(Lesson, LessonProgress)
            .outerjoin(LessonProgress, LessonProgress.lesson_id == Lesson.id)
            .where(Lesson.level == level)
            .order_by(Lesson.order_index.asc(), Lesson.id.asc())
        )
        rows = (await db.execute(stmt)).all()
        return [self._lesson_row_to_dict(l, p) for l, p in rows]

    async def get_lessons_for_scenario(
        self, scenario: str, db: AsyncSession
    ) -> List[dict]:
        stmt = (
            select(Lesson, LessonProgress)
            .outerjoin(LessonProgress, LessonProgress.lesson_id == Lesson.id)
            .where(Lesson.scenario == scenario)
            .order_by(Lesson.order_index.asc(), Lesson.id.asc())
        )
        rows = (await db.execute(stmt)).all()
        return [self._lesson_row_to_dict(l, p) for l, p in rows]

    async def get_all_lessons(self, db: AsyncSession) -> Dict[str, List[dict]]:
        stmt = (
            select(Lesson, LessonProgress)
            .outerjoin(LessonProgress, LessonProgress.lesson_id == Lesson.id)
            .order_by(Lesson.level.asc(), Lesson.order_index.asc(), Lesson.id.asc())
        )
        rows = (await db.execute(stmt)).all()
        grouped: Dict[str, List[dict]] = {}
        for lesson, progress in rows:
            grouped.setdefault(lesson.level, []).append(
                self._lesson_row_to_dict(lesson, progress)
            )
        return grouped

    @staticmethod
    def _lesson_row_to_dict(lesson: Lesson, progress: Optional[LessonProgress]) -> dict:
        content = lesson.content_json or {}
        return {
            "id": lesson.id,
            "title": lesson.title,
            "level": lesson.level,
            "scenario": lesson.scenario,
            "topic": lesson.topic,
            "estimated_minutes": int(content.get("estimated_minutes", 10)),
            "completed": bool(progress.completed) if progress else False,
            "score": progress.score if progress else None,
            "attempts": int(progress.attempts) if progress else 0,
        }

    # ---------- grading ----------
    async def submit_exercise(
        self,
        lesson_id: int,
        exercise_index: int,
        user_answer: str,
        db: AsyncSession,
    ) -> dict:
        lesson_detail = await self.get_lesson(lesson_id, db)
        if exercise_index < 0 or exercise_index >= len(lesson_detail.exercises):
            raise HTTPException(status_code=400, detail="Invalid exercise index")

        ex = lesson_detail.exercises[exercise_index]
        ex_type = ex.type

        if ex_type == "fill_in_blank":
            try:
                idx = int(user_answer)
            except (TypeError, ValueError):
                idx = -1
            correct = idx == ex.correct_index
            return {
                "correct": correct,
                "score": 100.0 if correct else 0.0,
                "explanation": ex.hint,
                "correct_answer": ex.options[ex.correct_index],
            }

        if ex_type == "multiple_choice":
            try:
                idx = int(user_answer)
            except (TypeError, ValueError):
                idx = -1
            correct = idx == ex.correct_index
            return {
                "correct": correct,
                "score": 100.0 if correct else 0.0,
                "explanation": ex.explanation,
                "correct_answer": ex.options[ex.correct_index],
            }

        if ex_type == "arrange_words":
            correct = _normalize(user_answer) == _normalize(ex.correct_sentence)
            return {
                "correct": correct,
                "score": 100.0 if correct else 0.0,
                "explanation": ex.hint,
                "correct_answer": ex.correct_sentence,
            }

        if ex_type == "translate":
            graded = await self._grade_translation(
                user_answer, ex.model_answer, ex.source_text
            )
            return {
                "correct": graded["score"] >= 70,
                "score": graded["score"],
                "explanation": graded["feedback"],
                "correct_answer": ex.model_answer,
            }

        if ex_type == "speaking_prompt":
            return {
                "correct": False,
                "score": 0.0,
                "explanation": "Use the voice exercise endpoint to record this answer.",
                "correct_answer": ex.prompt_text,
                "requires_voice": True,
            }

        if ex_type == "listening":
            return {
                "correct": False,
                "score": 0.0,
                "explanation": "Listening exercises are scored client-side per question.",
                "correct_answer": "",
            }

        raise HTTPException(status_code=400, detail=f"Unsupported exercise type {ex_type}")

    async def _grade_translation(
        self, user_answer: str, model_answer: str, source: str
    ) -> dict:
        prompt = (
            "Du bist ein Deutschlehrer. Bewerte die Übersetzung eines Lernenden.\n"
            f"Quelltext: {source}\n"
            f"Musterlösung: {model_answer}\n"
            f"Antwort des Lernenden: {user_answer}\n"
            "Gib NUR JSON zurück: {\"score\": 0-100, \"feedback\": \"kurzes Feedback auf Deutsch\"}"
        )
        try:
            completion = await self._client.chat.completions.create(
                model=self._settings.groq_llm_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=300,
                response_format={"type": "json_object"},
            )
            raw = completion.choices[0].message.content or "{}"
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip())
            data = json.loads(cleaned)
            return {
                "score": float(data.get("score", 0)),
                "feedback": data.get("feedback", ""),
            }
        except Exception as exc:
            logger.error("translate_grade_failed", error=str(exc))
            # Fallback: simple normalized equality
            ok = _normalize(user_answer) == _normalize(model_answer)
            return {
                "score": 100.0 if ok else 50.0,
                "feedback": "Automatische Bewertung nicht verfügbar.",
            }

    # ---------- exercise generation ----------
    async def generate_exercise(
        self, lesson_id: int, exercise_type: str, db: AsyncSession
    ) -> dict:
        lesson_detail = await self.get_lesson(lesson_id, db)
        vocab_words = ", ".join(
            v.word for v in lesson_detail.vocabulary_list[:15]
        )
        prompt = (
            f"Erstelle eine NEUE Übung vom Typ '{exercise_type}' für eine Deutschlektion.\n"
            f"Niveau: {lesson_detail.level}\n"
            f"Szenario: {lesson_detail.scenario}\n"
            f"Thema: {lesson_detail.topic}\n"
            f"Verfügbarer Wortschatz: {vocab_words}\n\n"
            "Gib NUR JSON zurück, das genau einem dieser Schemata entspricht:\n"
            "fill_in_blank: {\"type\":\"fill_in_blank\",\"sentence_with_blank\":\"...\",\"options\":[\"a\",\"b\",\"c\",\"d\"],\"correct_index\":0,\"hint\":\"...\"}\n"
            "multiple_choice: {\"type\":\"multiple_choice\",\"question\":\"...\",\"options\":[...],\"correct_index\":0,\"explanation\":\"...\"}\n"
            "arrange_words: {\"type\":\"arrange_words\",\"scrambled_words\":[...],\"correct_sentence\":\"...\",\"hint\":\"...\"}\n"
            "translate: {\"type\":\"translate\",\"source_text\":\"...\",\"source_lang\":\"en\",\"target_lang\":\"de\",\"model_answer\":\"...\"}\n"
            "speaking_prompt: {\"type\":\"speaking_prompt\",\"prompt_text\":\"...\",\"expected_topic\":\"...\",\"min_words\":20}\n"
        )
        try:
            completion = await self._client.chat.completions.create(
                model=self._settings.groq_llm_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=600,
                response_format={"type": "json_object"},
            )
            raw = completion.choices[0].message.content or "{}"
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip())
            data = json.loads(cleaned)
            data.setdefault("type", exercise_type)
            return data
        except Exception as exc:
            logger.error("generate_exercise_failed", error=str(exc))
            return {
                "type": exercise_type,
                "error": "Generation failed. Please try again.",
            }

    # ---------- seeding ----------
    async def seed_all_lessons(self, db: AsyncSession) -> int:
        from data.lesson_seeds import LESSONS

        existing_titles = {
            row[0]
            for row in (await db.execute(select(Lesson.title))).all()
        }

        added = 0
        for index, lesson_dict in enumerate(LESSONS):
            title = lesson_dict["title"]
            if title in existing_titles:
                continue
            content = dict(lesson_dict)
            db.add(
                Lesson(
                    title=title,
                    level=content["level"],
                    scenario=content["scenario"],
                    topic=content["topic"],
                    content_json=content,
                    order_index=index,
                )
            )
            added += 1

        if added:
            await db.commit()
        logger.info("curriculum_seeded", added=added)
        return added


_curriculum_service: Optional[CurriculumService] = None


def get_curriculum_service() -> CurriculumService:
    global _curriculum_service
    if _curriculum_service is None:
        _curriculum_service = CurriculumService()
    return _curriculum_service
