from config import CONFIG
from files.providers.local_files_dummy import LocalFilesDummyProvider


def get_files_provider():
    provider_name = CONFIG.active_files_provider

    if provider_name == "local_files_dummy":
        return LocalFilesDummyProvider()

    raise ValueError(f"Unsupported files provider: {provider_name}")
