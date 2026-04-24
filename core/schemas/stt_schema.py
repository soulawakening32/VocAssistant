from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class STTSegment:
    start: float
    end: float
    text: str


@dataclass
class STTResult:
    text: str
    language: Optional[str] = None
    language_probability: Optional[float] = None
    duration: Optional[float] = None
    segments: List[STTSegment] = field(default_factory=list)
    provider: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)