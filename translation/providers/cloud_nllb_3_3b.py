import requests

from config import CONFIG
from core.interfaces.translation_interface import BaseTranslationProvider
from core.schemas.translation_schema import TranslationResult


class CloudNLLB33BProvider(BaseTranslationProvider):
    def __init__(self) -> None:
        self.api_base_url = CONFIG.cloud_api_base_url
        self.api_key = CONFIG.cloud_api_key
        self.timeout = CONFIG.cloud_timeout_seconds
        self.model_name = "facebook/nllb-200-3.3B"

    def load(self) -> None:
        return

    def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
    ) -> TranslationResult:
        if not self.api_base_url:
            raise ValueError("CLOUD_API_BASE_URL is not configured")

        payload = {
            "model": self.model_name,
            "text": text,
            "source_lang": source_lang,
            "target_lang": target_lang,
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

        return TranslationResult(
            source_text=text,
            translated_text=response_json.get("translated_text", ""),
            source_lang=source_lang,
            target_lang=target_lang,
            provider="cloud_nllb_3_3b",
            metadata={
                "model_name": self.model_name,
            },
        )