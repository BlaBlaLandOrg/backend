from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
import tempfile
from app.api.schemas import CharacterSchema, TextToSpeechSchema, CreateCharacterSchema
from app.api.core.whisperapi_controller import WhisperController
from app.api.core.elevenlabs_controller import ElevenlabsController
from app.api.core.openai_controller import OpenaiController
from app.api.core.models import Recording, Transcription, Message

router = APIRouter()

# mock data
characters_db = [
    {"name": "Alice", "rating": 10},
    {"name": "Bob", "rating": 8},
    {"name": "Charlie", "rating": 9},
]


### Elevenlabs API
@router.get("/list-all-characters", response_model=List[CharacterSchema])
async def read_all_functionalities():
    # DB Call
    return characters_db


@router.get("/list-character-by-name/{name}", response_model=CharacterSchema)
async def read_character_by_name(name: str):
    # DB Call
    return characters_db[0]
    raise HTTPException(status_code=404, detail="Character not found")


@router.post("/create-character")
async def create_character(character: CreateCharacterSchema) -> str:
    # DB CALL
    files = [await file.read() for file in character.files]
    character_id = ElevenlabsController().create_character(name=character.name, files=files,
                                                           description=character.description, labels=character.labels)
    return character_id

@router.post("/text-to-speech", response_model=Recording)
async def text_to_speech(text: TextToSpeechSchema) -> Recording:
    # DB Call
    return ElevenlabsController().text_to_speech(text=text.text, voice_name=text.voice_name, model=text.model)


### Whisper API
@router.post("/transcribe-audio")
async def speech_to_text(audio_file: TextToSpeechSchema) -> Transcription:
    # DB Call
    contents = await audio_file.audio_file.read()
    transcript = WhisperController().whisper_to_text_bytes(file=contents)
    return transcript


### OpenAI API
@router.post("/generate-text")
async def generate_text(messages: List[Message]) -> str:
    # DB Call
    return OpenaiController().answer(messages)

