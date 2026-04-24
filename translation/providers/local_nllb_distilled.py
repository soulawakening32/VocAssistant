from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

from config import CONFIG
from core.interfaces.translation_interface import BaseTranslationProvider
from core.schemas.translation_schema import TranslationResult


class LocalNLLBDistilledProvider(BaseTranslationProvider):
    def __init__(self) -> None:
        self._model = None
        self._tokenizer = None

    def load(self) -> None:
        if self._model is None or self._tokenizer is None:
            self._tokenizer = AutoTokenizer.from_pretrained(CONFIG.translation_model_name)
            self._model = AutoModelForSeq2SeqLM.from_pretrained(CONFIG.translation_model_name)
            self._model.eval()

            if CONFIG.translation_device == "cuda" and torch.cuda.is_available():
                self._model = self._model.to("cuda")

    def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str,
    ) -> TranslationResult:
        self.load()

        clean_text = text.strip()
        if not clean_text:
            return TranslationResult(
                source_text=text,
                translated_text="",
                source_lang=source_lang,
                target_lang=target_lang,
                provider="local_nllb_distilled",
            )

        self._tokenizer.src_lang = source_lang
        inputs = self._tokenizer(clean_text, return_tensors="pt")

        if CONFIG.translation_device == "cuda" and torch.cuda.is_available():
            inputs = {k: v.to("cuda") for k, v in inputs.items()}

        forced_bos_token_id = self._tokenizer.convert_tokens_to_ids(target_lang)

        with torch.inference_mode():
            generated_tokens = self._model.generate(
                **inputs,
                forced_bos_token_id=forced_bos_token_id,
                max_new_tokens=CONFIG.translation_max_new_tokens,
            )

        translated_text = self._tokenizer.batch_decode(
            generated_tokens,
            skip_special_tokens=True,
        )[0]

        return TranslationResult(
            source_text=clean_text,
            translated_text=translated_text,
            source_lang=source_lang,
            target_lang=target_lang,
            provider="local_nllb_distilled",
        )