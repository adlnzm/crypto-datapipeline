import time
from typing import Callable

from utils.logger import get_logger

logger = get_logger(__name__)

def run_interval(
        job: Callable,
        interval_seconds: int
) :
    logger.info(f"Scheduler started (interval={interval_seconds}s)")

    while True :
        start_time = time.time()

        try :
            logger.info("Executing scheduled job")
            job()
        except Exception :
            logger.exception("Scheduled job failed")

        elapsed = time.time() - start_time
        sleep_time = max(0, interval_seconds - elapsed)

        logger.info(f"Sleeping for {sleep_time:.2f} seconds")
        time.sleep(sleep_time)