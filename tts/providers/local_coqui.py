from TTS.api import TTS

from config import CONFIG
from core.interfaces.tts_interface import BaseTTSProvider
from core.schemas.tts_schema import TTSResult


class LocalCoquiTTSProvider(BaseTTSProvider):
    def __init__(self) -> None:
        self._tts_model = None

    def load(self) -> None:
        if self._tts_model is None:
            self._tts_model = TTS(
                model_name=CONFIG.tts_model_name,
                progress_bar=True,
                gpu=CONFIG.tts_use_gpu,
            )

    def synthesize(
        self,
        text: str,
        mode: str = "standard",
        language: str = "fr",
        voice: str | None = None,
    ) -> TTSResult:
        self.load()

        self._tts_model.tts_to_file(
            text=text,
            file_path=CONFIG.tts_output_file,
        )

        return TTSResult(
            text=text,
            mode=mode,
            language=language,
            voice=voice or CONFIG.tts_default_voice,
            provider="local_coqui",
            file_path=CONFIG.tts_output_file,
        )