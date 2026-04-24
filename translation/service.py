from config import CONFIG
from core.interfaces.translation_interface import BaseTranslationProvider
from translation.providers.local_nllb_distilled import LocalNLLBDistilledProvider
from translation.providers.cloud_nllb_3_3b import CloudNLLB33BProvider


def get_translation_provider() -> BaseTranslationProvider:
    provider_name = CONFIG.active_translation_provider

    if provider_name == "local_nllb_distilled":
        return LocalNLLBDistilledProvider()

    if provider_name == "cloud_nllb_3_3b":
        return CloudNLLB33BProvider()

    raise ValueError(f"Unsupported translation provider: {provider_name}")