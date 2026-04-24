from abc import ABC, abstractmethod

from core.schemas.translation_schema import TranslationResult


class BaseTranslationProvider(ABC):
    @abstractmethod
    def load(self) -> None:
        pass

    @abstractmethod
    def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
    ) -> TranslationResult:
        pass