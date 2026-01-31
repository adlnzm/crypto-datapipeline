import time
from requests.exceptions import HTTPError
from typing import List, Dict, Optional
from datetime import datetime

from ingestion.coingecko_client import CoinGeckoClient
from config.settings import PIPELINE_CONFIG, PIPELINE_NAME, configure_logging
from utils.logger import get_logger

logger = get_logger(__name__)

def fetch_market_snapshot(
        since_timestamp: Optional[str] = None
) -> List[Dict] :
    
    client = CoinGeckoClient()

    per_page = 25 
    max_records = PIPELINE_CONFIG["max_records_per_run"]
    sleep_seconds = 6

    all_records: List[Dict] = []
    page = 1

    logger.info("Starting market data ingestion")

    while len(all_records) < max_records :
        logger.debug(f"Fetching page {page}")

        try :
            records = client.get_market_data(
                per_page=per_page,
                page=page
            )

        except HTTPError as e :
            if e.response is not None and e.response.status_code == 429 :
                logger.warning(
                    "Rate limit hit at page %s. Returning partial snapshot (%s records).",
                    page,
                    len(all_records),
                )
                break
            raise

        if not records :
            break

        all_records.extend(records)

        if len(records) < per_page :
            logger.info("Last page Reached")
            break

        page += 1
        time.sleep(sleep_seconds)

    logger.info(f"Fetched {len(all_records)} market snapshot records")
    return all_records