"""LLM-powered conversation service using Groq."""
from __future__ import annotations

import json
import re
from typing import AsyncGenerator, List, Optional

import structlog
from groq import AsyncGroq

from core.config import get_settings
from models.schemas import (
    CEFRLevel,
    ConversationMessage,
    ConversationRequest,
    ConversationResponse,
)

logger = structlog.get_logger(__name__)


SCENARIOS = {
    "bakery": "Du bist ein Bäcker. Der Lernende ist ein Kunde.",
    "doctor": "Du bist ein Arzt. Der Lernende ist ein Patient.",
    "job_interview": "Du bist ein HR-Manager. Der Lernende bewirbt sich.",
    "supermarket": "Du bist ein Supermarktmitarbeiter.",
    "train_station": "Du bist ein Bahnhofsmitarbeiter.",
    "restaurant": "Du bist ein Kellner.",
    "landlord": "Du bist ein Vermieter.",
    "free": "Freies Gespräch passend für {level}.",
}


SYSTEM_PROMPT = """Du bist ein freundlicher deutscher Konversationspartner für einen \
Sprachlerner auf dem Niveau {level} (Goethe-Institut CEFR).

ROLLE / SZENARIO: {scenario}

REGELN:
1. Antworte IMMER auf Deutsch.
2. Passe dich dem Niveau {level} an:
   - A1/A2: kurze, einfache Sätze, Präsens, häufige Vokabeln
   - B1/B2: normale Sätze, gelegentliche Erklärungen schwieriger Wörter
   - C1/C2: natürliches, idiomatisches Deutsch mit Redewendungen
3. Verwende die Anrede "{formality}" konsequent.
4. Wenn der Lernende Fehler macht, korrigiere sie höflich am Ende der Antwort.
5. Schlage 1–2 neue, nützliche Vokabeln vor, wenn passend.
6. Bleibe in der Rolle des Szenarios.

AUSGABEFORMAT (NUR JSON, keine Erklärungen außerhalb):
{{
  "reply": "Deine deutsche Antwort als Charakter",
  "translation": "English translation of the reply",
  "corrections": [
    {{"original": "...", "corrected": "...", "explanation": "..."}}
  ],
  "new_vocabulary": [
    {{"word": "...", "translation": "...", "example": "..."}}
  ]
}}
"""


class ConversationService:
    def __init__(self) -> None:
        self._settings = get_settings()
        self._client = AsyncGroq(api_key=self._settings.groq_api_key or "missing-key")

    # ---------- system prompt ----------
    def _system_prompt(self, request: ConversationRequest) -> str:
        scenario_key = request.scenario or "free"
        scenario_text = SCENARIOS.get(scenario_key, SCENARIOS["free"])
        scenario_text = scenario_text.format(level=request.level.value)
        return SYSTEM_PROMPT.format(
            level=request.level.value,
            scenario=scenario_text,
            formality=request.formality,
        )

    def _build_messages(self, request: ConversationRequest) -> List[dict]:
        msgs: List[dict] = [{"role": "system", "content": self._system_prompt(request)}]
        for m in request.history[-10:]:
            msgs.append({"role": m.role, "content": m.content})
        msgs.append({"role": "user", "content": request.message})
        return msgs

    # ---------- chat ----------
    async def chat(self, request: ConversationRequest) -> ConversationResponse:
        try:
            completion = await self._client.chat.completions.create(
                model=self._settings.groq_llm_model,
                messages=self._build_messages(request),
                temperature=self._settings.groq_temperature,
                max_tokens=self._settings.groq_max_tokens,
                response_format={"type": "json_object"},
            )
            raw = completion.choices[0].message.content or ""
            return self._parse(raw)
        except Exception as exc:
            logger.error("chat_failed", error=str(exc))
            return ConversationResponse(
                reply="Entschuldigung, ich kann gerade nicht antworten.",
                translation="Sorry, I can't respond right now.",
                corrections=[],
                new_vocabulary=[],
            )

    def _parse(self, raw: str) -> ConversationResponse:
        text = raw.strip()
        # strip ```json fences if present
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        try:
            data = json.loads(text)
            return ConversationResponse(
                reply=data.get("reply", ""),
                translation=data.get("translation"),
                corrections=data.get("corrections", []) or [],
                new_vocabulary=data.get("new_vocabulary", []) or [],
            )
        except Exception:
            return ConversationResponse(
                reply=text,
                translation=None,
                corrections=[],
                new_vocabulary=[],
            )

    # ---------- streaming ----------
    async def stream_chat(
        self, request: ConversationRequest
    ) -> AsyncGenerator[str, None]:
        try:
            stream = await self._client.chat.completions.create(
                model=self._settings.groq_llm_model,
                messages=self._build_messages(request),
                temperature=self._settings.groq_temperature,
                max_tokens=self._settings.groq_max_tokens,
                stream=True,
            )
            async for chunk in stream:
                try:
                    delta = chunk.choices[0].delta.content
                except (IndexError, AttributeError):
                    delta = None
                if delta:
                    yield delta
        except Exception as exc:
            logger.error("stream_failed", error=str(exc))
            yield "[stream error]"

    # ---------- writing evaluation ----------
    async def evaluate_writing(self, text: str, task: str, level: CEFRLevel) -> dict:
        prompt = f"""Du bist ein Goethe-Institut Prüfer und bewertest einen \
Schreibtext auf dem Niveau {level.value}.

AUFGABE: {task}

TEXT DES LERNENDEN:
{text}

Bewerte streng nach Goethe-Rubrik (Inhalt, Sprachliche Mittel, Korrektheit, \
Aufbau). Gib JSON zurück:
{{
  "score": <0-15>,
  "grade": "<sehr gut|gut|befriedigend|ausreichend|mangelhaft>",
  "feedback": "Allgemeines Feedback auf Deutsch",
  "strengths": ["...", "..."],
  "improvements": ["...", "..."]
}}
"""
        try:
            completion = await self._client.chat.completions.create(
                model=self._settings.groq_llm_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=self._settings.groq_max_tokens,
                response_format={"type": "json_object"},
            )
            raw = completion.choices[0].message.content or "{}"
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip())
            return json.loads(cleaned)
        except Exception as exc:
            logger.error("evaluate_writing_failed", error=str(exc))
            return {
                "score": 0,
                "grade": "n/a",
                "feedback": "Bewertung derzeit nicht möglich.",
                "strengths": [],
                "improvements": [],
            }

    # ---------- dialogue generator ----------
    async def generate_lesson_dialogue(
        self,
        scenario: str,
        level: CEFRLevel,
        topic: str,
        num_exchanges: int = 6,
    ) -> List[dict]:
        scenario_text = SCENARIOS.get(scenario, SCENARIOS["free"]).format(
            level=level.value
        )
        prompt = f"""Erstelle einen realistischen deutschen Dialog für einen \
Sprachlerner auf dem Niveau {level.value}.

SZENARIO: {scenario_text}
THEMA: {topic}
ANZAHL AUSTAUSCHE: {num_exchanges}

Gib JSON zurück:
{{
  "dialogue": [
    {{"speaker": "A", "german": "...", "english": "..."}},
    {{"speaker": "B", "german": "...", "english": "..."}}
  ]
}}
"""
        try:
            completion = await self._client.chat.completions.create(
                model=self._settings.groq_llm_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=self._settings.groq_max_tokens,
                response_format={"type": "json_object"},
            )
            raw = completion.choices[0].message.content or "{}"
            cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip())
            data = json.loads(cleaned)
            return data.get("dialogue", []) or []
        except Exception as exc:
            logger.error("generate_dialogue_failed", error=str(exc))
            return []


_conversation_service: Optional[ConversationService] = None


def get_conversation_service() -> ConversationService:
    global _conversation_service
    if _conversation_service is None:
        _conversation_service = ConversationService()
    return _conversation_service
