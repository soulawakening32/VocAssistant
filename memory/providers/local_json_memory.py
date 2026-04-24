import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import List

from config import CONFIG
from core.interfaces.memory_interface import BaseMemoryProvider
from core.schemas.session_schema import Message, Session


class LocalJsonMemoryProvider(BaseMemoryProvider):
    def __init__(self) -> None:
        self.base_dir = Path(CONFIG.memory_local_base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _session_path(self, session_id: str) -> Path:
        return self.base_dir / f"{session_id}.json"

    def _now(self) -> str:
        return datetime.utcnow().isoformat()

    def create_session(self, title: str) -> str:
        session_id = title.strip().replace(" ", "_").lower()
        session = Session(
            session_id=session_id,
            title=title,
            created_at=self._now(),
            updated_at=self._now(),
            messages=[],
            metadata={},
        )
        self._write_session(session)
        return session_id

    def save_message(self, session_id: str, role: str, text: str) -> None:
        session = self.get_session(session_id)
        if session is None:
            session = Session(
                session_id=session_id,
                title=session_id,
                created_at=self._now(),
                updated_at=self._now(),
                messages=[],
                metadata={},
            )

        session.messages.append(
            Message(
                role=role,
                text=text,
                timestamp=self._now(),
            )
        )
        session.updated_at = self._now()
        self._write_session(session)

    def get_session_history(self, session_id: str) -> List[Message]:
        session = self.get_session(session_id)
        if session is None:
            return []
        return session.messages

    def get_session(self, session_id: str) -> Session | None:
        path = self._session_path(session_id)
        if not path.exists():
            return None

        with path.open("r", encoding="utf-8") as f:
            raw = json.load(f)

        messages = [
            Message(
                role=msg["role"],
                text=msg["text"],
                timestamp=msg.get("timestamp"),
                language=msg.get("language"),
                metadata=msg.get("metadata", {}),
            )
            for msg in raw.get("messages", [])
        ]

        return Session(
            session_id=raw["session_id"],
            title=raw.get("title"),
            created_at=raw.get("created_at"),
            updated_at=raw.get("updated_at"),
            messages=messages,
            metadata=raw.get("metadata", {}),
        )

    def _write_session(self, session: Session) -> None:
        path = self._session_path(session.session_id)
        with path.open("w", encoding="utf-8") as f:
            json.dump(asdict(session), f, ensure_ascii=False, indent=2)