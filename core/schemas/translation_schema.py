from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_lang: str
    target_lang: str
    provider: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)