import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from prometheus_fastapi_instrumentator import Instrumentator

from .model import get_sentiment, get_pipe

logger = logging.getLogger(__name__)

app = FastAPI(title="MachineInnovators Inc. API", version="1.0.0")

logging.basicConfig(
    level="INFO",
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

Instrumentator().instrument(app).expose(app)

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


class TextInput(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready():
    try:
        _ = get_pipe()
        return {"ready": True}
    except Exception as e:
        logger.exception("Model not ready")
        return {"ready": False, "error": str(e)}


@app.get("/")
def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_title": "MachineInnovators Inc. Sentiment API",
            "app_version": app.version,
            "description": "Inserisci un testo e ottieni sentiment + score.",
        },
    )


@app.post("/analyze")
def analyze_sentiment(data: TextInput):
    try:
        result = get_sentiment(data.text.strip())
        return {
            "input_text": data.text.strip(),
            "sentiment": result["label"],
            "score": result["score"],
        }
    except Exception:
        logger.exception("Inference failed")
        raise HTTPException(status_code=500, detail="Inference error")
