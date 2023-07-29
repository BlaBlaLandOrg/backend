from pydantic import BaseModel
from fastapi import UploadFile
from typing import List

class CharacterSchema(BaseModel):
    name: str
    rating: int

class CreateCharacterSchema(BaseModel):
    name: str
    files: List[UploadFile]
    description: str
    labels: List[str]

class TextToSpeachSchema(BaseModel):
    text: str
    voice_name: str
    model: str = "eleven_multilingual_v1"

class TranscribeAudioSchema(BaseModel):
    audio_file: UploadFile