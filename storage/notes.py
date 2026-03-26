from datetime import date
from typing import Dict, Optional
from schemas.note import NoteResponse

class NotesStore:
    def __init__(self):
        self._notes: Dict[int, dict] = {}
        self._current_id = 1
    
    def create(self, title: str, content: str) -> NoteResponse:
      
        note = {
            "id": self._current_id,
            "title": title,
            "content": content,
            "created_at": date.today()
        }
        self._notes[self._current_id] = note
        self._current_id += 1
        return NoteResponse(**note)
    
    def get_all(self) -> list[NoteResponse]:
        return [NoteResponse(**note) for note in self._notes.values()]
    
    def get_by_id(self, note_id: int) -> Optional[NoteResponse]:
        note = self._notes.get(note_id)
        return NoteResponse(**note) if note else None
    
    def update(self, note_id: int, title: Optional[str] = None, content: Optional[str] = None) -> Optional[NoteResponse]:
        if note_id not in self._notes:
            return None
        
        note = self._notes[note_id]
        if title is not None:
            note["title"] = title
        if content is not None:
            note["content"] = content
        
        return NoteResponse(**note)
    
    def delete(self, note_id: int) -> bool:
       
        if note_id in self._notes:
            del self._notes[note_id]
            return True
        return False

notes_store = NotesStore()
