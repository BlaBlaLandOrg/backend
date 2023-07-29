from pydantic import BaseModel


class Recording(BaseModel):
    path: str
    model: str
    bytes: str

