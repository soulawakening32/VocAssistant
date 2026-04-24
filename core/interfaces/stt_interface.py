from abc import ABC, abstractmethod
import numpy as np

from core.schemas.stt_schema import STTResult


class BaseSTTProvider(ABC):
    @abstractmethod
    def load(self) -> None:
        pass

    @abstractmethod
    def transcribe_array(self, audio_array: np.ndarray, language: str) -> STTResult:
        pass