from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class BrainResult:
    user_text: str
    intent: str
    response_text: str
    mode: str = "standard"

    use_web: bool = False
    use_translation: bool = False
    use_emotion: bool = False

    action: Optional[str] = None
    translation_target: Optional[str] = None
    translation_text: Optional[str] = None

    provider: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)