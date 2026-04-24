import requests
from typing import List

from config import CONFIG
from core.interfaces.brain_interface import BaseBrainProvider
from core.schemas.brain_schema import BrainResult
from core.schemas.session_schema import Message


class CloudR11776Provider(BaseBrainProvider):
    def __init__(self) -> None:
        self.backend = CONFIG.brain_backend
        self.engine = CONFIG.brain_inference_engine
        self.model_name = CONFIG.brain_model_name
        self.api_base_url = CONFIG.brain_api_base_url
        self.api_key = CONFIG.brain_api_key
        self.timeout = CONFIG.brain_timeout_seconds
        self.max_model_len = CONFIG.brain_max_model_len
        self.kv_cache_dtype = CONFIG.brain_kv_cache_dtype
        self.gpu_type = CONFIG.brain_gpu_type
        self.use_quantization = CONFIG.brain_use_quantization
        self.quantization_mode = CONFIG.brain_quantization_mode
        self.enable_streaming = CONFIG.brain_enable_streaming

    def load(self) -> None:
        return

    def process(
        self,
        user_text: str,
        history: List[Message] | None = None,
    ) -> BrainResult:
        history = history or []

        if not self.api_base_url:
            raise ValueError("BRAIN_API_BASE_URL is not configured")

        payload = self._build_payload(user_text=user_text, history=history)
        response_json = self._call_backend(payload)

        return self._parse_response(
            user_text=user_text,
            response_json=response_json,
        )

    def _build_payload(self, user_text: str, history: List[Message]) -> dict:
        messages = []

        system_prompt = (
            "You are the cloud brain of a voice assistant. "
            "Return structured reasoning outputs for assistant orchestration."
        )
        messages.append({"role": "system", "content": system_prompt})

        for msg in history[-12:]:
            messages.append(
                {
                    "role": msg.role,
                    "content": msg.text,
                }
            )

        messages.append({"role": "user", "content": user_text})

        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 512,
            "stream": False,
            "metadata": {
                "backend": self.backend,
                "engine": self.engine,
                "max_model_len": self.max_model_len,
                "kv_cache_dtype": self.kv_cache_dtype,
                "gpu_type": self.gpu_type,
                "use_quantization": self.use_quantization,
                "quantization_mode": self.quantization_mode,
                "enable_streaming": self.enable_streaming,
            },
        }

        return payload

    def _call_backend(self, payload: dict) -> dict:
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
        return response.json()

    def _parse_response(self, user_text: str, response_json: dict) -> BrainResult:
        text_output = self._extract_text(response_json).strip()

        intent = self._detect_intent(user_text)
        translation_target = None
        translation_text = None

        if intent == "translation":
            translation_target = self._detect_translation_target(user_text)
            translation_text = self._extract_text_to_translate(user_text)

        return BrainResult(
            user_text=user_text,
            intent=intent,
            response_text=text_output if text_output else "Je n'ai pas pu générer une réponse.",
            mode=self._choose_response_mode(user_text, intent),
            use_web=self._should_use_web(user_text),
            use_translation=(intent == "translation"),
            use_emotion=self._should_use_emotion(user_text),
            action=intent,
            translation_target=translation_target,
            translation_text=translation_text,
            provider="cloud_r1_1776",
            metadata={
                "backend": self.backend,
                "engine": self.engine,
                "model_name": self.model_name,
                "kv_cache_dtype": self.kv_cache_dtype,
                "quantization_mode": self.quantization_mode,
            },
        )

    def _extract_text(self, response_json: dict) -> str:
        if "choices" in response_json and response_json["choices"]:
            choice = response_json["choices"][0]
            message = choice.get("message", {})
            return message.get("content", "") or ""

        if "output_text" in response_json:
            return response_json["output_text"] or ""

        if "text" in response_json:
            return response_json["text"] or ""

        return ""

    def _detect_intent(self, user_text: str) -> str:
        text = user_text.lower().strip()

        if not text:
            return "empty"
        if "traduis" in text or "traduire" in text or "translate" in text:
            return "translation"
        if "bonjour" in text or "salut" in text:
            return "greeting"
        if "ça va" in text or "ca va" in text:
            return "wellbeing"
        if "quel est ton nom" in text or "comment tu t'appelles" in text:
            return "identity"
        if "heure" in text:
            return "time_request"
        if "merci" in text:
            return "thanks"
        if "qui es tu" in text or "tu es qui" in text:
            return "identity"
        return "general"

    def _detect_translation_target(self, user_text: str) -> str:
        text = user_text.lower()

        if "anglais" in text or "english" in text:
            return "eng_Latn"
        if "français" in text or "francais" in text or "french" in text:
            return "fra_Latn"
        if "arabe" in text or "arabic" in text:
            return "arb_Arab"

        return "eng_Latn"

    def _extract_text_to_translate(self, user_text: str) -> str:
        text = user_text.strip()
        lower = text.lower()

        patterns = [
            "traduis ceci en anglais :",
            "traduis ceci en anglais",
            "traduis en anglais :",
            "traduis en anglais",
            "traduire en anglais :",
            "traduire en anglais",
            "translate to english :",
            "translate to english",
            "traduis ceci en arabe :",
            "traduis ceci en arabe",
            "traduis en arabe :",
            "traduis en arabe",
            "traduire en arabe :",
            "traduire en arabe",
            "translate to arabic :",
            "translate to arabic",
            "traduis ceci en français :",
            "traduis ceci en français",
            "traduis ceci en francais",
            "traduis en français :",
            "traduis en français",
            "traduis en francais :",
            "traduis en francais",
            "traduire en français :",
            "traduire en français",
            "traduire en francais :",
            "traduire en francais",
            "translate to french :",
            "translate to french",
        ]

        for pattern in patterns:
            if pattern in lower:
                start_index = lower.find(pattern) + len(pattern)
                extracted = text[start_index:].strip(" :,-")
                if extracted:
                    return extracted

        words_to_remove = [
            "traduis", "traduire", "traduction", "ceci",
            "en anglais", "en arabe", "en français", "en francais",
            "translate", "to english", "to arabic", "to french",
        ]

        cleaned = lower
        for item in words_to_remove:
            cleaned = cleaned.replace(item, "")

        return cleaned.strip(" :,-")

    def _should_use_web(self, user_text: str) -> bool:
        text = user_text.lower()
        web_keywords = [
            "actualité", "news", "prix", "météo", "meteo", "aujourd'hui",
            "maintenant", "actuel", "cherche", "recherche",
            "vérifie", "verifie", "internet", "web",
        ]
        return any(keyword in text for keyword in web_keywords)

    def _should_use_emotion(self, user_text: str) -> bool:
        text = user_text.lower()
        emotion_keywords = [
            "triste", "heureux", "stressé", "stresse", "énervé",
            "enerve", "émotion", "emotion",
        ]
        return any(keyword in text for keyword in emotion_keywords)

    def _choose_response_mode(self, user_text: str, intent: str) -> str:
        text = user_text.lower()
        if any(word in text for word in ["chante", "joue", "raconte", "imite", "théâtral", "theatral"]):
            return "studio"
        if intent in ["greeting", "wellbeing", "identity", "thanks"]:
            return "expressive"
        return "standard"