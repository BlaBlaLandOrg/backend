import os
import openai
import tempfile
from .models import Transcription

class WhisperController:
    """
    supports [".m4a", ".mp3", ".mp4", ".mpeg", ".mpga", ".wav", ".webm"]
    """
    def __init__(self, api_key: str = None):
        self.openai_api_key = os.getenv("OPENAI_API_KEY") if not api_key else api_key

    def whisper_to_text_file(self, filename: str):
        openai.api_key = self.openai_api_key
        audio_file = open(f"{os.path.abspath(os.getcwd())}/{filename}", "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        print(transcript)

    def whisper_to_text_bytes(self, file: bytes):
        with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
            content = file.read()
            tmp_file.write(content)
            tmp_file.flush()
            tmp_file.close()

            with open(tmp_file.name, "rb") as audio_file:
                openai.api_key = self.openai_api_key
                transcript = Transcription(transcript=openai.Audio.transcribe("whisper-1", audio_file))
                return transcript



if __name__ == "__main__":
    w = WhisperController()
    w.whisper_to_text(filename="assets/audio/Rachel-3cf28684-8470-4277-b94e-a4f2645f74ad.mp3")