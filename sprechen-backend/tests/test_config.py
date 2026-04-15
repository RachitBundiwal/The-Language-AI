"""Tests for core.config.Settings."""
from __future__ import annotations

from core.config import Settings, get_settings


def test_settings_defaults() -> None:
    s = Settings()
    assert s.app_name == "Sprechen"
    assert s.debug is True
    assert s.groq_llm_model == "llama-3.3-70b-versatile"
    assert s.groq_whisper_model == "whisper-large-v3"
    assert 0.0 <= s.groq_temperature <= 2.0
    assert s.groq_max_tokens > 0
    assert s.edge_tts_voice == "de-DE-KatjaNeural"
    assert s.edge_tts_rate == "+0%"
    assert s.edge_tts_pitch == "+0Hz"
    assert s.audio_cache_dir == "./audio_cache"


def test_get_settings_is_cached() -> None:
    a = get_settings()
    b = get_settings()
    assert a is b


def test_settings_reads_env(monkeypatch) -> None:
    monkeypatch.setenv("GROQ_API_KEY", "abc-123")
    s = Settings()
    assert s.groq_api_key == "abc-123"
