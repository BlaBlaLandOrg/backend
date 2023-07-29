from fastapi import APIRouter, Depends, HTTPException
from typing import List
import tempfile
from app.api.schemas import CharacterSchema, TextToSpeachSchema
from app.api.core.whisperapi_controller import WhisperController
from app.api.core.models import Recording, Transcription

router = APIRouter()


# mock data
characters_db = [
    {"name": "Alice", "rating": 10},
    {"name": "Bob", "rating": 8},
    {"name": "Charlie", "rating": 9},
]

@router.get("/list-all-characters", response_model=List[CharacterSchema])
async def read_all_functionalities():
    # DB Call
    return characters_db

@router.get("/list-character-by-name/{name}", response_model=CharacterSchema)
async def read_character_by_name(name: str):
    # DB Call
    return characters_db[0]
    raise HTTPException(status_code=404, detail="Character not found")

@router.post("/text-to-speach", response_model=Recording)
async def text_to_speach(TexttoSpeach: TextToSpeachSchema):
    # DB Call
    return Recording(path="path", model="model", bytes="bytes")

@router.post("/transcribe-audio")
async def speach_to_text(audio_file: TextToSpeachSchema) -> Transcription:
    # DB Call
    contents = await audio_file.audio_file.read()
    transcript = WhisperController().whisper_to_text_bytes(file=contents)



    return "speach-to-text"