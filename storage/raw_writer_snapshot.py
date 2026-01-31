import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from config.settings import SNAPSHOT_RAW_DIR
from utils.logger import get_logger
from utils.json_utils import json_safe

logger = get_logger(__name__)

def write_raw_snapshot(records: List[Dict]) -> Path :
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"market_data_{timestamp}.json"
    filepath = SNAPSHOT_RAW_DIR / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Writing raw data to {filepath}")

    with open(filepath, "w", encoding="utf-8") as f :
        json.dump(records, f, indent=2, default=json_safe)

    logger.info("Raw data successfully written")
    return filepath