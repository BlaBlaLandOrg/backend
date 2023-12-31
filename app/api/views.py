from fastapi import UploadFile, APIRouter, Depends, HTTPException, Response, Request, File, Form
from starlette.responses import FileResponse
from typing import List, Dict
from sqlalchemy.orm import Session
from app.api.schemas import VoiceSchema, TextToSpeechSchema, CreateVoiceSchema, CharacterSchema, TranscribeAudioSchema
from app.api.core.whisperapi_controller import WhisperController
from app.api.core.elevenlabs_controller import ElevenlabsController
from app.api.core.openai_controller import OpenaiController
from app.api.core.stablediffusion_controller import generate_avatar
from app.api.core.models import Recording, Transcription, Message
from app.database.controller import SessionLocal, engine
from fastapi.responses import StreamingResponse
import base64
import requests
import os
import imghdr
from typing_extensions import Annotated

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def read_image_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

### Elevenlabs API
@router.get("/list-all-voices", response_model=List[VoiceSchema])
async def read_all_voices():
    voices = ElevenlabsController().list_voices()
    voices = [VoiceSchema(name=voice.name) for voice in voices]
    return voices


@router.post("/list-voice-by-name/{name}")
async def read_voice_by_name(name: str):
    voices = ElevenlabsController().list_voices()
    voice_by_name = [voice for voice in voices if voice.name == name]
    return voice_by_name

@router.post("/create-character")
async def create_character(
    files: Annotated[List[UploadFile], File()],
    name: str, description: str,
    db: Session = Depends(get_db)
):
    from ..database.models import Character, Voice

    def read_image_from_url(url):
        response = requests.get(url)
        response.raise_for_status()
        return response.content


    file_paths = []
    for file in files:
        file_id = f"{os.path.abspath(os.getcwd())}/app/api/core/assets/audio/{file.filename}.mp3"
        file_paths.append(file_id)
        with open(file_id, 'wb') as f:
            f.write(file.file.read())
            f.close()

    character_id = ElevenlabsController().create_character(name=name, file_list=file_paths,
                                                           description=description)
    print(character_id)
    voices = ElevenlabsController().list_voices()
    print(voices)
    voice_by_name = [voice for voice in voices if voice.voice_id == character_id["voice_id"]]
    voice_by_name = voice_by_name[0]
    voice = Voice(name=voice_by_name.name, id=voice_by_name.voice_id)
    db.add(voice)
    db.commit()
    avatar_url = generate_avatar(description)
    avatar_data = read_image_from_url(avatar_url)
    character = Character(name=name, description=description, voice_id=character_id["voice_id"],
                          avatar_data=avatar_data, rating=0, rating_count=0)
    # highest id + 1
    ids = db.query(Character).all()
    ids = max([id.id for id in ids])
    character.id = ids + 1
    db.add(character)
    db.commit()

    return character_id

@router.post("/text-to-speech")
async def text_to_speech(text: TextToSpeechSchema) -> Recording:
    # DB Call
    return ElevenlabsController().text_to_speech(text=text.text, voice_name=text.voice_name, model=text.model,
                                                 lip_sync=text.lip_sync)


### Whisper API
@router.post("/transcribe-audio")
async def speech_to_text(request: Request, audio_file: UploadFile) -> Transcription:
    # DB Call
    contents = audio_file.file
    transcript = WhisperController().whisper_to_text_bytes(file=contents)
    return transcript


### OpenAI API
@router.post("/generate-text")
async def generate_text(messages: List[Message]) -> Dict[str, str]:
    # DB Call
    return OpenaiController(messages).answer()[0]


### Internal
@router.get("/list-all-character", response_model=List[CharacterSchema])
def read_all_characters(db: Session = Depends(get_db)):
    from app.database.models import Character
    character = db.query(Character).all()

    characters_in_schema = []
    for i in character:
        character = CharacterSchema(id=i.id, name=i.name, avatar_url=f"/api/get-image/{i.id}", description=i.description, labels=["Default"], rating=i.rating, voice_schema=VoiceSchema(name=i.voice.name))
        characters_in_schema.append(character)

    return characters_in_schema


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

@router.get("/get-recording")
async def get_recording(id: str):
    audio_path = f"{os.path.abspath(os.getcwd())}/app/api/core/assets/audio/{id}.mp3"
    try:
        file = open(audio_path, "rb").read()
        return StreamingResponse(content=file, media_type="audio/mp3")
        # return FileResponse(audio_path, media_type=f"audio/mp3")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while processing the audio file.")

@router.get("/get-recording2")
async def get_recording(id: str):
    audio_path = f"{os.path.abspath(os.getcwd())}/app/api/core/assets/audio/{id}.mp3"
    try:
        return FileResponse(audio_path, media_type=f"audio/mp3")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while processing the audio file.")

@router.post("/character-update-rating/{id}")
def update_character_rating(id: str, rating: int, db: Session = Depends(get_db)):
    from app.database.models import Character
    character = db.query(Character).filter(Character.id == id).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")

    rating_character = character.rating
    try:
        rating_count = character.rating_count
        if rating_count is None:
            rating_count = 0
    except:
        rating_count = 0


    new_rating = (rating_character * rating_count + rating) / (rating_count + 1)
    character.rating = new_rating
    db.commit()
    return {"message": "Rating updated", "new_rating": new_rating}


### Internal Mock
@router.get("/character-mock")
def characters_mock(db: Session = Depends(get_db)):
    from app.database.models import Character, Voice


    # create voices with working voices of elevenlabs -> mapping
    bob = Voice(id=1, name='Sam')
    alice = Voice(id=2, name='Elli')
    eve = Voice(id=3, name='Rachel')
    benjamin = Voice(id=4, name='Arnold')
    surferboy = Voice(id=5, name='Dave')

    db.add(bob)
    db.add(alice)
    db.add(eve)
    db.add(benjamin)
    db.add(surferboy)

    db.flush()

    # create characters
    char1 = Character(name='Blablaland-Monster', avatar_data=read_image_file(f"{os.path.abspath(os.getcwd())}/app/api/core/assets/img/78d7f0d9-39a9-48a4-97aa-20d9c8341cc7.jpg"), description='The perfect monster for children',
                       rating=5, voice_id=bob.id, rating_count=1)
    char2 = Character(name='Grandmother', avatar_data=read_image_file(f"{os.path.abspath(os.getcwd())}/app/api/core/assets/img/77c3274b-c2d5-40b3-adb1-7578dd1fa8cd.jpg"), description='The perfect grandmother',
                       rating=4, voice_id=alice.id, rating_count=1)
    char3 = Character(name='Surferboy', avatar_data=read_image_file(f"{os.path.abspath(os.getcwd())}/app/api/core/assets/img/5c771a9e-2293-4315-be9b-866a381f07fe.jpg"), description='A sexy Surferboy from the Beach',
                      rating=5, voice_id=surferboy.id, rating_count=1)
    char4 = Character(name='Morgan Freeman', avatar_data=read_image_file(f"{os.path.abspath(os.getcwd())}/app/api/core/assets/img/461b3391-d377-4bdd-a9f1-4f066e31c264.jpg"), description='The legend Morgan Freeman himself',
                      rating=4, voice_id=bob.id, rating_count=1)
    char5 = Character(name='Benjamin', avatar_data=read_image_file(f"{os.path.abspath(os.getcwd())}/app/api/core/assets/img/002340e1-f4d7-400d-bc33-000f1a28dcb9.jpg"), description='Lets talk sports',
                      rating=5, voice_id=benjamin.id, rating_count=1)
    char6 = Character(name='Isabella', avatar_data=read_image_file(f"{os.path.abspath(os.getcwd())}/app/api/core/assets/img/e684172f-f5fe-444f-a25d-488c0bc43bc6.jpg"), description='Have a conversation about your favorite book',
                        rating=5, voice_id=alice.id, rating_count=1)
    db.add(char1)
    db.add(char2)
    db.add(char3)
    db.add(char4)
    db.add(char5)
    db.add(char6)


    # commit the transaction
    db.commit()




