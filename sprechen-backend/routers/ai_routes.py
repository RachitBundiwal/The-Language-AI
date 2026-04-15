"""HTTP routes for the Sprechen AI backend."""
from __future__ import annotations

import asyncio
import json
from typing import Optional

import structlog
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from models.schemas import (
    CEFRLevel,
    ConversationRequest,
    ConversationResponse,
    PronunciationResponse,
    TranscriptionResponse,
    TTSRequest,
    TTSResponse,
    VoiceExerciseResult,
)
from services.conversation_service import SCENARIOS, get_conversation_service
from services.pronunciation_service import get_pronunciation_service
from services.stt_service import get_stt_service
from services.tts_service import GERMAN_VOICES, get_tts_service

logger = structlog.get_logger(__name__)

voice_router = APIRouter(prefix="/api/v1/voice", tags=["voice"])
conversation_router = APIRouter(
    prefix="/api/v1/conversation", tags=["conversation"]
)


# ---------- voice ----------
@voice_router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe(
    file: UploadFile = File(...),
    language: str = Form("de"),
) -> TranscriptionResponse:
    audio_bytes = await file.read()
    audio_format = (file.filename or "audio.webm").rsplit(".", 1)[-1].lower()
    return await get_stt_service().transcribe(
        audio_bytes, audio_format=audio_format, language=language
    )


@voice_router.post("/score-pronunciation", response_model=PronunciationResponse)
async def score_pronunciation(
    file: UploadFile = File(...),
    reference_text: str = Form(...),
) -> PronunciationResponse:
    audio_bytes = await file.read()
    audio_format = (file.filename or "audio.webm").rsplit(".", 1)[-1].lower()
    return await get_pronunciation_service().score_pronunciation(
        audio_bytes, reference_text, audio_format=audio_format
    )


@voice_router.post("/full-exercise", response_model=VoiceExerciseResult)
async def full_exercise(
    file: UploadFile = File(...),
    reference_text: str = Form(...),
    level: CEFRLevel = Form(CEFRLevel.B1),
    scenario: Optional[str] = Form(None),
) -> VoiceExerciseResult:
    audio_bytes = await file.read()
    audio_format = (file.filename or "audio.webm").rsplit(".", 1)[-1].lower()

    transcription = await get_stt_service().transcribe(
        audio_bytes, audio_format=audio_format, language="de"
    )

    user_text = transcription.transcript or reference_text

    pron_task = get_pronunciation_service().score_pronunciation(
        audio_bytes, reference_text, audio_format=audio_format
    )
    chat_task = get_conversation_service().chat(
        ConversationRequest(
            message=user_text,
            history=[],
            level=level,
            scenario=scenario,
        )
    )
    pronunciation, conversation = await asyncio.gather(pron_task, chat_task)

    if conversation and conversation.reply:
        try:
            tts_resp = await get_tts_service().synthesize(
                TTSRequest(text=conversation.reply)
            )
            conversation.audio_url = tts_resp.audio_url
        except Exception as exc:
            logger.error("full_exercise_tts_failed", error=str(exc))

    return VoiceExerciseResult(
        transcription=transcription,
        pronunciation=pronunciation,
        conversation=conversation,
    )


@voice_router.post("/tts", response_model=TTSResponse)
async def tts(request: TTSRequest) -> TTSResponse:
    return await get_tts_service().synthesize(request)


@voice_router.get("/voices")
async def voices() -> dict:
    return GERMAN_VOICES


# ---------- conversation ----------
@conversation_router.post("/chat", response_model=ConversationResponse)
async def chat(request: ConversationRequest) -> ConversationResponse:
    return await get_conversation_service().chat(request)


@conversation_router.post("/chat/stream")
async def chat_stream(request: ConversationRequest):
    async def event_gen():
        async for token in get_conversation_service().stream_chat(request):
            yield f"data: {json.dumps({'token': token})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_gen(), media_type="text/event-stream")


@conversation_router.post("/evaluate-writing")
async def evaluate_writing(
    text: str = Form(...),
    task: str = Form(...),
    level: CEFRLevel = Form(CEFRLevel.B1),
) -> dict:
    return await get_conversation_service().evaluate_writing(text, task, level)


@conversation_router.post("/generate-dialogue")
async def generate_dialogue(
    scenario: str = Form(...),
    level: CEFRLevel = Form(CEFRLevel.B1),
    topic: str = Form(...),
    num_exchanges: int = Form(6),
) -> dict:
    if scenario not in SCENARIOS:
        raise HTTPException(
            status_code=400, detail=f"Unknown scenario '{scenario}'."
        )
    dialogue = await get_conversation_service().generate_lesson_dialogue(
        scenario, level, topic, num_exchanges
    )
    return {"dialogue": dialogue}
