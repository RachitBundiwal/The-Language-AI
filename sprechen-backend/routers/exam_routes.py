"""HTTP routes for the Goethe Institut exam simulator."""
from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import get_db
from models.exam_schemas import (
    ExamPaper,
    ExamReadiness,
    ExamResult,
    MCSubmission,
    SpeakingCard,
    WritingSubmission,
)
from models.orm_models import ExamAttempt
from services.exam_service import PASS_THRESHOLD, get_exam_service, get_grade

router = APIRouter(prefix="/api/v1/exams", tags=["exams"])


# ---------- helpers ----------
def _split_strengths_improvements(per_task: List[dict]) -> tuple[List[str], List[str]]:
    strengths: List[str] = []
    improvements: List[str] = []
    for r in per_task:
        strengths.extend(r.get("strengths", []) or [])
        improvements.extend(r.get("improvements", []) or [])
    return strengths[:5], improvements[:5]


async def _record_attempt(
    db: AsyncSession,
    *,
    level: str,
    section: str,
    score: float,
    max_score: float,
    duration_seconds: int,
    answers_json: dict,
    passed: bool,
) -> None:
    attempt = ExamAttempt(
        exam_level=level,
        section=section,
        score=score,
        max_score=max_score,
        duration_seconds=duration_seconds,
        answers_json=answers_json,
        passed=passed,
    )
    db.add(attempt)
    await db.commit()


# ---------- paper retrieval ----------
@router.get("/paper/{level}/{section}", response_model=ExamPaper)
async def get_paper(level: str, section: str) -> ExamPaper:
    return get_exam_service().get_exam_paper(level, section)


@router.get("/paper/{level}/Hören/audio/{part}/{script_index}")
async def get_listening_audio(level: str, part: int, script_index: int) -> dict:
    service = get_exam_service()
    paper = service.get_exam_paper(level, "Hören")
    target_part = next(
        (p for p in paper.parts if int(p.get("part_number", -1)) == part), None
    )
    if target_part is None:
        raise HTTPException(status_code=404, detail="Listening part not found")
    scripts = target_part.get("scripts", []) or []
    if script_index < 0 or script_index >= len(scripts):
        raise HTTPException(status_code=404, detail="Script index out of range")
    script_text = scripts[script_index].get("script", "")
    audio_url = await service.generate_listening_audio(script_text, level)
    return {"audio_url": audio_url, "script": script_text}


# ---------- submissions ----------
@router.post("/submit/lesen", response_model=ExamResult)
async def submit_lesen(
    submission: MCSubmission, db: AsyncSession = Depends(get_db)
) -> ExamResult:
    service = get_exam_service()
    paper = service.get_exam_paper(submission.level, "Lesen")
    answers = [a.model_dump() for a in submission.answers]
    graded = await service.grade_lesen(paper, answers)
    result = ExamResult(
        level=submission.level,
        section="Lesen",
        score=graded["score"],
        max_score=graded["max_score"],
        percentage=graded["percentage"],
        passed=graded["passed"],
        grade=get_grade(graded["percentage"]),
        detailed_results=graded["detailed"],
        feedback=_lesen_hoeren_feedback(graded["percentage"], "Lesen"),
        strengths=[],
        improvements=[],
    )
    await _record_attempt(
        db,
        level=submission.level,
        section="Lesen",
        score=graded["score"],
        max_score=graded["max_score"],
        duration_seconds=submission.duration_seconds,
        answers_json={"answers": answers},
        passed=graded["passed"],
    )
    return result


@router.post("/submit/hören", response_model=ExamResult)
async def submit_hoeren(
    submission: MCSubmission, db: AsyncSession = Depends(get_db)
) -> ExamResult:
    service = get_exam_service()
    paper = service.get_exam_paper(submission.level, "Hören")
    answers = [a.model_dump() for a in submission.answers]
    graded = await service.grade_hören(paper, answers)
    result = ExamResult(
        level=submission.level,
        section="Hören",
        score=graded["score"],
        max_score=graded["max_score"],
        percentage=graded["percentage"],
        passed=graded["passed"],
        grade=get_grade(graded["percentage"]),
        detailed_results=graded["detailed"],
        feedback=_lesen_hoeren_feedback(graded["percentage"], "Hören"),
    )
    await _record_attempt(
        db,
        level=submission.level,
        section="Hören",
        score=graded["score"],
        max_score=graded["max_score"],
        duration_seconds=submission.duration_seconds,
        answers_json={"answers": answers},
        passed=graded["passed"],
    )
    return result


@router.post("/submit/schreiben", response_model=ExamResult)
async def submit_schreiben(
    submission: WritingSubmission, db: AsyncSession = Depends(get_db)
) -> ExamResult:
    service = get_exam_service()
    paper = service.get_exam_paper(submission.level, "Schreiben")
    payload = [a.model_dump() for a in submission.answers]
    graded = await service.grade_schreiben(paper, payload)
    strengths, improvements = _split_strengths_improvements(graded["per_task"])
    result = ExamResult(
        level=submission.level,
        section="Schreiben",
        score=graded["score"],
        max_score=graded["max_score"],
        percentage=graded["percentage"],
        passed=graded["passed"],
        grade=get_grade(graded["percentage"]),
        detailed_results=graded["per_task"],
        feedback=_schreiben_feedback(graded["percentage"]),
        strengths=strengths,
        improvements=improvements,
    )
    await _record_attempt(
        db,
        level=submission.level,
        section="Schreiben",
        score=graded["score"],
        max_score=graded["max_score"],
        duration_seconds=submission.duration_seconds,
        answers_json={"answers": payload, "per_task": graded["per_task"]},
        passed=graded["passed"],
    )
    return result


@router.post("/submit/sprechen", response_model=ExamResult)
async def submit_sprechen(
    audio_file: UploadFile = File(...),
    level: str = Form(...),
    card_number: int = Form(...),
    duration_seconds: int = Form(0),
    db: AsyncSession = Depends(get_db),
) -> ExamResult:
    service = get_exam_service()
    paper = service.get_exam_paper(level, "Sprechen")
    card_dict = next(
        (c for c in paper.parts if int(c.get("card_number", -1)) == card_number),
        None,
    )
    if card_dict is None:
        raise HTTPException(status_code=404, detail=f"Card {card_number} not found")
    card = SpeakingCard(**card_dict)

    audio_bytes = await audio_file.read()
    audio_format = (audio_file.filename or "audio.webm").split(".")[-1].lower()

    graded = await service.grade_sprechen(
        audio_bytes, card, level, audio_format=audio_format
    )

    score = float(graded["score"])
    # One card is worth (max_score / number_of_cards). For partial single-card
    # results we report the card-percentage directly so the UI can show progress.
    cards_total = max(1, len(paper.parts))
    per_card_max = paper.max_score / cards_total
    card_score = (score / 100.0) * per_card_max
    percentage = score  # 0-100 for this card

    result = ExamResult(
        level=level,
        section="Sprechen",
        score=round(card_score, 1),
        max_score=per_card_max,
        percentage=round(percentage, 1),
        passed=percentage >= PASS_THRESHOLD,
        grade=get_grade(percentage),
        detailed_results=[
            {
                "card_number": card_number,
                "transcript": graded.get("transcript", ""),
                "pronunciation_score": graded.get("pronunciation_score", 0.0),
                "content_score": graded.get("content_score", 0.0),
            }
        ],
        feedback=graded.get("feedback", ""),
        strengths=graded.get("strengths", []),
        improvements=graded.get("improvements", []),
    )

    await _record_attempt(
        db,
        level=level,
        section="Sprechen",
        score=round(card_score, 1),
        max_score=per_card_max,
        duration_seconds=duration_seconds,
        answers_json={
            "card_number": card_number,
            "transcript": graded.get("transcript", ""),
            "pronunciation_score": graded.get("pronunciation_score", 0.0),
            "content_score": graded.get("content_score", 0.0),
        },
        passed=result.passed,
    )
    return result


# ---------- history & readiness ----------
@router.get("/history")
async def history(db: AsyncSession = Depends(get_db)) -> List[dict]:
    stmt = (
        select(ExamAttempt)
        .order_by(desc(ExamAttempt.created_at))
        .limit(20)
    )
    rows = (await db.execute(stmt)).scalars().all()
    return [
        {
            "id": r.id,
            "level": r.exam_level,
            "section": r.section,
            "score": r.score,
            "max_score": r.max_score,
            "percentage": round((r.score / r.max_score * 100.0), 1)
            if r.max_score
            else 0.0,
            "duration_seconds": r.duration_seconds,
            "passed": r.passed,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]


@router.get("/readiness", response_model=ExamReadiness)
async def readiness(db: AsyncSession = Depends(get_db)) -> ExamReadiness:
    return await get_exam_service().get_exam_readiness(db)


# ---------- feedback helpers ----------
def _lesen_hoeren_feedback(percentage: float, section: str) -> str:
    if percentage >= 87:
        return f"Hervorragend! Dein {section}-Verständnis ist auf Prüfungsniveau."
    if percentage >= 73:
        return f"Sehr gut. Dein {section}-Verständnis ist solide."
    if percentage >= 60:
        return f"Bestanden. Übe weiter, um sicherer zu werden."
    return (
        f"Noch nicht bestanden. Konzentriere dich auf typische {section}-Aufgaben "
        "und übe regelmäßig."
    )


def _schreiben_feedback(percentage: float) -> str:
    if percentage >= 87:
        return "Sehr gut strukturierte Texte mit reichem Wortschatz."
    if percentage >= 73:
        return "Gute Texte. Achte weiter auf Konnektoren und Grammatik."
    if percentage >= 60:
        return "Bestanden. Arbeite an Wortschatzvielfalt und Satzbau."
    return "Übe regelmäßig kurze Texte und beachte alle Inhaltspunkte der Aufgabe."
