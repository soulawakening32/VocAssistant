from abc import ABC, abstractmethod
from typing import List

from core.schemas.session_schema import Message, Session


class BaseMemoryProvider(ABC):
    @abstractmethod
    def create_session(self, title: str) -> str:
        pass

    @abstractmethod
    def save_message(self, session_id: str, role: str, text: str) -> None:
        pass

    @abstractmethod
    def get_session_history(self, session_id: str) -> List[Message]:
        pass

    @abstractmethod
    def get_session(self, session_id: str) -> Session | None:
        pass
