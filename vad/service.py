from config import CONFIG
from vad.providers.local_webrtcvad import LocalWebRTCVADProvider


def get_vad_provider():
    provider_name = CONFIG.active_vad_provider

    if provider_name == "local_webrtcvad":
        return LocalWebRTCVADProvider()

    raise ValueError(f"Unsupported VAD provider: {provider_name}")