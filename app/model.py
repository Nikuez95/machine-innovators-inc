# Per prima cosa, ho installato la libreria transformers:
from transformers import pipeline

# Ho creato una pipeline di classificazione del testo utilizzando un modello pre-addestrato per l'analisi del sentiment.
pipe = pipeline(
    "text-classification", model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)


# Funzione per ottenere il sentiment di un testo dato
def get_sentiment(text: str):
    result = pipe(text)
    return result
