from fastapi import FastAPI, HTTPException
from typing import List, Dict
import json
from pathlib import Path

from config.settings import (
    PIPELINE_NAME, 
    configure_logging,
    SNAPSHOT_RAW_DIR,
    SNAPSHOT_PROCESSED_DIR,
    TIMESERIES_RAW_DIR,
    TIMESERIES_PROCESSED_DIR,
)
from utils.logger import get_logger

configure_logging()
logger = get_logger(__name__)

app = FastAPI(
    title="Crypto Market Data API",
    description="API exposing crypto market pipeline outputs",
    version="1.0.0"
)

def _load_latest_json(directory: Path) :
    files = sorted(directory.glob("*.json"))
    if not files :
        raise FileNotFoundError(f"No data files found in {directory}")
    with open(files[-1], "r") as f :
        return json.load(f)

@app.get("/health")
def health_check() :
    return {
        "status": "healthy",
        "service": PIPELINE_NAME,
    }

@app.get("/snapshot/raw", response_model=List[Dict])
def get_raw_snapshot() :
    try :
        return _load_latest_json(SNAPSHOT_RAW_DIR)
    
    except Exception as e :
        logger.exception("Failed to fetch raw snapshot data")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/snapshot/processed", response_model=List[Dict])
def get_processed_snapshot() :
    try :
        return _load_latest_json(SNAPSHOT_PROCESSED_DIR)
    except Exception as e :
        logger.exception("Failed to load processed snapshot data")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/timeseries/raw", response_model=List[Dict])
def get_raw_timeseries() :
    try :
        return _load_latest_json(TIMESERIES_RAW_DIR)
    except Exception as e :
        logger.exception("Failed to load raw timeseries data")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/timeseries/processed", response_model=List[Dict])
def get_processed_timeseries() :
    try :
        return _load_latest_json(TIMESERIES_PROCESSED_DIR)
    except Exception as e :
        logger.exception("Failed to load processed timeseries data")
        raise HTTPException(status_code=500, detail=str(e))