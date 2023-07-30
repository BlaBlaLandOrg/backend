from pydantic import BaseModel
from typing import Optional, Any


class Recording(BaseModel):
    path: str
    model: str
    bytes: str
    lipsync: Any


class Transcription(BaseModel):
    text: str


class Message(BaseModel):
    role: str
    content: str