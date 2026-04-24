import requests
import tempfile
import soundfile as sf
import numpy as np

from config import CONFIG
from core.interfaces.stt_interface import BaseSTTProvider
from core.schemas.stt_schema import STTResult, STTSegment


class CloudFasterWhisperProvider(BaseSTTProvider):
    def __init__(self) -> None:
        self.api_base_url = CONFIG.cloud_api_base_url
        self.api_key = CONFIG.cloud_api_key
        self.timeout = CONFIG.cloud_timeout_seconds
        self.model_name = CONFIG.stt_model_name

    def load(self) -> None:
        return

    def transcribe_array(self, audio_array: np.ndarray, language: str) -> STTResult:
        if not self.api_base_url:
            raise ValueError("CLOUD_API_BASE_URL is not configured")

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            sf.write(tmp.name, audio_array, CONFIG.audio_sample_rate)
            temp_path = tmp.name

        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        data = {
            "language": language,
            "model": self.model_name,
        }

        with open(temp_path, "rb") as f:
            files = {
                "file": ("audio.wav", f, "audio/wav"),
            }

            response = requests.post(
                self.api_base_url,
                headers=headers,
                data=data,
                files=files,
                timeout=self.timeout,
            )

        response.raise_for_status()
        response_json = response.json()

        segments = [
            STTSegment(
                start=seg.get("start", 0.0),
                end=seg.get("end", 0.0),
                text=seg.get("text", ""),
            )
            for seg in response_json.get("segments", [])
        ]

        return STTResult(
            text=response_json.get("text", ""),
            language=response_json.get("language", language),
            language_probability=response_json.get("language_probability"),
            duration=response_json.get("duration"),
            segments=segments,
            provider="cloud_faster_whisper",
            metadata={
                "model_name": self.model_name,
            },
        )