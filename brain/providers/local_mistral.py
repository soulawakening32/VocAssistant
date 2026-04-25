from typing import List, Optional
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

from core.interfaces.brain_interface import BaseBrainProvider
from core.schemas.brain_schema import BrainResult
from core.schemas.session_schema import Message


class LocalMistralProvider(BaseBrainProvider):

    def __init__(self):
        self.model = None
        self.tokenizer = None

    def load(self) -> None:
        if self.model is not None:
            return

        model_name = "mistralai/Mistral-7B-Instruct-v0.1"

        print("🔄 Loading Mistral model...")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )

        print("✅ Mistral loaded")

    def process(
        self,
        user_text: str,
        history: Optional[List[Message]] = None,
    ) -> BrainResult:

        self.load()

        prompt = self._build_prompt(user_text, history)

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=120,
                temperature=0.7,
                do_sample=True,
                top_p=0.9,
                repetition_penalty=1.2,
                eos_token_id=self.tokenizer.eos_token_id,      # 🔥 important
                pad_token_id=self.tokenizer.eos_token_id       # 🔥 bonus stabilité
            )

        # 🔥 EXTRACTION PROPRE DE LA RÉPONSE
        input_length = inputs["input_ids"].shape[1]
        generated_tokens = outputs[0][input_length:]

        response_text = self.tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True
        ).strip()

        return BrainResult(
            user_text=user_text,
            intent="general",
            response_text=response_text,
            mode="standard",
            use_web=False,
            use_translation=False,
            use_emotion=False,
            action="response",
            translation_target=None,
            translation_text=None,
            provider="local_mistral",
        )

    def _build_prompt(self, user_text: str, history: Optional[List[Message]]) -> str:
        system_prompt = (
            "Tu es un assistant vocal intelligent. "
            "Tu réponds uniquement à la question de l'utilisateur. "
            "Tu ne génères pas de Q/A, ni d'exercices, ni de contenu hors sujet. "
            "Réponds de manière claire, naturelle et concise."
        )

        return f"<s>[INST] {system_prompt}\n\n{user_text} [/INST]"