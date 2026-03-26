from datetime import date
from pydantic import BaseModel
from typing import Optional

class NoteCreate(BaseModel):
   
    title: str
    content: str

class NoteUpdate(BaseModel):
   
    title: Optional[str] = None
    content: Optional[str] = None

class NoteResponse(BaseModel):
  
    id: int
    title: str
    content: str
    created_at: date
    
    class Config:
        from_attributes = True

class DeleteResponse(BaseModel):
    message: str
    success: bool