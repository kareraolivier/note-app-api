from datetime import date
from pydantic import BaseModel, Field
from typing import Optional, List

class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=5000)

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1, max_length=5000)

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: str
    
    class Config:
        from_attributes = True

class DeleteResponse(BaseModel):
    message: str
    success: bool
    deleted_note_id: int

class PaginatedResponse(BaseModel):
    total: int
    page: int
    limit: int
    total_pages: int
    data: List[NoteResponse]
