from pydantic import BaseModel


class CharacterSchema(BaseModel):
    name: str
    rating: int

class TextToSpeachSchema(BaseModel):
    text: str
    voice_name: str
    model: str = "eleven_multilingual_v1"