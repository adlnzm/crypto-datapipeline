import json
from pathlib import Path
from typing import List, Dict
from config.settings import TIMESERIES_RAW_DIR
from utils.logger import get_logger
from utils.json_utils import json_safe
from datetime import datetime

logger = get_logger(__name__)

def write_raw_timeseries(records: List[Dict]) -> Path :
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"timeseries_{timestamp}.json"
    filepath = TIMESERIES_RAW_DIR / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f :
        json.dump(records, f, indent=2, default=json_safe)

    logger.info(f"Timeseries raw data written: {filepath}")
    return filepath