from typing import List, Dict
from statistics import mean

from utils.logger import get_logger

logger = get_logger(__name__)

def compute_market_aggregates(records: List[Dict]) -> Dict :
    prices = [
        r["current_price"]
        for r in records
        if r.get("current_price") is not None
    ]

    market_caps = [
        r["market_cap"]
        for r in records
        if r.get("market_cap") is not None
    ]

    aggregates = {
        "total_assets": len(records),
        "average_price": mean(prices) if prices else None,
        "total_market_cap": sum(market_caps) if market_caps else None,
    }

    logger.info("Computed market aggregates")

    return aggregates