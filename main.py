
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import notes

app = FastAPI(
    title="Notes API",
    description="A simple Notes API with CSV storage",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(notes.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Notes API!",
    
 
        }
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
