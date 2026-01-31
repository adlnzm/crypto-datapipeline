from utils.validator import validate_market_record
from utils.logger import get_logger
from utils.datetime_utils import parse_iso_ts

logger = get_logger(__name__)

def clean_market_data(records) :
    if records :
        logger.debug("Sample raw record keys: %s", records[0].keys())

    cleaned = []

    for r in records :
        if not validate_market_record(r) :
            continue

        r["last_updated"] = parse_iso_ts(r.get("last_updated"))

        cleaned.append(r)

    logger.info(f"Cleaned {len(cleaned)} of {len(records)} records")
    return cleaned