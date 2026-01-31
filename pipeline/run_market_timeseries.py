import time
from datetime import datetime
from ingestion import fetch_market_timeseries
from orchestration import update_last_run
from config.settings import PIPELINE_NAME
from utils.logger import get_logger

from storage.raw_writer_timeseries import write_raw_timeseries
from storage.db_timeseries import get_session_timeseries, get_engine_timeseries
from storage.models_timeseries import CryptoTimeseries
from storage.processed_writer_timeseries import write_processed_timeseries

logger = get_logger(PIPELINE_NAME)

COINS = ["bitcoin", "ethereum"]

def run_timeseries_pipeline() :
    get_engine_timeseries()
    
    logger.info("Timeseries pipeline started")

    now = int(time.time())
    one_day_ago = now - 86400

    all_records = []

    for coin in COINS :
        records = fetch_market_timeseries(
            coin_id=coin, 
            from_ts=one_day_ago, 
            to_ts=now
        )

        if not records :
            logger.warning(f"No timeseries data fetched for {coin}")
            continue

        logger.info(f"Fetched {len(records)} records for {coin}")

        all_records.extend(records)
        time.sleep(15)
        
    write_raw_timeseries(all_records)

    processed_records = []

    for r in all_records :
        assert isinstance(r["timestamp"], datetime)
        assert r["coin_id"]

        processed_records.append({
            "coin_id": r["coin_id"],
            "timestamp": r["timestamp"],
            "price": r["price"],
            "market_cap": r.get("market_cap"),
            "volume": r.get("volume"),      
        })
    
    write_processed_timeseries(processed_records)

    with get_session_timeseries() as session :
        session.add_all(
            [CryptoTimeseries(**r) for r in processed_records]
        )

    update_last_run("crypto_timeseries")
    logger.info(f"Inserted {len(processed_records)} timeseries rows")
    logger.info("Timeseries pipeline completed")