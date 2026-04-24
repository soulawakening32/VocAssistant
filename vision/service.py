from config import CONFIG
from vision.providers.local_vision_dummy import LocalVisionDummyProvider


def get_vision_provider():
    provider_name = CONFIG.active_vision_provider

    if provider_name == "local_vision_dummy":
        return LocalVisionDummyProvider()

    raise ValueError(f"Unsupported vision provider: {provider_name}")
