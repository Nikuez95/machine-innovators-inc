# Progetto MLOps: MachineInnovators Inc.
Questa repository contiene l'implementazione di una pipeline per il progetto "MachineInnovators Inc."
L'obiettivo è stato quello di prendere un modello Sentiment Analysis e costruire un'infrastrutura di produzione monitorabile e scalabile.
L'interno ambiente è gestito tramite docker-compose, permettendo di avviare il tutto con un singolo comando

*docker-compose up -d --build*

# Cosa ho usato
**API & Serving**: Python, FastAPI, Uvicorn
**Modello ML**: HuggingFace Transfoormers (RoBERTa)
**Container**: Docker, Docker Compose
**CI/CD**: Github Actions (Linting e Testing)
**Monitoraggio**: Prometheus, Grafana
**Orchestra**: Apache Airflow

# Architettura
Ci sono 4 servizi (tramite container) che comunicano tra loro:
_innovators-api_: Il servizio Python/FastAPI che ha il modello di sentiment
_prometheus_: Il database che "estrae" le metriche dall'endpoint _/metrics_ dell'API
_grafana_: Connesso a Prometheus che mostra la salute dall'API in tempo reale
_airflow_: L'orchestratore che gestisce le pipeline di riaddestramento al modello


# Endopoints Disponibili
API: http://localhost:8000
Grafana http://localhost:3000 (Login: admin / admin)
Airflow: http://localhost:8080
Prometheus: http://localhost:9090


# Le scelte che ho fatto:
Ho scelto FastAPI per la sua alta performance e facilità di creazione API robuste.
 - Il modello di HuggingFace viene caricato all'avvio e servito tramite endpoint (_/analyze_).
 - Ho implementato una semplice interfaccia **HTML** sul root (_/_) per testare rapidamente l'API dal browser.
 - Ho integrato la libreria _prometheus-fastapi-instrumentator_ per trovare automaticamente le metriche dell'API sull'endpoint _/metrics_

 CI/CD
  - Ho implementato una pipeline di Continuous Integration (_.github/workflows/CI-CD.yml_) che ad ogni push Github Actions avvia il runner.
  - Il codice viene controllato con _flake8_ (configurato tramite _setup.cfg_ per evitare errori data la scelta di aver creato l'HTML sul root)
  - Test unitari che vengono eseguiti con _pytest_ 

Monitoraggio
 - Prometheus è configurato (_prometheus.yml) per estrarre automaticamente le metriche esposte dall'API
 - Grafana: Ho creato una dashboard (persistente) per visualizzare le metriche da Prometheus (Traffico API, Latenza, Tasso Errori)

Orchestrazione
 - Per gestire questo ho integrato Apache Airflow, definendo la pipeline di ri-addestramento tramite DAG Python
 - La DAG simula i passaggi di Fetch Data -> Train Model -> Deploy Model, pronta per essere estesa con script di training reali
 - Questo setup mi permette di schedulare e / o triggerare manualmente il retraining del modello, completando il ciclo di vita MLOps.