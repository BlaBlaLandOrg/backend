from pydantic import BaseModel, Json
from typing import Optional, Any, List, Dict


class Recording(BaseModel):
    path: str
    model: str
    bytes: str
    lipsync: Json[List[Dict[str, Any]]] = None


class Transcription(BaseModel):
    text: str


class Message(BaseModel):
    role: str
    content: str