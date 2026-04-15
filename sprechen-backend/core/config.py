"""Application configuration loaded from environment variables."""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "Sprechen"
    debug: bool = True

    # Groq
    groq_api_key: str = ""
    groq_llm_model: str = "llama-3.3-70b-versatile"
    groq_whisper_model: str = "whisper-large-v3"
    groq_temperature: float = 0.7
    groq_max_tokens: int = 1024

    # Edge TTS
    edge_tts_voice: str = "de-DE-KatjaNeural"
    edge_tts_rate: str = "+0%"
    edge_tts_pitch: str = "+0Hz"

    # Audio cache
    audio_cache_dir: str = "./audio_cache"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
