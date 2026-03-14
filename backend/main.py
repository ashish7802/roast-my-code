import os

import anthropic
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from auth import auth_router, get_current_user
from database import Base, engine
from models import User

load_dotenv()

app = FastAPI(title="Roast My Code API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
SYSTEM_PROMPT = (
    "You are a savage but funny code reviewer. Roast the user's code brutally but also give 2-3 real "
    "improvement tips at the end. Keep it under 200 words. End with a score like 'Code Quality: X/10' "
    "with a matching emoji."
)


class RoastRequest(BaseModel):
    code: str = Field(min_length=1)
    intensity: str = Field(min_length=1)


class RoastResponse(BaseModel):
    roast: str
    score: str


def extract_score(text: str) -> str:
    import re

    match = re.search(r"Code\s*Quality\s*:\s*(\d{1,2})\s*/\s*10\s*([^\n]*)?", text, flags=re.IGNORECASE)
    if not match:
        return "Code Quality: ???/10 🤷"
    value = max(0, min(10, int(match.group(1))))
    tail = (match.group(2) or "").strip()
    return f"Code Quality: {value}/10{(' ' + tail) if tail else ''}"


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/roast", response_model=RoastResponse)
def roast(payload: RoastRequest, _: User = Depends(get_current_user)):
    if payload.intensity not in {"Gentle", "Medium", "Savage"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid intensity")

    if not ANTHROPIC_API_KEY:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Anthropic API key not configured")

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=350,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"Intensity: {payload.intensity}\n\nCode:\n{payload.code}",
                }
            ],
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Anthropic API error: {exc}") from exc

    roast_text = ""
    if getattr(message, "content", None):
        roast_text = (getattr(message.content[0], "text", "") or "").strip()

    if not roast_text:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="No roast content returned by Anthropic")

    return RoastResponse(roast=roast_text, score=extract_score(roast_text))
