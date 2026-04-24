import sounddevice as sd
import soundfile as sf


def play_audio_file(file_path: str) -> None:
    data, samplerate = sf.read(file_path)
    sd.play(data, samplerate)
    sd.wait()
