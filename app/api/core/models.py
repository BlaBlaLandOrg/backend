from pydantic import BaseModel, Json
from typing import Optional, Any, List


class Recording(BaseModel):
    path: str
    model: str
    bytes: str
    lipsync: str


class Transcription(BaseModel):
    text: str


class Message(BaseModel):
    role: str
    content: str