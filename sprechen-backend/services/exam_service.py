"""Goethe Institut exam simulator service."""
from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional

import structlog
from fastapi import HTTPException
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.cache import cache_response
from core.config import get_settings
from models.exam_schemas import (
    ExamPaper,
    ExamReadiness,
    ListeningPart,
    ReadingPart,
    SpeakingCard,
    WritingTask,
)
from models.orm_models import ExamAttempt
from models.schemas import TTSRequest
from services.pronunciation_service import get_pronunciation_service
from services.stt_service import get_stt_service
from services.tts_service import get_tts_service

logger = structlog.get_logger(__name__)


GOETHE_GRADES = {
    87: "Sehr gut",
    73: "Gut",
    60: "Befriedigend",
    0: "Nicht bestanden",
}

PASS_THRESHOLD = 60.0


def get_grade(percentage: float) -> str:
    """Return the highest Goethe grade label whose threshold percentage <= value."""
    for threshold in sorted(GOETHE_GRADES.keys(), reverse=True):
        if percentage >= threshold:
            return GOETHE_GRADES[threshold]
    return GOETHE_GRADES[0]


def _section_rate_for_level(level: str) -> str:
    level = (level or "").upper()
    if level in ("A1",):
        return "-20%"
    if level in ("A2", "B1"):
        return "-10%"
    return "+0%"


class ExamService:
    def __init__(self) -> None:
        self._settings = get_settings()
        from groq import AsyncGroq

        self._client = AsyncGroq(api_key=self._settings.groq_api_key or "missing-key")

    # ---------------------------------------------------------------
    # paper lookup
    # ---------------------------------------------------------------
    @cache_response(ttl=3600)
    def get_exam_paper(self, level: str, section: str) -> ExamPaper:
        from data.exam_papers import EXAM_PAPERS

        level_norm = (level or "").upper()
        section_aliases = {
            "lesen": "Lesen",
            "hören": "Hören",
            "hoeren": "Hören",
            "horen": "Hören",
            "schreiben": "Schreiben",
            "sprechen": "Sprechen",
        }
        section_norm = section_aliases.get((section or "").lower(), section)
        key = f"{level_norm}_{section_norm}"
        paper = EXAM_PAPERS.get(key)
        if paper is None:
            raise HTTPException(
                status_code=404, detail=f"Exam paper not found: {key}"
            )
        return ExamPaper(**paper)

    # ---------------------------------------------------------------
    # multiple-choice grading (Lesen / Hören)
    # ---------------------------------------------------------------
    async def grade_lesen(
        self, paper: ExamPaper, answers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return self._grade_mc(paper, answers)

    async def grade_hören(
        self, paper: ExamPaper, answers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return self._grade_mc(paper, answers)

    def _grade_mc(
        self, paper: ExamPaper, answers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        # Build a flat list of (global_qid, correct_index, part_number, points_per_q).
        flat: List[Dict[str, Any]] = []
        per_part: Dict[int, Dict[str, int]] = {}
        global_qid = 0
        for part in paper.parts:
            part_number = int(part.get("part_number", 0))
            questions = part.get("questions", []) or []
            max_points = int(part.get("max_points", len(questions)))
            points_per_q = (max_points / len(questions)) if questions else 0.0
            per_part[part_number] = {
                "part": part_number,
                "correct": 0,
                "total": len(questions),
                "max_points": max_points,
                "points": 0.0,
            }
            for q in questions:
                flat.append(
                    {
                        "qid": global_qid,
                        "correct_index": int(q.get("correct_index", -1)),
                        "part_number": part_number,
                        "points_per_q": points_per_q,
                    }
                )
                global_qid += 1

        answer_map = {int(a.get("question_id", -1)): int(a.get("answer_index", -1)) for a in answers}

        score = 0.0
        for entry in flat:
            given = answer_map.get(entry["qid"], -1)
            if given == entry["correct_index"]:
                score += entry["points_per_q"]
                bucket = per_part[entry["part_number"]]
                bucket["correct"] += 1
                bucket["points"] += entry["points_per_q"]

        max_score = float(paper.max_score)
        percentage = (score / max_score * 100.0) if max_score > 0 else 0.0
        return {
            "score": round(score, 1),
            "max_score": max_score,
            "percentage": round(percentage, 1),
            "passed": percentage >= PASS_THRESHOLD,
            "detailed": [
                {
                    "part": v["part"],
                    "correct": v["correct"],
                    "total": v["total"],
                    "points": round(v["points"], 1),
                    "max_points": v["max_points"],
                }
                for v in per_part.values()
            ],
        }

    # ---------------------------------------------------------------
    # writing grading (Groq + Goethe rubric)
    # ---------------------------------------------------------------
    async def grade_schreiben(
        self, paper: ExamPaper, submissions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        tasks_by_number: Dict[int, Dict[str, Any]] = {}
        for part in paper.parts:
            tasks_by_number[int(part.get("task_number", 0))] = part

        per_task_results: List[Dict[str, Any]] = []
        total_score = 0.0
        max_total = float(paper.max_score)

        for sub in submissions:
            task_number = int(sub.get("task_number", 0))
            user_text = (sub.get("text") or "").strip()
            task = tasks_by_number.get(task_number)
            if task is None:
                continue
            graded = await self._grade_writing_task(task, user_text)
            total_score += float(graded["score"])
            per_task_results.append(
                {
                    "task_number": task_number,
                    "score": graded["score"],
                    "max_points": int(task.get("max_points", 15)),
                    "feedback": graded["feedback"],
                    "strengths": graded["strengths"],
                    "improvements": graded["improvements"],
                    "rubric": graded.get("rubric", {}),
                }
            )

        percentage = (total_score / max_total * 100.0) if max_total > 0 else 0.0
        return {
            "score": round(total_score, 1),
            "max_score": max_total,
            "percentage": round(percentage, 1),
            "passed": percentage >= PASS_THRESHOLD,
            "per_task": per_task_results,
        }

    async def _grade_writing_task(
        self, task: Dict[str, Any], user_text: str
    ) -> Dict[str, Any]:
        max_points = int(task.get("max_points", 15))
        instruction = task.get("instruction", "")
        prompt = task.get("prompt", "")
        min_words = int(task.get("min_words", 0))
        max_words = int(task.get("max_words", 9999))
        model_answer = task.get("model_answer", "")

        word_count = len([w for w in re.findall(r"\w+", user_text)])

        rubric_prompt = (
            "Du bist ein Prüfer des Goethe-Instituts. Bewerte den folgenden "
            "Schülertext nach den vier offiziellen Goethe-Kriterien.\n\n"
            f"AUFGABE: {instruction}\n"
            f"PROMPT: {prompt}\n"
            f"WORTGRENZE: {min_words}-{max_words} Wörter (Schüler: {word_count})\n"
            f"MUSTERLÖSUNG (zur Orientierung): {model_answer}\n\n"
            f"SCHÜLERTEXT:\n{user_text}\n\n"
            "Bewerte JEDES Kriterium von 0 bis 15 Punkten:\n"
            "1. Aufgabenbewältigung (alle Inhaltspunkte abgedeckt?)\n"
            "2. Kohärenz (logischer Aufbau, Konnektoren)\n"
            "3. Wortschatz (Vielfalt und Angemessenheit)\n"
            "4. Grammatik (Korrektheit, Strukturen)\n\n"
            "Antworte NUR mit JSON in genau diesem Format:\n"
            "{\n"
            '  "aufgabenbewältigung": <0-15>,\n'
            '  "kohaerenz": <0-15>,\n'
            '  "wortschatz": <0-15>,\n'
            '  "grammatik": <0-15>,\n'
            '  "feedback": "<Feedback auf Deutsch, 2-3 Sätze>",\n'
            '  "strengths": ["<Stärke 1>", "<Stärke 2>"],\n'
            '  "improvements": ["<Verbesserung 1>", "<Verbesserung 2>"]\n'
            "}"
        )

        try:
            completion = await self._client.chat.completions.create(
                model=self._settings.groq_llm_model,
                messages=[{"role": "user", "content": rubric_prompt}],
                temperature=0.2,
                max_tokens=700,
                response_format={"type": "json_object"},
            )
            raw = completion.choices[0].message.content or "{}"
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip())
            data = json.loads(cleaned)
        except Exception as exc:
            logger.error("schreiben_grade_failed", error=str(exc))
            data = {}

        rubric_keys = ("aufgabenbewältigung", "kohaerenz", "wortschatz", "grammatik")
        rubric_scores = {k: float(data.get(k, 0)) for k in rubric_keys}
        # Average of the four 0-15 scores, then scale to max_points.
        avg_15 = sum(rubric_scores.values()) / 4.0
        scaled = (avg_15 / 15.0) * max_points

        # Word-count penalty if substantially under minimum
        if word_count < min_words * 0.6 and min_words > 0:
            scaled *= 0.5

        return {
            "score": round(scaled, 1),
            "feedback": data.get("feedback", "Bewertung nicht verfügbar."),
            "strengths": data.get("strengths") or [],
            "improvements": data.get("improvements") or [],
            "rubric": rubric_scores,
        }

    # ---------------------------------------------------------------
    # speaking grading (STT + pronunciation + content)
    # ---------------------------------------------------------------
    async def grade_sprechen(
        self,
        audio_bytes: bytes,
        card: SpeakingCard,
        level: str,
        audio_format: str = "webm",
    ) -> Dict[str, Any]:
        stt_service = get_stt_service()
        pronunciation_service = get_pronunciation_service()

        transcription = await stt_service.transcribe(
            audio_bytes, audio_format=audio_format, language="de"
        )
        transcript = transcription.transcript or ""

        # If we have nothing to assess, return zero.
        if not transcript.strip():
            return {
                "score": 0.0,
                "pronunciation_score": 0.0,
                "content_score": 0.0,
                "transcript": "",
                "feedback": "Es wurde keine Sprache erkannt. Bitte versuche es erneut.",
                "duration_seconds": transcription.duration_seconds,
            }

        pronunciation = await pronunciation_service.score_pronunciation(
            audio_bytes, transcript, audio_format=audio_format
        )
        pron_score = float(pronunciation.overall_score or 0.0)

        content = await self._grade_speaking_content(card, transcript, level)
        content_score = float(content.get("score", 0))

        final = pron_score * 0.4 + content_score * 0.6
        feedback_parts = []
        if content.get("feedback"):
            feedback_parts.append(content["feedback"])
        if pronunciation.ai_feedback:
            feedback_parts.append(pronunciation.ai_feedback)

        return {
            "score": round(final, 1),
            "pronunciation_score": round(pron_score, 1),
            "content_score": round(content_score, 1),
            "transcript": transcript,
            "feedback": "\n\n".join(feedback_parts) or "Bewertung abgeschlossen.",
            "strengths": content.get("strengths", []),
            "improvements": content.get("improvements", []),
            "duration_seconds": transcription.duration_seconds,
        }

    async def _grade_speaking_content(
        self, card: SpeakingCard, transcript: str, level: str
    ) -> Dict[str, Any]:
        prompt = (
            "Du bist Prüfer beim Goethe-Institut. Bewerte die mündliche Antwort "
            "eines Lernenden auf eine Sprechen-Aufgabe.\n\n"
            f"NIVEAU: {level}\n"
            f"AUFGABE ({card.task_type}): {card.prompt}\n"
            f"LEITFRAGEN: {', '.join(card.supporting_questions) if card.supporting_questions else '—'}\n\n"
            f"TRANSKRIPT:\n{transcript}\n\n"
            "Bewerte den INHALT (nicht die Aussprache) auf einer Skala 0-100 "
            "nach Relevanz, Kohärenz und Wortschatzreichtum.\n"
            "Antworte NUR mit JSON:\n"
            "{\n"
            '  "score": <0-100>,\n'
            '  "feedback": "<Feedback auf Deutsch, 2-3 Sätze>",\n'
            '  "strengths": ["<Stärke 1>", "<Stärke 2>"],\n'
            '  "improvements": ["<Verbesserung 1>"]\n'
            "}"
        )
        try:
            completion = await self._client.chat.completions.create(
                model=self._settings.groq_llm_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=500,
                response_format={"type": "json_object"},
            )
            raw = completion.choices[0].message.content or "{}"
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip())
            return json.loads(cleaned)
        except Exception as exc:
            logger.error("sprechen_content_grade_failed", error=str(exc))
            return {
                "score": 0.0,
                "feedback": "Inhaltsbewertung nicht verfügbar.",
                "strengths": [],
                "improvements": [],
            }

    # ---------------------------------------------------------------
    # readiness
    # ---------------------------------------------------------------
    async def get_exam_readiness(self, db: AsyncSession) -> ExamReadiness:
        sections = ["Lesen", "Hören", "Schreiben", "Sprechen"]
        by_section: Dict[str, float] = {}
        for section in sections:
            stmt = (
                select(ExamAttempt)
                .where(ExamAttempt.section == section)
                .order_by(desc(ExamAttempt.created_at))
                .limit(3)
            )
            rows = (await db.execute(stmt)).scalars().all()
            if not rows:
                by_section[section] = 0.0
                continue
            avg = sum(
                (r.score / r.max_score * 100.0) if r.max_score else 0.0 for r in rows
            ) / len(rows)
            by_section[section] = round(avg, 1)

        overall = (
            by_section["Lesen"] * 0.30
            + by_section["Hören"] * 0.30
            + by_section["Schreiben"] * 0.20
            + by_section["Sprechen"] * 0.20
        )
        overall = round(overall, 1)

        weakest = min(by_section.items(), key=lambda kv: kv[1])
        weakest_name = weakest[0]
        recommendations = {
            "Lesen": "Fokussiere dich auf Lesetexte: Zeitungsartikel und Anzeigen.",
            "Hören": "Höre täglich deutsches Radio und mache Hörverstehen-Übungen.",
            "Schreiben": "Übe formelle E-Mails und kurze Aufsätze mit klaren Konnektoren.",
            "Sprechen": "Sprich täglich laut und mache Aussprachetraining.",
        }
        recommendation = (
            f"Schwächster Bereich: {weakest_name}. " + recommendations[weakest_name]
        )

        predicted_weeks = max(0, round((100.0 - overall) / 8.0))

        return ExamReadiness(
            overall=overall,
            by_section=by_section,
            recommendation=recommendation,
            predicted_weeks=predicted_weeks,
        )

    # ---------------------------------------------------------------
    # listening audio generation
    # ---------------------------------------------------------------
    async def generate_listening_audio(self, script: str, level: str) -> str:
        rate = _section_rate_for_level(level)
        tts = get_tts_service()
        request = TTSRequest(
            text=script,
            voice=self._settings.edge_tts_voice,
            rate=rate,
        )
        response = await tts.synthesize(request)
        return response.audio_url


_exam_service: Optional[ExamService] = None


def get_exam_service() -> ExamService:
    global _exam_service
    if _exam_service is None:
        _exam_service = ExamService()
    return _exam_service
