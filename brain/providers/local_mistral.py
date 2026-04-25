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
            )

        input_length = inputs["input_ids"].shape[1]

        generated_tokens = outputs[0][input_length:]

        response_text = self.tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
        


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

        def _build_prompt(self, user_text: str, history):
             return f"<s>[INST] Tu es un assistant intelligent. Réponds clairement.\n\n{user_text} [/INST]"


        return prompt
