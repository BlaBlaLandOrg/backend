from pydantic import BaseModel


class CharacterSchema(BaseModel):
    name: str