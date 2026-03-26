 
from fastapi import APIRouter, HTTPException
router = APIRouter()

@router.get("/")
async def read_notes():
    return {"message": "This endpoint will return all notes."}

@router.post("/")
async def create_note():
    return {"message": "Note created successfully"}

