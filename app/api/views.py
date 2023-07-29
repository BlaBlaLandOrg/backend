from fastapi import UploadFile, APIRouter, Depends, HTTPException, Response
from typing import List, Dict
from sqlalchemy.orm import Session
from app.api.schemas import VoiceSchema, TextToSpeechSchema, CreateVoiceSchema, CharacterSchema, TranscribeAudioSchema
from app.api.core.whisperapi_controller import WhisperController
from app.api.core.elevenlabs_controller import ElevenlabsController
from app.api.core.openai_controller import OpenaiController
from app.api.core.models import Recording, Transcription, Message
from app.database.controller import SessionLocal, engine
import base64
import os
import imghdr


router = APIRouter()

# mock data
characters_db = [
    {"name": "Alice", "rating": 10},
    {"name": "Bob", "rating": 8},
    {"name": "Charlie", "rating": 9},
]

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

### Elevenlabs API
@router.get("/list-all-voices", response_model=List[VoiceSchema])
async def read_all_functionalities():
    # DB Call
    return characters_db


@router.get("/list-character-by-name/{name}", response_model=VoiceSchema)
async def read_character_by_name(name: str):
    # DB Call
    return characters_db[0]
    raise HTTPException(status_code=404, detail="Character not found")


@router.post("/create-character")
async def create_character(files: List[UploadFile], character: CreateVoiceSchema) -> str:
    # DB CALL
    _files = [await file.read() for file in files]
    character_id = ElevenlabsController().create_character(name=character.name, files=_files,
                                                           description=character.description, labels=character.labels)
    return character_id

@router.post("/text-to-speech", response_model=Recording)
async def text_to_speech(text: TextToSpeechSchema) -> Recording:
    # DB Call
    return ElevenlabsController().text_to_speech(text=text.text, voice_name=text.voice_name, model=text.model)


### Whisper API
@router.post("/transcribe-audio")
async def speech_to_text(audio_file: UploadFile) -> Transcription:
    # DB Call
    contents = await audio_file.file.read()
    transcript = WhisperController().whisper_to_text_bytes(file=contents)
    return transcript


### OpenAI API
@router.post("/generate-text")
async def generate_text(messages: List[Message]) -> str:
    # DB Call
    return OpenaiController().answer(messages)


### Internal
@router.get("/list-all-character", response_model=List[CharacterSchema])
def read_all_characters(db: Session = Depends(get_db)):
    # DB Call
    return characters_db


@router.get("/get-image/{id}")
def get_image(id: str, db: Session = Depends(get_db)):
    from app.database.models import Character
    character = db.query(Character).filter(Character.id == id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    img_type = imghdr.what(None, h=character.avatar_data)
    if not img_type:
        raise HTTPException(status_code=500, detail="Could not determine image type")

    image_data = base64.b64encode(character.avatar_data).decode("utf-8")
    return Response(content=base64.b64decode(image_data), media_type=f"image/{img_type}")


### Internal Mock
@router.get("/character-mock")
def characters_mock(db: Session = Depends(get_db)):
    from app.database.models import Character, Voice

    def read_image_file(file_path):
        with open(file_path, 'rb') as file:
            return file.read()


    # create voices
    bob = Voice(name='Bob')
    alice = Voice(name='Alice')
    eve = Voice(name='Eve')

    db.add(bob)
    db.add(alice)
    db.add(eve)

    db.flush()

    # create characters
    char1 = Character(name='Char1', avatar_data=read_image_file(f"{os.path.abspath(os.getcwd())}/app/api/core/assets/img/nisonco-pr-and-seo-yIRdUr6hIvQ-unsplash.jpg"), description='The first character',
                      labels='hero, male', rating=5, voice_id=bob.id)
    char2 = Character(name='Char2', avatar_data=read_image_file(f"{os.path.abspath(os.getcwd())}/app/api/core/assets/img/nisonco-pr-and-seo-yIRdUr6hIvQ-unsplash.jpg"), description='The second character',
                      labels='villain, female', rating=4, voice_id=alice.id)
    char3 = Character(name='Char3', avatar_data=read_image_file(f"{os.path.abspath(os.getcwd())}/app/api/core/assets/img/nisonco-pr-and-seo-yIRdUr6hIvQ-unsplash.jpg"), description='The third character',
                      labels='sidekick, female', rating=5, voice_id=eve.id)
    char4 = Character(name='Char4', avatar_data=read_image_file(f"{os.path.abspath(os.getcwd())}/app/api/core/assets/img/nisonco-pr-and-seo-yIRdUr6hIvQ-unsplash.jpg"), description='The fourth character',
                      labels='hero, male', rating=4, voice_id=bob.id)

    db.add(char1)
    db.add(char2)
    db.add(char3)
    db.add(char4)


    # commit the transaction
    db.commit()




