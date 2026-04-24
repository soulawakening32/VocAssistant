from typing import List

from core.interfaces.brain_interface import BaseBrainProvider
from core.schemas.brain_schema import BrainResult
from core.schemas.session_schema import Message


class LocalRuleBrainProvider(BaseBrainProvider):
    def load(self) -> None:
        return

    def process(
        self,
        user_text: str,
        history: List[Message] | None = None,
    ) -> BrainResult:
        history = history or []
        text = user_text.strip()
        lowered = text.lower()

        intent = self._detect_intent(lowered)
        mode = self._choose_response_mode(lowered, intent)

        translation_target = None
        translation_text = None

        if intent == "translation":
            translation_target = self._detect_translation_target(lowered)
            translation_text = text

        response_text = self._generate_local_response(text, intent, history)

        return BrainResult(
            user_text=text,
            intent=intent,
            response_text=response_text,
            mode=mode,
            use_web=False,
            use_translation=(intent == "translation"),
            use_emotion=False,
            action=intent,
            translation_target=translation_target,
            translation_text=translation_text,
            provider="local_rule_brain",
        )

    def _detect_intent(self, text: str) -> str:
        if not text:
            return "empty"

        if any(w in text for w in ["bonjour", "salut", "hello", "hi"]):
            return "greeting"

        if any(w in text for w in ["ça va", "ca va", "how are you"]):
            return "wellbeing"

        if any(w in text for w in ["qui es tu", "tu es qui", "who are you"]):
            return "identity"

        if any(w in text for w in ["merci", "thanks", "thank you"]):
            return "thanks"

        if "heure" in text or "time" in text:
            return "time_request"

        if any(w in text for w in ["traduis", "translate"]):
            return "translation"

        return "general"

    def _detect_translation_target(self, text: str) -> str:
        if "anglais" in text or "english" in text:
            return "eng_Latn"
        if "français" in text or "french" in text:
            return "fra_Latn"
        return "eng_Latn"

    def _choose_response_mode(self, text: str, intent: str) -> str:
        if intent in ["greeting", "wellbeing", "identity", "thanks"]:
            return "expressive"
        return "standard"

    def _generate_local_response(self, user_text: str, intent: str, history: List[Message]) -> str:

        if intent == "empty":
            return "Je n'ai rien entendu clairement."

        if intent == "greeting":
            return "Salut 😊 comment tu vas ?"

        if intent == "wellbeing":
            return "Je vais très bien, merci. Et toi ?"

        if intent == "identity":
            return "Je suis ton assistant vocal intelligent."

        if intent == "thanks":
            return "Avec plaisir 😊"

        if intent == "time_request":
            return "Je ne donne pas encore l'heure réelle."

        if intent == "translation":
            return "Je vais traduire ça."

        return f"Hmm… tu viens de dire : {user_text}"
