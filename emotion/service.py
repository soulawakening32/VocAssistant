from config import CONFIG
from emotion.providers.local_emotion_dummy import LocalEmotionDummyProvider


def get_emotion_provider():
    provider_name = CONFIG.active_emotion_provider

    if provider_name == "local_emotion_dummy":
        return LocalEmotionDummyProvider()

    raise ValueError(f"Unsupported emotion provider: {provider_name}")