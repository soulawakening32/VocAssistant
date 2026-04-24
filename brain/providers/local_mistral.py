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
                max_new_tokens=150,
                temperature=0.7,
                do_sample=True,
            )

        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        response_text = generated_text.replace(prompt, "").strip()

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
        prompt = ""

        if history:
            for msg in history[-5:]:
                role = "User" if msg.role == "user" else "Assistant"
                prompt += f"{role}: {msg.content}\n"

        prompt += f"User: {user_text}\nAssistant:"

        return prompt
