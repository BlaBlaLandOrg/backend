from pydantic import BaseModel
from fastapi import UploadFile


class CharacterSchema(BaseModel):
    name: str
    rating: int

class TextToSpeachSchema(BaseModel):
    text: str
    voice_name: str
    model: str = "eleven_multilingual_v1"

class TranscribeAudioSchema(BaseModel):
    audio_file: UploadFile
