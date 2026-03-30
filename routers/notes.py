from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas.note import NoteCreate, NoteUpdate, NoteResponse, DeleteResponse
from storage.notes import notes_store

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteCreate):
    return notes_store.create(note.title, note.content)

@router.get("/", response_model=List[NoteResponse])
async def get_all_notes():
    return notes_store.get_all()

@router.get("/{note_id}", response_model=NoteResponse)
async def get_note_by_id(note_id: int):
   
    note = notes_store.get_by_id(note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found"
        )
    return note

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(note_id: int, note_update: NoteUpdate):
    
    updated_note = notes_store.update(
        note_id, 
        note_update.title, 
        note_update.content
    )
    if not updated_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found"
        )
    return updated_note

@router.delete("/{note_id}", response_model=DeleteResponse,status_code=status.HTTP_200_OK)
async def delete_note(note_id: int):
   
    deleted = notes_store.delete(note_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found"
        )
    return DeleteResponse(
        message=f"Note with id {note_id} is deleted",
        success=True,
    )
