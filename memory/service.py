from config import CONFIG
from core.interfaces.memory_interface import BaseMemoryProvider
from memory.providers.local_json_memory import LocalJsonMemoryProvider
from memory.providers.qdrant_memory import QdrantMemoryProvider


def get_memory_provider() -> BaseMemoryProvider:
    provider_name = CONFIG.active_memory_provider

    if provider_name == "local_json_memory":
        return LocalJsonMemoryProvider()

    if provider_name == "qdrant_memory":
        return QdrantMemoryProvider()

    raise ValueError(f"Unsupported memory provider: {provider_name}")
