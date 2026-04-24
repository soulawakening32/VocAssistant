from config import CONFIG
from core.interfaces.tts_interface import BaseTTSProvider
from tts.providers.local_coqui import LocalCoquiTTSProvider
from tts.providers.cloud_qwen_customvoice import CloudQwenCustomVoiceProvider
from tts.providers.cloud_qwen_voicedesign import CloudQwenVoiceDesignProvider
from tts.providers.cloud_bark import CloudBarkProvider


def get_tts_provider() -> BaseTTSProvider:
    provider_name = CONFIG.active_tts_provider

    if provider_name == "local_coqui":
        return LocalCoquiTTSProvider()

    if provider_name == "cloud_qwen_customvoice":
        return CloudQwenCustomVoiceProvider()

    if provider_name == "cloud_qwen_voicedesign":
        return CloudQwenVoiceDesignProvider()

    if provider_name == "cloud_bark":
        return CloudBarkProvider()

    raise ValueError(f"Unsupported TTS provider: {provider_name}")