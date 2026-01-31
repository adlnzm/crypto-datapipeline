import os
from pathlib import Path
import logging 
import logging.config
import yaml

PIPELINE_NAME = "crypto_market_datapipeline"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOGS_DIR = PROJECT_ROOT / "logs"
CONFIG_DIR = PROJECT_ROOT  / "config"

AIRFLOW_DATA_DIR = Path("/opt/airflow/data")

SNAPSHOT_RAW_DIR = AIRFLOW_DATA_DIR / "snapshot" / "raw"
SNAPSHOT_PROCESSED_DIR = AIRFLOW_DATA_DIR / "snapshot" / "processed"
TIMESERIES_RAW_DIR = AIRFLOW_DATA_DIR / "timeseries" / "raw"
TIMESERIES_PROCESSED_DIR = AIRFLOW_DATA_DIR / "timeseries" / "processed"

REQUIRED_DIRS = [
    LOGS_DIR,
    SNAPSHOT_RAW_DIR,
    SNAPSHOT_PROCESSED_DIR,
    TIMESERIES_RAW_DIR,
    TIMESERIES_PROCESSED_DIR,
]

API_CONFIG = {
    "crypto_base_url": "https://api.coingecko.com/api/v3",
    "timeout_seconds": 10,
    "retry_attempts": 3,
    "retry_backoff": 2
}

SNAPSHOT_DB_CONFIG = {
    "type": "postgres",
    "user": os.getenv("SNAPSHOT_DB_USER", "airflow"),
    "password": os.getenv("SNAPSHOT_DB_PASSWORD", "airflow"),
    "host": os.getenv("SNAPSHOT_DB_HOST", "postgres"),
    "port": 5432,
    "database": "airflow_snapshot",
}

TIMESERIES_DB_CONFIG = {
    "type": "postgres",
    "user": os.getenv("TIMESERIES_DB_USER", "airflow"),
    "password": os.getenv("TIMESERIES_DB_PASSWORD", "airflow"),
    "host": os.getenv("TIMESERIES_DB_HOST", "postgres"),
    "port": 5432,
    "database": "airflow_timeseries"
}

PIPELINE_CONFIG = {
    "batch_size": 25,
    "max_records_per_run": 150,
    "retry_attempts": 1,
    "retry_backoff": 15,
    "fail_fast": False
}

LOGGING_YAML = CONFIG_DIR / "logging.yaml"

def configure_logging() :
    if LOGGING_YAML.exists() :
        with open(LOGGING_YAML) as f :
            config = yaml.safe_load(f)
            logging.config.dictConfig(config)
    else :
        logging.basicConfig(level=logging.INFO)

def validate_settings() :
    for d in REQUIRED_DIRS :
        if not d.exists() :
            raise RuntimeError(f"Missing required directory: {d}")
        
validate_settings()