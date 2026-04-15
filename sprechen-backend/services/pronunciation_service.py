"""Pronunciation assessment via Whisper transcription + Groq LLM analysis."""
from __future__ import annotations

import json
import re
from difflib import SequenceMatcher
from typing import List, Optional, Tuple

import structlog
from groq import AsyncGroq

from core.config import get_settings
from models.schemas import PhonemeScore, PronunciationResponse
from services.stt_service import get_stt_service

logger = structlog.get_logger(__name__)

PHONEME_TIPS = {
    "ç": "Soft 'ich-Laut' — tongue near roof, NOT 'sh'",
    "x": "Hard 'ach-Laut' — gargle at back of throat",
    "ü": "Round lips like 'oo' but say 'ee'",
    "ö": "Round lips like 'o' but say 'e'",
    "r": "German R — uvular, gargled at back",
    "z": "German Z — sharp 'ts' like in 'cats'",
    "pf": "Both consonants — like 'up-front'",
}

_ANALYSIS_PROMPT = """\
You are a German pronunciation coach. Given a reference sentence and the learner's \
actual transcription with per-word confidence scores, analyse pronunciation quality.

Reference: {reference}
Transcription: {transcript}
Word confidences: {word_data}

Respond in JSON only:
{{
  "problem_sounds": ["list of German sounds the learner likely struggles with, e.g. ü, ö, ch, r, z"],
  "feedback_de": "2-3 sentences of coaching advice in German",
  "fluency_rating": <0-100 integer>,
  "accuracy_rating": <0-100 integer>
}}
"""


class PronunciationService:
    def __init__(self) -> None:
        self._settings = get_settings()
        self._llm = AsyncGroq(api_key=self._settings.groq_api_key or "missing-key")

    async def score_pronunciation(
        self,
        user_audio_bytes: bytes,
        reference_text: str,
        audio_format: str = "webm",
    ) -> PronunciationResponse:
        try:
            stt = get_stt_service()
            transcription = await stt.transcribe(user_audio_bytes, audio_format)

            if not transcription.transcript:
                return self._fallback_response(reference_text)

            # Word-error-rate based scores
            ref_words = self._normalize(reference_text).split()
            hyp_words = self._normalize(transcription.transcript).split()
            similarity = SequenceMatcher(None, ref_words, hyp_words).ratio()

            accuracy = round(similarity * 100, 1)
            completeness = round(min(len(hyp_words) / max(len(ref_words), 1), 1.0) * 100, 1)

            # Average word confidence from Whisper
            confidences = [w.get("probability", 0.9) for w in transcription.word_timestamps]
            avg_confidence = sum(confidences) / max(len(confidences), 1)
            fluency = round(avg_confidence * 100, 1)

            # Ask LLM for qualitative analysis
            word_data = [
                {"word": w.get("word", ""), "confidence": round(w.get("probability", 0.9), 2)}
                for w in transcription.word_timestamps
            ]
            llm_analysis = await self._llm_analyze(reference_text, transcription.transcript, word_data)

            if llm_analysis:
                fluency = llm_analysis.get("fluency_rating", fluency)
                accuracy = llm_analysis.get("accuracy_rating", accuracy)

            problem_phonemes = llm_analysis.get("problem_sounds", []) if llm_analysis else []
            ai_feedback = llm_analysis.get("feedback_de", "") if llm_analysis else ""

            if not ai_feedback:
                ai_feedback = self._basic_feedback(accuracy)

            pron_score = round((accuracy * 0.5 + fluency * 0.3 + completeness * 0.2), 1)

            phoneme_scores = [
                PhonemeScore(
                    phoneme=ph,
                    score=0.4,
                    feedback=PHONEME_TIPS.get(ph, f"Achte auf den Laut /{ph}/."),
                )
                for ph in problem_phonemes[:5]
            ]

            return PronunciationResponse(
                overall_score=pron_score,
                pronunciation_score=accuracy,
                fluency_score=fluency,
                accuracy_score=accuracy,
                completeness_score=completeness,
                prosody_score=None,
                phoneme_scores=phoneme_scores,
                problem_phonemes=problem_phonemes,
                ai_feedback=ai_feedback,
            )
        except Exception as exc:
            logger.error("pronunciation_failed", error=str(exc))
            return self._fallback_response(reference_text)

    async def _llm_analyze(
        self, reference: str, transcript: str, word_data: list
    ) -> Optional[dict]:
        try:
            prompt = _ANALYSIS_PROMPT.format(
                reference=reference,
                transcript=transcript,
                word_data=json.dumps(word_data, ensure_ascii=False),
            )
            resp = await self._llm.chat.completions.create(
                model=self._settings.groq_llm_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=300,
            )
            text = resp.choices[0].message.content or ""
            # Extract JSON from response
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                return json.loads(match.group())
        except Exception as exc:
            logger.warning("llm_pronunciation_analysis_failed", error=str(exc))
        return None

    @staticmethod
    def _normalize(text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"[^\w\säöüß]", "", text)
        return re.sub(r"\s+", " ", text)

    @staticmethod
    def _basic_feedback(accuracy: float) -> str:
        if accuracy >= 90:
            return "Ausgezeichnet! Deine Aussprache klingt sehr natürlich."
        if accuracy >= 75:
            return "Sehr gut. Deine Aussprache ist klar verständlich."
        if accuracy >= 50:
            return "Gut gemacht. Übe weiter, um noch flüssiger zu werden."
        return "Weiter üben! Versuche langsamer und deutlicher zu sprechen."

    @staticmethod
    def _fallback_response(reference_text: str) -> PronunciationResponse:
        return PronunciationResponse(
            overall_score=0.0,
            pronunciation_score=0.0,
            fluency_score=0.0,
            accuracy_score=0.0,
            completeness_score=0.0,
            prosody_score=None,
            phoneme_scores=[],
            problem_phonemes=[],
            ai_feedback="Konnte die Aufnahme nicht analysieren. Bitte versuche es erneut.",
        )


_pron_service: Optional[PronunciationService] = None


def get_pronunciation_service() -> PronunciationService:
    global _pron_service
    if _pron_service is None:
        _pron_service = PronunciationService()
    return _pron_service
