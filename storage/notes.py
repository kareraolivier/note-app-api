
import csv
import os
from datetime import date
from typing import List, Optional, Dict, Any

class NotesStorage:
    """CSV-based storage for notes"""
    
    def __init__(self, filename: str = "notes.csv"):
        self.filename = filename
        self._init_csv()
    
    def _init_csv(self):
        """Create CSV file with headers if it doesn't exist"""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['id', 'title', 'content', 'created_at'])
    
    def _read_all(self) -> List[Dict[str, Any]]:
        """Read all notes from CSV"""
        notes = []
        if not os.path.exists(self.filename):
            return notes
        
        with open(self.filename, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                notes.append({
                    'id': int(row['id']),
                    'title': row['title'],
                    'content': row['content'],
                    'created_at': row['created_at']
                })
        return notes
    
    def _write_all(self, notes: List[Dict[str, Any]]):
        """Write all notes to CSV"""
        with open(self.filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'title', 'content', 'created_at'])
            writer.writeheader()
            writer.writerows(notes)
    
    def _next_id(self) -> int:
        """Get next available ID"""
        notes = self._read_all()
        if not notes:
            return 1
        return max(n['id'] for n in notes) + 1
    
    def create(self, title: str, content: str) -> Dict[str, Any]:
        """Create a new note"""
        notes = self._read_all()
        new_id = self._next_id()
        
        new_note = {
            'id': new_id,
            'title': title,
            'content': content,
            'created_at': date.today().isoformat()
        }
        
        notes.append(new_note)
        self._write_all(notes)
        return new_note
    
    def get_all(self, title_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all notes with optional title filter"""
        notes = self._read_all()
        
        if title_filter:
            filtered = []
            for note in notes:
                if title_filter.lower() in note['title'].lower():
                    filtered.append(note)
            return filtered
        
        return notes
    
    def get_by_id(self, note_id: int) -> Optional[Dict[str, Any]]:
        """Get a single note by ID"""
        notes = self._read_all()
        for note in notes:
            if note['id'] == note_id:
                return note
        return None
    
    def update(self, note_id: int, title: Optional[str] = None, content: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Update a note"""
        notes = self._read_all()
        
        for i, note in enumerate(notes):
            if note['id'] == note_id:
                if title:
                    notes[i]['title'] = title
                if content:
                    notes[i]['content'] = content
                
                self._write_all(notes)
                return notes[i]
        
        return None
    
    def delete(self, note_id: int) -> bool:
        """Delete a note"""
        notes = self._read_all()
        
        for i, note in enumerate(notes):
            if note['id'] == note_id:
                del notes[i]
                self._write_all(notes)
                return True
        
        return False
    
    def get_paginated(self, page: int = 1, limit: int = 10, title_filter: Optional[str] = None) -> dict:
        """Get paginated notes"""
        all_notes = self.get_all(title_filter)
        total = len(all_notes)
        total_pages = (total + limit - 1) // limit if total > 0 else 1
        page = max(1, min(page, total_pages))
        
        start = (page - 1) * limit
        end = start + limit
        paginated = all_notes[start:end]
        
        return {
            "total": total,
            "page": page,
            "limit": limit,
            "total_pages": total_pages,
            "data": paginated
        }
