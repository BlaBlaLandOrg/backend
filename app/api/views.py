from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.api.schemas import CharacterSchema

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