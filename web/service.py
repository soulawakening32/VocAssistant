from config import CONFIG
from web.providers.local_web_dummy import LocalWebDummyProvider


def get_web_provider():
    provider_name = CONFIG.active_web_provider

    if provider_name == "local_web_dummy":
        return LocalWebDummyProvider()

    raise ValueError(f"Unsupported web provider: {provider_name}")
