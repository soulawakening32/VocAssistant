from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import soundfile as sf
import tempfile
import subprocess
import os
import uuid

from core.orchestrator import orchestrator

app = FastAPI()

# ✅ CORS (important pour le HTML local)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/voice")
async def voice(file: UploadFile = File(...)):

    try:
        # ----------------------------
        # 1. SAVE WEBM
        # ----------------------------
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            tmp.write(await file.read())
            webm_path = tmp.name

        wav_path = webm_path.replace(".webm", ".wav")

        # ----------------------------
        # 2. CONVERT WEBM → WAV
        # ----------------------------
        subprocess.run([
            "ffmpeg",
            "-i", webm_path,
            "-ar", "16000",
            "-ac", "1",
            wav_path
        ])

        # ----------------------------
        # 3. READ AUDIO
        # ----------------------------
        audio, samplerate = sf.read(wav_path)

        # ----------------------------
        # 4. STT + BRAIN
        # ----------------------------
        stt_result = orchestrator.transcribe_audio(audio)

        if not stt_result.text.strip():
            return {"error": "no speech detected"}

        result = orchestrator.process_text(
            stt_result.text,
            session_id="user_1"
        )

        # ✅ CORRECTION ICI
        text = result["response_text"]

        print("🧠 USER:", stt_result.text)
        print("🤖 RESPONSE:", text)

        # ----------------------------
        # 5. TTS
        # ----------------------------
        from TTS.api import TTS

        tts = TTS(model_name="tts_models/fr/css10/vits")

        output_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.wav")
        
        tts.tts_to_file(text=text, file_path=output_path)
        
        print("🔊 AUDIO FILE:", output_path)

        # ----------------------------
        # 6. CLEAN INPUT FILES
        # ----------------------------
        os.remove(webm_path)
        os.remove(wav_path)

        # ----------------------------
        # 7. RETURN AUDIO
        # ----------------------------
        return FileResponse(output_path, media_type="audio/wav")

    except Exception as e:
        print("❌ ERROR:", str(e))
        return {"error": str(e)}