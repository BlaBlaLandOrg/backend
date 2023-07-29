from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.api.schemas import CharacterSchema

router = APIRouter()

@router.get("/list-all", response_model=List[CharacterSchema])
async def read_all_functionalities():
    # DB Call
    return