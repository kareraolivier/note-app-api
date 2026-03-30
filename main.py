from fastapi import FastAPI
from routers import notes

app = FastAPI(
    title="NotesApp API",
    description="A simple NotesApp API",
    version="1.0.0"
)


app.include_router(notes.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Notes API!",
        "endpoints": {
            "POST /notes": "Create a new note",
            "GET /notes": "Get all notes",
            "GET /notes/{id}": "Get a specific note",
            "PUT /notes/{id}": "Update a note",
            "DELETE /notes/{id}": "Delete a note"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
