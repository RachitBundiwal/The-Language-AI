"""Text-to-speech service powered by edge-tts (Microsoft Neural)."""
from __future__ import annotations

import hashlib
import io
import os
from typing import Optional

import asyncio

import edge_tts
import structlog
from fastapi import HTTPException
from pydub import AudioSegment

from core.config import get_settings
from models.schemas import TTSRequest, TTSResponse

try:
    from gtts import gTTS  # type: ignore
except ImportError:
    gTTS = None  # type: ignore

logger = structlog.get_logger(__name__)


GERMAN_VOICES = {
    "de-DE-KatjaNeural": "Female · Standard German",
    "de-DE-ConradNeural": "Male · Standard German",
    "de-DE-AmalaNeural": "Female · Warm",
    "de-AT-IngridNeural": "Female · Austrian",
    "de-CH-LeniNeural": "Female · Swiss",
}


class TTSService:
    def __init__(self) -> None:
        self._settings = get_settings()
        os.makedirs(self._settings.audio_cache_dir, exist_ok=True)

    def _cache_path(self, key: str) -> str:
        return os.path.join(self._settings.audio_cache_dir, f"{key}.mp3")

    @staticmethod
    def _make_key(text: str, voice: str, rate: str) -> str:
        return hashlib.md5(f"{text}|{voice}|{rate}".encode("utf-8")).hexdigest()

    async def synthesize(self, request: TTSRequest) -> TTSResponse:
        key = self._make_key(request.text, request.voice, request.rate)
        path = self._cache_path(key)

        if os.path.exists(path):
            duration = self._duration(path)
            return TTSResponse(
                audio_url=f"/audio/{key}.mp3",
                duration_seconds=duration,
                text=request.text,
            )

        audio_bytes = await self._edge_bytes(
            request.text, request.voice, request.rate, self._settings.edge_tts_pitch
        )
        if not audio_bytes:
            audio_bytes = await self._gtts_bytes(request.text)

        if not audio_bytes:
            logger.error("tts_all_providers_failed", text_len=len(request.text))
            raise HTTPException(status_code=503, detail="TTS providers unavailable")

        with open(path, "wb") as f:
            f.write(audio_bytes)

        duration = self._duration(path)
        return TTSResponse(
            audio_url=f"/audio/{key}.mp3",
            duration_seconds=duration,
            text=request.text,
        )

    async def synthesize_to_bytes(
        self, text: str, voice: Optional[str] = None
    ) -> bytes:
        voice = voice or self._settings.edge_tts_voice
        data = await self._edge_bytes(
            text, voice, self._settings.edge_tts_rate, self._settings.edge_tts_pitch
        )
        if not data:
            data = await self._gtts_bytes(text)
        if not data:
            logger.error("tts_bytes_all_providers_failed")
        return data

    async def _edge_bytes(
        self, text: str, voice: str, rate: str, pitch: str
    ) -> bytes:
        try:
            communicate = edge_tts.Communicate(
                text=text, voice=voice, rate=rate, pitch=pitch
            )
            buf = bytearray()
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    buf.extend(chunk["data"])
            return bytes(buf)
        except Exception as exc:
            logger.warning("edge_tts_failed", error=str(exc))
            return b""

    async def _gtts_bytes(self, text: str) -> bytes:
        if gTTS is None:
            return b""

        def _sync() -> bytes:
            try:
                tts = gTTS(text=text, lang="de")
                buf = io.BytesIO()
                tts.write_to_fp(buf)
                return buf.getvalue()
            except Exception as exc:
                logger.warning("gtts_failed", error=str(exc))
                return b""

        return await asyncio.to_thread(_sync)

    def list_voices(self) -> dict:
        return GERMAN_VOICES

    @staticmethod
    def _duration(path: str) -> float:
        try:
            seg = AudioSegment.from_file(path, format="mp3")
            return len(seg) / 1000.0
        except Exception:
            return 0.0


_tts_service: Optional[TTSService] = None


def get_tts_service() -> TTSService:
    global _tts_service
    if _tts_service is None:
        _tts_service = TTSService()
    return _tts_service
