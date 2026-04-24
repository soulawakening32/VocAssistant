import collections
import queue
from typing import Optional

import numpy as np
import sounddevice as sd
import webrtcvad

from config import CONFIG


class LocalWebRTCVADProvider:
    def __init__(self) -> None:
        self.sample_rate = CONFIG.audio_sample_rate
        self.channels = CONFIG.audio_channels
        self.frame_duration_ms = CONFIG.audio_frame_duration_ms
        self.frame_size = int(self.sample_rate * self.frame_duration_ms / 1000)

    @staticmethod
    def int16_bytes_to_float32(audio_bytes: bytes) -> np.ndarray:
        audio_int16 = np.frombuffer(audio_bytes, dtype=np.int16)
        return audio_int16.astype(np.float32) / 32768.0

    def record_utterance(self) -> Optional[np.ndarray]:
        vad = webrtcvad.Vad(CONFIG.vad_aggressiveness)
        audio_queue: queue.Queue[bytes] = queue.Queue()

        triggered = False
        voiced_frames = []
        ring_buffer = collections.deque(maxlen=CONFIG.vad_start_trigger_frames)
        silence_counter = 0

        def callback(indata, frames, time, status):
            if status:
                print(f"⚠️ Audio status: {status}")
            audio_queue.put(bytes(indata))

        print("🎤 En attente de parole...")

        with sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=self.frame_size,
            dtype="int16",
            channels=self.channels,
            callback=callback,
        ):
            max_total_frames = int((CONFIG.vad_max_record_seconds * 1000) / self.frame_duration_ms)
            total_frames = 0

            while total_frames < max_total_frames:
                frame = audio_queue.get()
                is_speech = vad.is_speech(frame, self.sample_rate)
                total_frames += 1

                if not triggered:
                    ring_buffer.append((frame, is_speech))
                    num_voiced = len([f for f, speech in ring_buffer if speech])

                    if num_voiced >= CONFIG.vad_start_trigger_frames:
                        triggered = True
                        print("🟢 Parole détectée, enregistrement...")
                        for f, _ in ring_buffer:
                            voiced_frames.append(f)
                        ring_buffer.clear()
                else:
                    voiced_frames.append(frame)

                    if is_speech:
                        silence_counter = 0
                    else:
                        silence_counter += 1

                    if silence_counter >= CONFIG.vad_end_trigger_frames:
                        print("🔴 Fin de parole détectée.")
                        break

        if not voiced_frames:
            return None

        audio_bytes = b"".join(voiced_frames)
        return self.int16_bytes_to_float32(audio_bytes)