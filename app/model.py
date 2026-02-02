from functools import lru_cache
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"

@lru_cache(maxsize=1)
def get_pipe():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        low_cpu_mem_usage=False,
    )
    model.eval()
    return pipeline("text-classification", model=model, tokenizer=tokenizer, device=-1)

def get_sentiment(text: str) -> dict:
    out = get_pipe()(text)
    r = out[0]
    return {"label": r["label"], "score": float(r["score"])}
