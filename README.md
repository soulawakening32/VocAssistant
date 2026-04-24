# Voice Assistant - Pre-Cloud Backend

Assistant vocal modulaire pensé pour évoluer du local vers le cloud.

## Stack finale visée

- STT: Whisper large-v3 + faster-whisper
- VAD: Silero VAD
- Brain: R1 1776 Q6
- Translation: NLLB-200-3.3B
- TTS:
  - Qwen3-TTS-12Hz-0.6B-CustomVoice
  - Qwen3-TTS-12Hz-1.7B-VoiceDesign
  - Bark (mode studio / premium)
- Memory: Qdrant
- Web: Tavily
- Emotion: Emotion2Vec+ Large

## Stack locale actuelle de dev

- VAD local
- faster-whisper (provider local configurable)
- brain local à règles
- traduction locale allégée
- TTS local Coqui
- mémoire locale JSON
- API FastAPI

## Endpoints actuels

- `GET /health`
- `POST /chat`
- `POST /translate`
- `POST /tts`
- `POST /transcribe`
- `POST /voice-chat`

## Lancement local

Activer l'environnement Python, puis :

```bash
python -m uvicorn api.app:app --reload