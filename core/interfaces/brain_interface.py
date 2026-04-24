from abc import ABC, abstractmethod
from typing import List

from core.schemas.brain_schema import BrainResult
from core.schemas.session_schema import Message


class BaseBrainProvider(ABC):
    @abstractmethod
    def load(self) -> None:
        pass

    @abstractmethod
    def process(
        self,
        user_text: str,
        history: List[Message] | None = None,
    ) -> BrainResult:
        pass