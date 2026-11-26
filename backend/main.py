from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.game_api import router as game_router

app = FastAPI(title="GeoQuest AI")
app.include_router(game_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "https://sahreen-sajjad.github.io"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Welcome to GeoQuest AI"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}