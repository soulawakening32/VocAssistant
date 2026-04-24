from typing import List

from core.interfaces.memory_interface import BaseMemoryProvider
from core.schemas.session_schema import Message, Session


class QdrantMemoryProvider(BaseMemoryProvider):
    def __init__(self) -> None:
        self._client = None

    def load(self) -> None:
        raise NotImplementedError("Qdrant provider not implemented yet")

    def create_session(self, title: str) -> str:
        raise NotImplementedError("Qdrant provider not implemented yet")

    def save_message(self, session_id: str, role: str, text: str) -> None:
        raise NotImplementedError("Qdrant provider not implemented yet")

    def get_session_history(self, session_id: str) -> List[Message]:
        raise NotImplementedError("Qdrant provider not implemented yet")

    def get_session(self, session_id: str) -> Session | None:
        raise NotImplementedError("Qdrant provider not implemented yet")
