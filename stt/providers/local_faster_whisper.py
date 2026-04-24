import numpy as np
from faster_whisper import WhisperModel

from config import CONFIG
from core.interfaces.stt_interface import BaseSTTProvider
from core.schemas.stt_schema import STTResult, STTSegment


class LocalFasterWhisperProvider(BaseSTTProvider):
    def __init__(self) -> None:
        self._model = None

    def load(self) -> None:
        if self._model is None:
            self._model = WhisperModel(
                CONFIG.stt_model_name,
                device=CONFIG.stt_device,
                compute_type=CONFIG.stt_compute_type,
            )

    def transcribe_array(self, audio_array: np.ndarray, language: str) -> STTResult:
        self.load()

        segments, info = self._model.transcribe(
            audio_array,
            language=language,
            beam_size=CONFIG.stt_beam_size,
            best_of=CONFIG.stt_best_of,
            temperature=CONFIG.stt_temperature,
        )

        segment_list: list[STTSegment] = []
        full_text_parts: list[str] = []

        for seg in segments:
            text = seg.text.strip()
            if text:
                segment_list.append(
                    STTSegment(
                        start=seg.start,
                        end=seg.end,
                        text=text,
                    )
                )
                full_text_parts.append(text)

        return STTResult(
            text=" ".join(full_text_parts).strip(),
            language=getattr(info, "language", language),
            language_probability=getattr(info, "language_probability", None),
            duration=getattr(info, "duration", None),
            segments=segment_list,
            provider="local_faster_whisper",
        )