from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional
from schemas.note import (
    NoteCreate, NoteUpdate, NoteResponse, 
    DeleteResponse, PaginatedResponse
)
from storage.notes import NotesStorage

router = APIRouter(prefix="/notes", tags=["notes"])

# Initialize storage
storage = NotesStorage()

@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteCreate):
    """Create a new note"""
    result = storage.create(note.title, note.content)
    return result

@router.get("/", response_model=PaginatedResponse)
async def get_notes(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    title: Optional[str] = Query(None, description="Filter by title")
):
    """Get all notes with pagination"""
    return storage.get_paginated(page=page, limit=limit, title_filter=title)

@router.get("/all", response_model=list[NoteResponse])
async def get_all_notes():
    """Get all notes without pagination"""
    notes = storage.get_all()
    return notes

@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: int):
    """Get a single note by ID"""
    note = storage.get_by_id(note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found"
        )
    return note

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(note_id: int, note: NoteUpdate):
    """Update a note"""
    updated = storage.update(note_id, note.title, note.content)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found"
        )
    return updated

@router.delete("/{note_id}", response_model=DeleteResponse)
async def delete_note(note_id: int):
    """Delete a note"""
    note = storage.get_by_id(note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found"
        )
    
    storage.delete(note_id)
    return DeleteResponse(
        message=f"Note '{note['title']}' was successfully deleted",
        success=True,
        deleted_note_id=note_id
    )
