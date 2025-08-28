#!/usr/bin/env python3
"""
TxVoc Backend API
FastAPI backend for text-to-speech synthesis with voice cloning
"""

import os
import asyncio
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import tempfile
import json
import shutil

from fastapi import FastAPI, UploadFile, File, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="TxVoc API",
    description="Text-to-Speech API with Voice Cloning",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",  # Alternative port
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# === DATA MODELS ===

class Voice(BaseModel):
    """Voice model for API responses"""
    id: str = Field(..., description="Unique voice identifier")
    name: str = Field(..., description="Display name for the voice")
    description: str = Field(..., description="Description of the voice")
    language: str = Field(default="en", description="Language code")
    created_at: str = Field(..., description="Creation timestamp")
    file_path: Optional[str] = Field(None, description="Path to voice file")
    duration: Optional[float] = Field(None, description="Audio duration in seconds")
    sample_rate: Optional[int] = Field(None, description="Audio sample rate")

class VoiceCreate(BaseModel):
    """Model for creating new voices"""
    name: str = Field(..., min_length=1, max_length=100, description="Voice name")
    description: str = Field(default="", max_length=500, description="Voice description")
    language: str = Field(default="en", description="Language code")

class SynthesisRequest(BaseModel):
    """Request model for speech synthesis"""
    text: str = Field(..., min_length=1, max_length=5000, description="Text to synthesize")
    voice_id: str = Field(..., description="Voice ID to use for synthesis")
    speed: float = Field(default=1.0, ge=0.5, le=2.0, description="Speech speed multiplier")
    pitch: float = Field(default=1.0, ge=0.5, le=2.0, description="Pitch adjustment")

class SynthesisResponse(BaseModel):
    """Response model for speech synthesis"""
    id: str = Field(..., description="Synthesis job ID")
    audio_url: str = Field(..., description="URL to download the audio")
    duration: Optional[float] = Field(None, description="Audio duration in seconds")
    voice_id: str = Field(..., description="Voice ID used")
    text: str = Field(..., description="Synthesized text")
    created_at: str = Field(..., description="Creation timestamp")

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")

# === GLOBAL VARIABLES ===

# In-memory storage (in production, use a proper database)
voices_db: Dict[str, Voice] = {}
synthesis_cache: Dict[str, SynthesisResponse] = {}

# File storage paths
BASE_DIR = Path(__file__).parent
VOICES_DIR = BASE_DIR / "storage" / "voices"
AUDIO_DIR = BASE_DIR / "storage" / "audio"
TEMP_DIR = BASE_DIR / "storage" / "temp"

# Ensure directories exist
for directory in [VOICES_DIR, AUDIO_DIR, TEMP_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# === UTILITY FUNCTIONS ===

def get_audio_duration(file_path: Path) -> Optional[float]:
    """Get audio file duration (placeholder implementation)"""
    try:
        # In a real implementation, use librosa or ffprobe
        return 10.0  # Placeholder duration
    except Exception as e:
        logger.warning(f"Could not get duration for {file_path}: {e}")
        return None

def validate_audio_file(file: UploadFile) -> bool:
    """Validate uploaded audio file"""
    if not file.content_type:
        return False

    valid_types = ["audio/wav", "audio/mpeg", "audio/mp3", "audio/ogg", "audio/flac"]
    return file.content_type in valid_types

def generate_synthesis_audio(text: str, voice_id: str, speed: float, pitch: float) -> Path:
    """Generate speech audio (placeholder implementation)"""
    # In a real implementation, this would use TTS engines like Coqui TTS

    # Create a simple text file as placeholder
    synthesis_id = str(uuid.uuid4())
    output_file = AUDIO_DIR / f"synthesis_{synthesis_id}.txt"

    content = f"""TxVoc Speech Synthesis
=====================
ID: {synthesis_id}
Text: {text}
Voice: {voice_id}
Speed: {speed}x
Pitch: {pitch}x
Generated: {datetime.now().isoformat()}

This is a placeholder file. In a real implementation,
this would be an actual audio file generated using
text-to-speech synthesis with the specified voice.
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    return output_file

# === API ENDPOINTS ===

@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information"""
    return {
        "service": "TxVoc API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "voices": "/voices - Manage voices",
            "synthesis": "/synthesize - Generate speech",
            "docs": "/docs - API documentation",
            "health": "/health - Health check"
        },
        "frontend_url": "http://localhost:3000"
    }

@app.get("/health", response_model=dict)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "voice_count": len(voices_db),
        "synthesis_count": len(synthesis_cache)
    }

# === VOICE MANAGEMENT ENDPOINTS ===

@app.get("/voices", response_model=List[Voice])
async def get_voices():
    """Get all available voices"""
    logger.info("Fetching all voices")
    return list(voices_db.values())

@app.get("/voices/{voice_id}", response_model=Voice)
async def get_voice(voice_id: str):
    """Get a specific voice by ID"""
    if voice_id not in voices_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Voice with ID '{voice_id}' not found"
        )

    return voices_db[voice_id]

@app.post("/voices", response_model=Voice, status_code=status.HTTP_201_CREATED)
async def upload_voice(
    file: UploadFile = File(...),
    name: str = "Custom Voice",
    description: str = "",
    language: str = "en"
):
    """Upload a new voice file"""
    try:
        # Validate file
        if not validate_audio_file(file):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid audio file. Supported formats: WAV, MP3, OGG, FLAC"
            )

        # Generate unique voice ID
        voice_id = str(uuid.uuid4())

        # Determine file extension
        original_filename = file.filename or "audio.wav"
        file_extension = Path(original_filename).suffix.lower()
        if not file_extension:
            file_extension = ".wav"

        # Save uploaded file
        voice_file_path = VOICES_DIR / f"{voice_id}{file_extension}"

        with open(voice_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Get audio properties
        duration = get_audio_duration(voice_file_path)

        # Create voice entry
        voice = Voice(
            id=voice_id,
            name=name,
            description=description,
            language=language,
            created_at=datetime.now().isoformat(),
            file_path=str(voice_file_path),
            duration=duration,
            sample_rate=22050  # Default sample rate
        )

        # Store in database
        voices_db[voice_id] = voice

        logger.info(f"Voice uploaded successfully: {voice_id} - {name}")
        return voice

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading voice: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload voice: {str(e)}"
        )

@app.delete("/voices/{voice_id}", response_model=dict)
async def delete_voice(voice_id: str):
    """Delete a voice"""
    if voice_id not in voices_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Voice with ID '{voice_id}' not found"
        )

    try:
        # Get voice info
        voice = voices_db[voice_id]

        # Remove file if exists
        if voice.file_path:
            file_path = Path(voice.file_path)
            if file_path.exists():
                file_path.unlink()

        # Remove from database
        del voices_db[voice_id]

        logger.info(f"Voice deleted successfully: {voice_id}")
        return {"message": f"Voice '{voice.name}' deleted successfully"}

    except Exception as e:
        logger.error(f"Error deleting voice: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete voice: {str(e)}"
        )

# === SPEECH SYNTHESIS ENDPOINTS ===

@app.post("/synthesize", response_model=SynthesisResponse, status_code=status.HTTP_201_CREATED)
async def synthesize_speech(request: SynthesisRequest):
    """Synthesize speech from text using specified voice"""
    try:
        # Validate voice exists
        if request.voice_id not in voices_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Voice with ID '{request.voice_id}' not found"
            )

        # Generate speech audio
        audio_file = generate_synthesis_audio(
            text=request.text,
            voice_id=request.voice_id,
            speed=request.speed,
            pitch=request.pitch
        )

        # Create synthesis response
        synthesis_id = str(uuid.uuid4())
        synthesis_response = SynthesisResponse(
            id=synthesis_id,
            audio_url=f"/audio/{audio_file.name}",
            duration=len(request.text) * 0.1,  # Rough estimate: 0.1s per character
            voice_id=request.voice_id,
            text=request.text,
            created_at=datetime.now().isoformat()
        )

        # Cache the response
        synthesis_cache[synthesis_id] = synthesis_response

        logger.info(f"Speech synthesized successfully: {synthesis_id}")
        return synthesis_response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error synthesizing speech: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to synthesize speech: {str(e)}"
        )

@app.get("/synthesis/{synthesis_id}", response_model=SynthesisResponse)
async def get_synthesis(synthesis_id: str):
    """Get synthesis information by ID"""
    if synthesis_id not in synthesis_cache:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Synthesis with ID '{synthesis_id}' not found"
        )

    return synthesis_cache[synthesis_id]

@app.get("/synthesis", response_model=List[SynthesisResponse])
async def get_all_synthesis():
    """Get all synthesis jobs"""
    return list(synthesis_cache.values())

# === AUDIO FILE SERVING ===

@app.get("/audio/{filename}")
async def serve_audio(filename: str):
    """Serve audio files"""
    try:
        # Check in audio directory
        file_path = AUDIO_DIR / filename

        if not file_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Audio file not found"
            )

        # Determine media type based on extension
        extension = file_path.suffix.lower()
        media_types = {
            '.wav': 'audio/wav',
            '.mp3': 'audio/mpeg',
            '.ogg': 'audio/ogg',
            '.flac': 'audio/flac',
            '.txt': 'text/plain'  # For placeholder files
        }

        media_type = media_types.get(extension, 'application/octet-stream')

        return FileResponse(
            path=file_path,
            media_type=media_type,
            filename=filename
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving audio file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to serve audio file: {str(e)}"
        )

# === INITIALIZATION ===

@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    logger.info("Starting TxVoc API server...")

    # Create a default voice for testing
    default_voice = Voice(
        id="default",
        name="Default Voice",
        description="Built-in default voice for testing",
        language="en",
        created_at=datetime.now().isoformat(),
        file_path=None,
        duration=None,
        sample_rate=22050
    )
    voices_db["default"] = default_voice

    logger.info(f"TxVoc API server initialized with {len(voices_db)} voices")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down TxVoc API server...")

# === ERROR HANDLERS ===

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

# === MAIN ===

if __name__ == "__main__":
    logger.info("Starting TxVoc API server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["./"],
        log_level="info"
    )
