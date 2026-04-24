from typing import Any, Dict, List, Optional

from config import CONFIG
from brain.service import get_brain_provider
from memory.service import get_memory_provider
from stt.service import get_stt_provider
from translation.service import get_translation_provider
from tts.service import get_tts_provider
from vad.service import get_vad_provider

from core.schemas.brain_schema import BrainResult
from core.schemas.session_schema import Message
from core.schemas.stt_schema import STTResult
from core.schemas.translation_schema import TranslationResult
from core.schemas.tts_schema import TTSResult


class AssistantOrchestrator:
    def __init__(self) -> None:
        self.vad_provider = get_vad_provider()
        self.stt_provider = get_stt_provider()
        self.brain_provider = get_brain_provider()
        self.translation_provider = get_translation_provider()
        self.tts_provider = get_tts_provider()
        self.memory_provider = get_memory_provider()

    def create_session(self, title: Optional[str] = None) -> str:
        session_title = title or CONFIG.default_session_name
        return self.memory_provider.create_session(session_title)

    def record_audio(self):
        return self.vad_provider.record_utterance()

    def transcribe_audio(self, audio_array) -> STTResult:
        return self.stt_provider.transcribe_array(
            audio_array=audio_array,
            language=CONFIG.stt_language,
        )

    def process_text(self, user_text: str, session_id: str) -> Dict[str, Any]:
        history: List[Message] = []
        if CONFIG.enable_memory:
            history = self.memory_provider.get_session_history(session_id)

        brain_result: BrainResult = self.brain_provider.process(
            user_text=user_text,
            history=history,
        )

        response_text = brain_result.response_text
        translation_result: Optional[TranslationResult] = None

        if CONFIG.enable_translation and brain_result.use_translation:
            translation_text = brain_result.translation_text or user_text
            target_lang = brain_result.translation_target or CONFIG.translation_target_lang

            translation_result = self.translation_provider.translate(
                text=translation_text,
                source_lang=CONFIG.translation_source_lang,
                target_lang=target_lang,
            )
            response_text = translation_result.translated_text

        if CONFIG.enable_memory:
            self.memory_provider.save_message(session_id, "user", user_text)
            self.memory_provider.save_message(session_id, "assistant", response_text)

        tts_result: TTSResult = self.tts_provider.synthesize(
            text=response_text,
            mode=brain_result.mode,
            language=self._resolve_tts_language(translation_result),
            voice=CONFIG.tts_default_voice,
        )

        return {
            "user_text": user_text,
            "brain_result": brain_result,
            "translation_result": translation_result,
            "response_text": response_text,
            "tts_result": tts_result,
        }

    def run_once(self, session_id: str) -> Optional[Dict[str, Any]]:
        audio = self.record_audio()
        if audio is None:
            return None

        stt_result = self.transcribe_audio(audio)
        if not stt_result.text.strip():
            return None

        pipeline_result = self.process_text(stt_result.text, session_id=session_id)
        pipeline_result["stt_result"] = stt_result
        return pipeline_result

    def _resolve_tts_language(
        self,
        translation_result: Optional[TranslationResult],
    ) -> str:
        if translation_result is not None:
            mapping = {
                "fra_Latn": "fr",
                "eng_Latn": "en",
                "arb_Arab": "ar",
            }
            return mapping.get(
                translation_result.target_lang,
                CONFIG.tts_default_language,
            )

        return CONFIG.tts_default_language
    
orchestrator = AssistantOrchestrator()