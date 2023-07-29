from elevenlabs import get_api_key
from elevenlabs import voices as elevenlabs_voices
from elevenlabs.api.voice import Voice
from elevenlabs import generate, play, clone
from fastapi import UploadFile
from typing import List
import json
import os
import uuid
import base64
from .models import Recording


class ElevenlabsController:

    def __init__(self):
        self.header = {"xi-api-key": get_api_key()}

    @staticmethod
    def list_voices():
        # pydantic models to json -> json.loads(voices.json())
        voices = elevenlabs_voices()
        t = Voice(voice_id="test")
        return voices.json()

    @staticmethod
    def text_to_speech(text: str, voice_name: str, model: str = "eleven_multilingual_v1"):
        audio = generate(
            text=f"{text}",
            voice=f"{voice_name}",
            model=f"{model}",
            api_key=get_api_key()
        )

        file_id = f"{os.path.abspath(os.getcwd())}/assets/audio/{voice_name}-{uuid.uuid4()}.mp3"

        with open(file_id, 'wb') as f:
            f.write(audio)

        audio_base64 = base64.b64encode(audio).decode()
        return Recording(path=file_id, model=model, bytes=audio_base64).json()

    @staticmethod
    def create_character(name: str, files: List[UploadFile], description: str, labels: List[str]) -> str:
        creation = clone(name, files, description, labels)
        return creation

if __name__ == "__main__":
    e = ElevenlabsController()
    print(e.list_voices())
    # print(e.text_to_speech(text="Hallo ich bin Patrick von Blablaland", voice_name="Rachel"))