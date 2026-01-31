import requests
import time
from typing import List, Dict
from datetime import datetime

def fetch_market_timeseries(
    coin_id: str,
    from_ts: int,
    to_ts: int,
    max_retires: int = 5
) -> List[Dict] :
    
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range"

    for attempt in range(1, max_retires + 1) :
        response = requests.get(
            url,
            params={
                "vs_currency": "usd",
                "from": from_ts,
                "to": to_ts,
            },
            timeout=15,
        )

        if response.status_code == 429 :
            sleep_time = attempt * 10
            time.sleep(sleep_time)
            continue
        
        response.raise_for_status()
        break
    
    else :
        raise RuntimeError(f"Failed after {max_retires} retires for {coin_id}")
    
    data = response.json()

    prices = data.get("prices", [])
    market_caps = data.get("market_caps", [])
    volumes = data.get("total_volumes", [])

    records: List[Dict] = []

    for i in range(len(prices)) :
        ts_ms, price = prices[i]

        record = {
            "coin_id": coin_id,
            "timestamp": datetime.utcfromtimestamp(ts_ms / 1000),
            "price": price,
            "market_cap": market_caps[i][1] if i < len(market_caps) else None,
            "volume": volumes[i][1] if i < len(volumes) else None, 
        }

        records.append(record)

    return records