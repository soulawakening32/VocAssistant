import requests

from config import CONFIG
from core.interfaces.tts_interface import BaseTTSProvider
from core.schemas.tts_schema import TTSResult


class CloudQwenCustomVoiceProvider(BaseTTSProvider):
    def __init__(self) -> None:
        self.backend = CONFIG.tts_backend
        self.api_base_url = CONFIG.tts_api_base_url
        self.api_key = CONFIG.tts_api_key
        self.timeout = CONFIG.tts_timeout_seconds
        self.model_name = CONFIG.tts_qwen_customvoice_model_name
        self.enable_streaming = CONFIG.tts_enable_streaming

    def load(self) -> None:
        return

    def synthesize(
        self,
        text: str,
        mode: str = "standard",
        language: str = "fr",
        voice: str | None = None,
    ) -> TTSResult:
        if not self.api_base_url:
            raise ValueError("TTS_API_BASE_URL is not configured")

        payload = {
            "model": self.model_name,
            "text": text,
            "language": language,
            "voice": voice or CONFIG.tts_default_voice,
            "mode": mode,
            "stream": False,
            "metadata": {
                "backend": self.backend,
                "provider": "cloud_qwen_customvoice",
                "enable_streaming": self.enable_streaming,
            },
        }

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        response = requests.post(
            self.api_base_url,
            json=payload,
            headers=headers,
            timeout=self.timeout,
        )
        response.raise_for_status()
        response_json = response.json()

        return TTSResult(
            text=text,
            mode=mode,
            language=language,
            voice=voice or CONFIG.tts_default_voice,
            provider="cloud_qwen_customvoice",
            file_path=response_json.get("file_path"),
            audio_url=response_json.get("audio_url"),
            metadata={
                "backend": self.backend,
                "model_name": self.model_name,
            },
        )