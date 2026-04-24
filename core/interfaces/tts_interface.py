from abc import ABC, abstractmethod

from core.schemas.tts_schema import TTSResult


class BaseTTSProvider(ABC):
    @abstractmethod
    def load(self) -> None:
        pass

    @abstractmethod
    def synthesize(
        self,
        text: str,
        mode: str = "standard",
        language: str = "fr",
        voice: str | None = None,
    ) -> TTSResult:
        pass