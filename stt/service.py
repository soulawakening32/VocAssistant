from config import CONFIG
from core.interfaces.stt_interface import BaseSTTProvider
from stt.providers.local_faster_whisper import LocalFasterWhisperProvider
from stt.providers.cloud_faster_whisper import CloudFasterWhisperProvider


def get_stt_provider() -> BaseSTTProvider:
    provider_name = CONFIG.active_stt_provider

    if provider_name == "local_faster_whisper":
        return LocalFasterWhisperProvider()

    if provider_name == "cloud_faster_whisper":
        return CloudFasterWhisperProvider()

    raise ValueError(f"Unsupported STT provider: {provider_name}")