from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class TTSResult:
    text: str
    mode: str = "standard"
    language: Optional[str] = None
    voice: Optional[str] = None
    provider: Optional[str] = None
    file_path: Optional[str] = None
    audio_url: Optional[str] = None
    duration: Optional[float] = None
    used_fallback: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)