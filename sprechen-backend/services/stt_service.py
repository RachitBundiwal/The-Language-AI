"""Speech-to-text service powered by Groq Whisper."""
from __future__ import annotations

import os
import tempfile
from typing import Optional

import structlog
from groq import AsyncGroq

from core.config import get_settings
from models.schemas import TranscriptionResponse

logger = structlog.get_logger(__name__)


class STTService:
    def __init__(self) -> None:
        settings = get_settings()
        self._settings = settings
        self._client = AsyncGroq(api_key=settings.groq_api_key or "missing-key")

    async def transcribe(
        self,
        audio_bytes: bytes,
        audio_format: str = "webm",
        language: str = "de",
    ) -> TranscriptionResponse:
        """Transcribe an audio blob using Groq Whisper-Large-v3."""
        tmp_path: Optional[str] = None
        try:
            with tempfile.NamedTemporaryFile(
                suffix=f".{audio_format}", delete=False
            ) as tmp:
                tmp.write(audio_bytes)
                tmp_path = tmp.name

            with open(tmp_path, "rb") as f:
                response = await self._client.audio.transcriptions.create(
                    file=(f"audio.{audio_format}", f.read()),
                    model=self._settings.groq_whisper_model,
                    response_format="verbose_json",
                    timestamp_granularities=["word"],
                    language=language,
                )

            transcript = getattr(response, "text", "") or ""
            duration = float(getattr(response, "duration", 0.0) or 0.0)
            raw_words = getattr(response, "words", None) or []

            word_timestamps = []
            for w in raw_words:
                if isinstance(w, dict):
                    word_timestamps.append(
                        {
                            "word": w.get("word", ""),
                            "start": float(w.get("start", 0.0)),
                            "end": float(w.get("end", 0.0)),
                            "probability": float(w.get("probability", 0.9)),
                        }
                    )
                else:
                    word_timestamps.append(
                        {
                            "word": getattr(w, "word", ""),
                            "start": float(getattr(w, "start", 0.0)),
                            "end": float(getattr(w, "end", 0.0)),
                            "probability": float(getattr(w, "probability", 0.9)),
                        }
                    )

            return TranscriptionResponse(
                transcript=transcript.strip(),
                language=language,
                confidence=0.9,
                word_timestamps=word_timestamps,
                duration_seconds=duration,
            )
        except Exception as exc:
            logger.error("stt_failed", error=str(exc))
            return TranscriptionResponse(
                transcript="",
                language=language,
                confidence=0.0,
                word_timestamps=[],
                duration_seconds=0.0,
            )
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass


_stt_service: Optional[STTService] = None


def get_stt_service() -> STTService:
    global _stt_service
    if _stt_service is None:
        _stt_service = STTService()
    return _stt_service
