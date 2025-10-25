# Ho creato un'API web utilizzando FastAPI che consente agli utenti di inviare testo e ricevere un'analisi del sentiment.
# L'API include una semplice interfaccia HTML per l'inserimento del testo e la visualizzazione dei risultati.

# Importo le librerie necessarie
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from .model import get_sentiment

# Creo l'istanza dell'app FastAPI
app = FastAPI()


# Definisco il modello Pydantic per la richiesta di input
class TextInput(BaseModel):
    text: str


# Definisco la route principale che restituisce una semplice interfaccia HTML
@app.get("/", response_class=HTMLResponse)
def root():
    html_content = """
    <html>
        <head>
            <title>MachineInnovators Inc. API</title>
            <style>
                body { font-family: sans-serif; margin: 2em; background: #f4f4f4; }
                h1 { color: #333; }
                #results { 
                    margin-top: 20px; 
                    padding: 10px; 
                    border: 1px solid #ccc; 
                    background: #fff; 
                    border-radius: 5px; 
                }
            </style>
        </head>
        <body>
            <h1>MachineInnovators Inc. Sentiment API</h1>
            <p>Inserisci il testo da analizzare (Inglese):</p>
            <input type="text" id="text-input" style="width: 300px; padding: 5px;">
            <button onclick="analyzeText()">Analizza</button>
            
            <h3>Risultati:</h3>
            <pre id="results">{ "..." }</pre>

            <script>
                async function analyzeText() {
                    const textInput = document.getElementById('text-input').value;
                    const resultsDiv = document.getElementById('results');
                    
                    if (!textInput) {
                        resultsDiv.innerText = '{ "Errore": "Input vuoto" }';
                        return;
                    }

                    const response = await fetch('/analyze', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ text: textInput }) // Invia il JSON come definito in Pydantic
                    });

                    const data = await response.json();
                    resultsDiv.innerText = JSON.stringify(data, null, 2);
                }
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# Definisco la route per l'analisi del sentiment
@app.post("/analyze")
def analyze_sentiment(data: TextInput):
    sentiment = get_sentiment(data.text)
    return {"input_text": data.text, "sentiment_result": sentiment[0]}
