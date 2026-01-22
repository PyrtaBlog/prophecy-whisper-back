# app/api/v1/transcribe.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import re
from app.external.transcript import get_transcript_text

router = APIRouter()

class TranscribeRequest(BaseModel):
    url: str

def extract_video_id(url: str) -> str:
    match = re.search(r"(?:v=|\/)([a-zA-Z0-9_-]{11})", url)
    if not match:
        raise ValueError("Invalid YouTube video URL")
    return match.group(1)

@router.post("/")
def transcribe(request: TranscribeRequest):
    try:
        video_id = extract_video_id(request.url)
        transcript = get_transcript_text(video_id)
        return {
            "video_id": video_id,
            "transcript": transcript
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch transcript")