import os
from dataclasses import dataclass
from typing import Optional


def _get_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    return int(value)


def _get_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    return float(value)


def _get_str(name: str, default: str) -> str:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    return value.strip()


def _get_optional_str(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    if value is None:
        return default
    value = value.strip()
    return value if value else default


@dataclass(frozen=True)
class AppConfig:
    app_env: str
    app_debug: bool
    app_name: str
    log_level: str

    default_language: str
    default_response_mode: str
    default_session_name: str

    active_vad_provider: str
    active_stt_provider: str
    active_brain_provider: str
    active_translation_provider: str
    active_tts_provider: str
    active_memory_provider: str
    active_emotion_provider: str
    active_web_provider: str
    active_vision_provider: str
    active_files_provider: str

    enable_web: bool
    enable_translation: bool
    enable_emotion: bool
    enable_vision: bool
    enable_files: bool
    enable_memory: bool

    stt_model_name: str
    stt_device: str
    stt_compute_type: str
    stt_language: str
    stt_beam_size: int
    stt_best_of: int
    stt_temperature: float

    audio_sample_rate: int
    audio_channels: int
    audio_frame_duration_ms: int

    vad_aggressiveness: int
    vad_start_trigger_frames: int
    vad_end_trigger_frames: int
    vad_max_record_seconds: int

    translation_model_name: str
    translation_device: str
    translation_source_lang: str
    translation_target_lang: str
    translation_max_new_tokens: int

    tts_model_name: str
    tts_use_gpu: bool
    tts_output_file: str
    tts_default_voice: Optional[str]
    tts_default_language: str

    tts_backend: str
    tts_api_base_url: Optional[str]
    tts_api_key: Optional[str]
    tts_timeout_seconds: int
    tts_enable_streaming: bool
    tts_standard_provider_name: str
    tts_premium_provider_name: str
    tts_studio_provider_name: str
    tts_qwen_customvoice_model_name: str
    tts_qwen_voicedesign_model_name: str
    tts_bark_model_name: str

    memory_local_base_dir: str
    qdrant_url: Optional[str]
    qdrant_api_key: Optional[str]
    qdrant_collection_name: str

    tavily_api_key: Optional[str]

    cloud_api_base_url: Optional[str]
    cloud_api_key: Optional[str]
    cloud_timeout_seconds: int

    brain_model_name: str
    brain_backend: str
    brain_inference_engine: str
    brain_api_base_url: Optional[str]
    brain_api_key: Optional[str]
    brain_timeout_seconds: int
    brain_max_model_len: int
    brain_kv_cache_dtype: str
    brain_gpu_type: str
    brain_use_quantization: bool
    brain_quantization_mode: str
    brain_enable_streaming: bool

    subscription_default_tier: str
    premium_fair_use_enabled: bool


def load_config() -> AppConfig:
    return AppConfig(
        app_env=_get_str("APP_ENV", "local"),
        app_debug=_get_bool("APP_DEBUG", True),
        app_name=_get_str("APP_NAME", "voice_assistant"),
        log_level=_get_str("LOG_LEVEL", "INFO"),

        default_language=_get_str("DEFAULT_LANGUAGE", "fr"),
        default_response_mode=_get_str("DEFAULT_RESPONSE_MODE", "standard"),
        default_session_name=_get_str("DEFAULT_SESSION_NAME", "conversation_locale"),

        active_vad_provider=_get_str("ACTIVE_VAD_PROVIDER", "local_webrtcvad"),
        active_stt_provider=_get_str("ACTIVE_PROVIDER", "local_faster_whisper"),
        active_brain_provider=_get_str("ACTIVE_BRAIN_PROVIDER", "local_mistral"),
        active_translation_provider=_get_str("ACTIVE_TRANSLATION_PROVIDER", "local_nllb_distilled"),
        active_tts_provider=_get_str("ACTIVE_TTS_PROVIDER", "local_coqui"),
        active_memory_provider=_get_str("ACTIVE_MEMORY_PROVIDER", "local_json_memory"),
        active_emotion_provider=_get_str("ACTIVE_EMOTION_PROVIDER", "local_emotion_dummy"),
        active_web_provider=_get_str("ACTIVE_WEB_PROVIDER", "local_web_dummy"),
        active_vision_provider=_get_str("ACTIVE_VISION_PROVIDER", "local_vision_dummy"),
        active_files_provider=_get_str("ACTIVE_FILES_PROVIDER", "local_files_dummy"),

        enable_web=_get_bool("ENABLE_WEB", False),
        enable_translation=_get_bool("ENABLE_TRANSLATION", True),
        enable_emotion=_get_bool("ENABLE_EMOTION", False),
        enable_vision=_get_bool("ENABLE_VISION", False),
        enable_files=_get_bool("ENABLE_FILES", False),
        enable_memory=_get_bool("ENABLE_MEMORY", True),

        stt_model_name=_get_str("STT_MODEL_NAME", "small"),
        stt_device=_get_str("STT_DEVICE", "cpu"),
        stt_compute_type=_get_str("STT_COMPUTE_TYPE", "int8"),
        stt_language=_get_str("STT_LANGUAGE", "fr"),
        stt_beam_size=_get_int("STT_BEAM_SIZE", 1),
        stt_best_of=_get_int("STT_BEST_OF", 1),
        stt_temperature=_get_float("STT_TEMPERATURE", 0.0),

        audio_sample_rate=_get_int("AUDIO_SAMPLE_RATE", 16000),
        audio_channels=_get_int("AUDIO_CHANNELS", 1),
        audio_frame_duration_ms=_get_int("AUDIO_FRAME_DURATION_MS", 30),

        vad_aggressiveness=_get_int("VAD_AGGRESSIVENESS", 2),
        vad_start_trigger_frames=_get_int("VAD_START_TRIGGER_FRAMES", 5),
        vad_end_trigger_frames=_get_int("VAD_END_TRIGGER_FRAMES", 20),
        vad_max_record_seconds=_get_int("VAD_MAX_RECORD_SECONDS", 15),

        translation_model_name=_get_str("TRANSLATION_MODEL_NAME", "facebook/nllb-200-distilled-600M"),
        translation_device=_get_str("TRANSLATION_DEVICE", "cpu"),
        translation_source_lang=_get_str("TRANSLATION_SOURCE_LANG", "fra_Latn"),
        translation_target_lang=_get_str("TRANSLATION_TARGET_LANG", "eng_Latn"),
        translation_max_new_tokens=_get_int("TRANSLATION_MAX_NEW_TOKENS", 256),

        tts_model_name=_get_str("TTS_MODEL_NAME", "tts_models/fr/css10/vits"),
        tts_use_gpu=_get_bool("TTS_USE_GPU", False),
        tts_output_file=_get_str("TTS_OUTPUT_FILE", "tts_output.wav"),
        tts_default_voice=_get_optional_str("TTS_DEFAULT_VOICE", None),
        tts_default_language=_get_str("TTS_DEFAULT_LANGUAGE", "fr"),

        tts_backend=_get_str("TTS_BACKEND", "runpod"),
        tts_api_base_url=_get_optional_str("TTS_API_BASE_URL", None),
        tts_api_key=_get_optional_str("TTS_API_KEY", None),
        tts_timeout_seconds=_get_int("TTS_TIMEOUT_SECONDS", 180),
        tts_enable_streaming=_get_bool("TTS_ENABLE_STREAMING", True),
        tts_standard_provider_name=_get_str("TTS_STANDARD_PROVIDER_NAME", "cloud_qwen_customvoice"),
        tts_premium_provider_name=_get_str("TTS_PREMIUM_PROVIDER_NAME", "cloud_qwen_voicedesign"),
        tts_studio_provider_name=_get_str("TTS_STUDIO_PROVIDER_NAME", "cloud_bark"),
        tts_qwen_customvoice_model_name=_get_str(
            "TTS_QWEN_CUSTOMVOICE_MODEL_NAME",
            "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
        ),
        tts_qwen_voicedesign_model_name=_get_str(
            "TTS_QWEN_VOICEDESIGN_MODEL_NAME",
            "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
        ),
        tts_bark_model_name=_get_str(
            "TTS_BARK_MODEL_NAME",
            "suno/bark",
        ),

        memory_local_base_dir=_get_str("MEMORY_LOCAL_BASE_DIR", "memory_store"),
        qdrant_url=_get_optional_str("QDRANT_URL", None),
        qdrant_api_key=_get_optional_str("QDRANT_API_KEY", None),
        qdrant_collection_name=_get_str("QDRANT_COLLECTION_NAME", "assistant_memory"),

        tavily_api_key=_get_optional_str("TAVILY_API_KEY", None),

        cloud_api_base_url=_get_optional_str("CLOUD_API_BASE_URL", None),
        cloud_api_key=_get_optional_str("CLOUD_API_KEY", None),
        cloud_timeout_seconds=_get_int("CLOUD_TIMEOUT_SECONDS", 120),

        brain_model_name=_get_str(
            "BRAIN_MODEL_NAME",
            "bartowski/perplexity-ai_r1-1776-GGUF",
        ),
        brain_backend=_get_str("BRAIN_BACKEND", "runpod"),
        brain_inference_engine=_get_str("BRAIN_INFERENCE_ENGINE", "vllm"),
        brain_api_base_url=_get_optional_str("BRAIN_API_BASE_URL", None),
        brain_api_key=_get_optional_str("BRAIN_API_KEY", None),
        brain_timeout_seconds=_get_int("BRAIN_TIMEOUT_SECONDS", 180),
        brain_max_model_len=_get_int("BRAIN_MAX_MODEL_LEN", 8192),
        brain_kv_cache_dtype=_get_str("BRAIN_KV_CACHE_DTYPE", "fp8"),
        brain_gpu_type=_get_str("BRAIN_GPU_TYPE", "A100_80GB"),
        brain_use_quantization=_get_bool("BRAIN_USE_QUANTIZATION", True),
        brain_quantization_mode=_get_str("BRAIN_QUANTIZATION_MODE", "q6"),
        brain_enable_streaming=_get_bool("BRAIN_ENABLE_STREAMING", True),

        subscription_default_tier=_get_str("SUBSCRIPTION_DEFAULT_TIER", "free"),
        premium_fair_use_enabled=_get_bool("PREMIUM_FAIR_USE_ENABLED", True),
    )


CONFIG = load_config()