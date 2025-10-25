from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2025, 9, 25),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Definizione della DAG
with DAG(
    "sentiment_model_retraining",
    default_args=default_args,
    description="Pipeline per il retraining del modello di sentiment.",
    schedule_interval=None,
    catchup=False,
) as dag:

    # T1: Simula il download di nuovi dati
    t1_fetch_data = BashOperator(
        task_id="fetch_new_data",
        bash_command='echo "--- Sto scaricando nuovi dati etichettati... ---" && sleep 5',
    )

    # T2: Simula il training del modello
    t2_train_model = BashOperator(
        task_id="train_new_model",
        bash_command='echo "--- Inizio il retraining del modello... ---" && sleep 10 && echo "--- Retraining completato. ---"',
    )

    # T3: Simula il deploy del nuovo modello
    t3_deploy_model = BashOperator(
        task_id="deploy_new_model",
        bash_command='echo "--- Salvo il modello e lo metto in produzione... ---" && sleep 5',
    )

    # 4. Orchestra
    t1_fetch_data >> t2_train_model >> t3_deploy_model
