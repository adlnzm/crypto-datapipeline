from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

from storage.db_snapshot import get_engine_snapshot
from storage.db_timeseries import get_engine_timeseries

get_engine_snapshot()
get_engine_timeseries()

default_args = {
    "owner": "data_eng",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="crypto_market_pipelines",
    default_args=default_args,
    description="Crypto market snapshot pipeline",
    schedule_interval="*/30 * * * *",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["crypto", "market", "snapshot"],
) as dag :

    run_snapshot = BashOperator(
        task_id="run_market_snapshot",
        bash_command="python -m pipeline snapshot",
    )

    run_timeseries = BashOperator(
        task_id="run_market_timesries",
        bash_command="python -m pipeline timeseries",
    )

    run_snapshot >> run_timeseries