from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import re


app = FastAPI(
    title="Smart Text API",
    description="Analyze and score text with no database",
    version="1.0",
)


# ---------- Pydantic Schema ----------

class TextInput(BaseModel):
    text: str = Field(..., min_length=5, description="Text to analyze")


class TextAnalysis(BaseModel):
    characters: int
    words: int
    sentences: int
    estimated_read_time_min: float
    sentiment: str


# ---------- Utility Logic ----------

POSITIVE_WORDS = {"good", "great", "happy", "success", "love", "excellent"}
NEGATIVE_WORDS = {"bad", "sad", "hate", "failure", "angry", "poor"}


def analyze_text(text: str) -> TextAnalysis:
    words = re.findall(r"\b\w+\b", text.lower())
    sentences = re.split(r"[.!?]+", text)

    positive = sum(1 for w in words if w in POSITIVE_WORDS)
    negative = sum(1 for w in words if w in NEGATIVE_WORDS)

    if positive > negative:
        sentiment = "positive"
    elif negative > positive:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return TextAnalysis(
        characters=len(text),
        words=len(words),
        sentences=len([s for s in sentences if s.strip()]),
        estimated_read_time_min=round(len(words) / 200, 2),
        sentiment=sentiment,
    )


# ---------- API Endpoint ----------

@app.post("/analyze", response_model=TextAnalysis)
def analyze(payload: TextInput):
    return analyze_text(payload.text)
