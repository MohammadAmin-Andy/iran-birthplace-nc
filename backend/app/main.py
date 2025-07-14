# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import birthplace

app = FastAPI(
    title="Iran Birthplace National Code API",
    version="1.0.0",
    description="An open-source API to validate Iranian national codes based on birthplace codes.",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Iran Birthplace NC API is running.",
        "documentation": "For documentation, visit /docs."
    }

app.include_router(
    birthplace.router,
    prefix="/api/birthplace",
    tags=["Birthplace Validation"]
)