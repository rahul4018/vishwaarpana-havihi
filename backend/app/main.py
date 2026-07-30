from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.router import api_router
from app.core.exception_handlers import (
    register_exception_handlers,
)


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Upload directories
UPLOAD_DIR = BASE_DIR / "uploads"
GALLERY_UPLOAD_DIR = UPLOAD_DIR / "gallery"

# Ensure upload directories exist
GALLERY_UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


app = FastAPI(
    title="Vishwaarpana Havihi API",
    description="Backend API for Vishwaarpana Havihi SaaS Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# Register global exception handlers
register_exception_handlers(app)


# CORS (Development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Serve uploaded files
app.mount(
    "/uploads",
    StaticFiles(
        directory=str(UPLOAD_DIR),
    ),
    name="uploads",
)


# API routes
app.include_router(api_router)


@app.get(
    "/",
    tags=["Root"],
)
async def root():
    return {
        "success": True,
        "message": "Welcome to Vishwaarpana Havihi API",
        "version": "1.0.0",
    }


@app.get(
    "/health",
    tags=["Health"],
)
async def health():
    return {
        "status": "healthy",
        "service": "backend",
    }