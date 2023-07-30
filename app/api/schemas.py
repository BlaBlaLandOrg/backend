from pydantic import BaseModel
from fastapi import UploadFile
from typing import List


### Elevenlabs
class VoiceSchema(BaseModel):
    name: str

class CreateVoiceSchema(BaseModel):
    name: str
    description: str
    labels: List[str]

class TextToSpeechSchema(BaseModel):
    text: str
    voice_name: str
    model: str = "eleven_multilingual_v1"
    lip_sync: bool = False


### Whisper
class TranscribeAudioSchema(BaseModel):
    audio_file: UploadFile


### Internal
class CharacterSchema(BaseModel):
    id: str
    name: str
    avatar_url: str
    description: str
    labels: List[str]
    rating: int
    voice_schema: VoiceSchema