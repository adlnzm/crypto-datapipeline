import sys
from datetime import datetime

from ingestion import fetch_market_snapshot
from transformations import clean_market_data
from transformations import compute_market_aggregates
from orchestration import get_last_run, update_last_run
from config.settings import PIPELINE_NAME, configure_logging
from storage.db_snapshot import get_session_snapshot, get_engine_snapshot
from storage.models_snapshot import CryptoSnapshot
from storage.raw_writer_snapshot import write_raw_snapshot
from storage.processed_writer_snapshot import write_processed_snapshot
from utils.logger import get_logger

logger = get_logger(PIPELINE_NAME)

def run_snapshot_pipeline() -> None :
    logger.info("Pipeline started")
    get_engine_snapshot()

    try :
        raw_data = fetch_market_snapshot()
        write_raw_snapshot(raw_data)
        cleaned_data = clean_market_data(raw_data)
        compute_market_aggregates(cleaned_data)
        write_processed_snapshot(cleaned_data)

        with get_session_snapshot() as session :

            for record in cleaned_data :
                snapshot = CryptoSnapshot(
                    coin_id=record.get("id"),
                    symbol=record.get("symbol"),
                    name=record.get("name"),
                    current_price=record.get("current_price"),
                    market_cap=record.get("market_cap"),
                    market_cap_rank=record.get("market_cap_rank"),
                    total_volume=record.get("total_volume"),
                    high_24h=record.get("high_24h"),
                    low_24h=record.get("low_24h"),
                    price_change_24h=record.get("price_change_24h"),
                    price_change_percentage_24h=record.get("price_change_percentage_24h"),
                    last_updated=record.get("lat_updated"),
                    ingested_at=datetime.utcnow(),
                )
                session.add(snapshot)

        update_last_run(PIPELINE_NAME)

        logger.info("Pipeline completed successfully")

    except Exception :
        logger.exception("Pipeline failed due to an unexcepted error")
        sys.exit(1)