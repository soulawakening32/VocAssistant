from config import CONFIG
from core.interfaces.brain_interface import BaseBrainProvider
from brain.providers.local_rule_brain import LocalRuleBrainProvider
from brain.providers.cloud_r1_1776 import CloudR11776Provider


def get_brain_provider() -> BaseBrainProvider:
    provider_name = CONFIG.active_brain_provider

    if provider_name == "local_rule_brain":
        return LocalRuleBrainProvider()

    if provider_name == "cloud_r1_1776":
        return CloudR11776Provider()

    raise ValueError(f"Unsupported brain provider: {provider_name}")