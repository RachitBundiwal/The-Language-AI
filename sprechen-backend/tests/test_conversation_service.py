"""Tests for services.conversation_service."""
from __future__ import annotations

import json
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from models.schemas import (
    CEFRLevel,
    ConversationMessage,
    ConversationRequest,
)
from services.conversation_service import (
    SCENARIOS,
    ConversationService,
    get_conversation_service,
)


# ---------- helpers ----------
def _completion(content: str):
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=content))]
    )


def _stream_chunks(tokens):
    async def agen():
        for t in tokens:
            yield SimpleNamespace(
                choices=[SimpleNamespace(delta=SimpleNamespace(content=t))]
            )

    return agen()


# ---------- scenarios ----------
def test_scenarios_have_required_keys() -> None:
    required = {
        "bakery",
        "doctor",
        "job_interview",
        "supermarket",
        "train_station",
        "restaurant",
        "landlord",
        "free",
    }
    assert required.issubset(SCENARIOS.keys())


def test_free_scenario_has_level_placeholder() -> None:
    assert "{level}" in SCENARIOS["free"]


# ---------- system prompt + history ----------
def test_system_prompt_includes_level_and_formality() -> None:
    svc = ConversationService()
    req = ConversationRequest(
        message="Hi", level=CEFRLevel.A2, scenario="bakery", formality="Sie"
    )
    prompt = svc._system_prompt(req)
    assert "A2" in prompt
    assert "Sie" in prompt
    assert "Bäcker" in prompt


def test_system_prompt_defaults_to_free_scenario() -> None:
    svc = ConversationService()
    req = ConversationRequest(message="Hi")
    prompt = svc._system_prompt(req)
    assert "B1" in prompt
    assert "Freies Gespräch" in prompt


def test_build_messages_truncates_history_to_last_10() -> None:
    svc = ConversationService()
    history = [
        ConversationMessage(role="user" if i % 2 == 0 else "assistant", content=f"m{i}")
        for i in range(20)
    ]
    req = ConversationRequest(message="now", history=history)
    msgs = svc._build_messages(req)
    # 1 system + 10 history + 1 current
    assert len(msgs) == 12
    assert msgs[0]["role"] == "system"
    assert msgs[-1] == {"role": "user", "content": "now"}
    assert msgs[1]["content"] == "m10"  # first kept history item


# ---------- _parse ----------
def test_parse_valid_json() -> None:
    svc = ConversationService()
    raw = json.dumps(
        {
            "reply": "Hallo!",
            "translation": "Hello!",
            "corrections": [{"original": "a", "corrected": "b", "explanation": "c"}],
            "new_vocabulary": [{"word": "Hund", "translation": "dog", "example": "x"}],
        }
    )
    out = svc._parse(raw)
    assert out.reply == "Hallo!"
    assert out.translation == "Hello!"
    assert len(out.corrections) == 1
    assert out.new_vocabulary[0]["word"] == "Hund"


def test_parse_strips_json_fences() -> None:
    svc = ConversationService()
    raw = '```json\n{"reply": "Hi"}\n```'
    out = svc._parse(raw)
    assert out.reply == "Hi"


def test_parse_invalid_json_falls_back_to_raw() -> None:
    svc = ConversationService()
    out = svc._parse("not really json at all")
    assert out.reply == "not really json at all"
    assert out.translation is None
    assert out.corrections == []


# ---------- chat ----------
@pytest.mark.asyncio
async def test_chat_returns_parsed_response() -> None:
    svc = ConversationService()
    raw = json.dumps(
        {
            "reply": "Guten Tag!",
            "translation": "Good day!",
            "corrections": [],
            "new_vocabulary": [],
        }
    )
    svc._client.chat = SimpleNamespace(
        completions=SimpleNamespace(
            create=AsyncMock(return_value=_completion(raw))
        )
    )
    out = await svc.chat(ConversationRequest(message="Hallo"))
    assert out.reply == "Guten Tag!"
    assert out.translation == "Good day!"


@pytest.mark.asyncio
async def test_chat_handles_groq_failure() -> None:
    svc = ConversationService()
    svc._client.chat = SimpleNamespace(
        completions=SimpleNamespace(
            create=AsyncMock(side_effect=RuntimeError("rate limit"))
        )
    )
    out = await svc.chat(ConversationRequest(message="Hallo"))
    assert "Entschuldigung" in out.reply


# ---------- streaming ----------
@pytest.mark.asyncio
async def test_stream_chat_yields_tokens() -> None:
    svc = ConversationService()
    svc._client.chat = SimpleNamespace(
        completions=SimpleNamespace(
            create=AsyncMock(return_value=_stream_chunks(["Hal", "lo", "!"]))
        )
    )
    tokens = []
    async for t in svc.stream_chat(ConversationRequest(message="x")):
        tokens.append(t)
    assert tokens == ["Hal", "lo", "!"]


@pytest.mark.asyncio
async def test_stream_chat_yields_error_marker_on_failure() -> None:
    svc = ConversationService()
    svc._client.chat = SimpleNamespace(
        completions=SimpleNamespace(
            create=AsyncMock(side_effect=RuntimeError("boom"))
        )
    )
    tokens = [t async for t in svc.stream_chat(ConversationRequest(message="x"))]
    assert tokens == ["[stream error]"]


# ---------- evaluate_writing ----------
@pytest.mark.asyncio
async def test_evaluate_writing_parses_grader_json() -> None:
    svc = ConversationService()
    raw = json.dumps(
        {
            "score": 12,
            "grade": "gut",
            "feedback": "Solider Text.",
            "strengths": ["Wortschatz"],
            "improvements": ["Kommas"],
        }
    )
    svc._client.chat = SimpleNamespace(
        completions=SimpleNamespace(
            create=AsyncMock(return_value=_completion(raw))
        )
    )
    out = await svc.evaluate_writing(
        "Mein Text ist gut.", "Schreib einen Text", CEFRLevel.B1
    )
    assert out["score"] == 12
    assert out["grade"] == "gut"
    assert "Wortschatz" in out["strengths"]


@pytest.mark.asyncio
async def test_evaluate_writing_handles_failure() -> None:
    svc = ConversationService()
    svc._client.chat = SimpleNamespace(
        completions=SimpleNamespace(
            create=AsyncMock(side_effect=RuntimeError("nope"))
        )
    )
    out = await svc.evaluate_writing("x", "task", CEFRLevel.B1)
    assert out["score"] == 0
    assert out["grade"] == "n/a"


# ---------- generate_lesson_dialogue ----------
@pytest.mark.asyncio
async def test_generate_lesson_dialogue_returns_list() -> None:
    svc = ConversationService()
    raw = json.dumps(
        {
            "dialogue": [
                {"speaker": "A", "german": "Hallo!", "english": "Hello!"},
                {"speaker": "B", "german": "Hi!", "english": "Hi!"},
            ]
        }
    )
    svc._client.chat = SimpleNamespace(
        completions=SimpleNamespace(
            create=AsyncMock(return_value=_completion(raw))
        )
    )
    out = await svc.generate_lesson_dialogue("bakery", CEFRLevel.A2, "Brot kaufen", 2)
    assert isinstance(out, list)
    assert len(out) == 2
    assert out[0]["german"] == "Hallo!"


@pytest.mark.asyncio
async def test_generate_lesson_dialogue_handles_failure() -> None:
    svc = ConversationService()
    svc._client.chat = SimpleNamespace(
        completions=SimpleNamespace(
            create=AsyncMock(side_effect=RuntimeError("nope"))
        )
    )
    out = await svc.generate_lesson_dialogue("bakery", CEFRLevel.A2, "topic", 2)
    assert out == []


# ---------- singleton ----------
def test_singleton_conversation_service() -> None:
    a = get_conversation_service()
    b = get_conversation_service()
    assert a is b
