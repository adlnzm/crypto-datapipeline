import time 
import requests
from typing import Dict, List, Optional

from config.settings import API_CONFIG, PIPELINE_CONFIG
from utils.logger import get_logger

logger = get_logger(__name__)

class CoinGeckoClient :
    def __init__(self) :
        self.base_url = API_CONFIG["crypto_base_url"]
        self.timeout = API_CONFIG["timeout_seconds"]
        self.retry_attempts = PIPELINE_CONFIG["retry_attempts"]
        self.retry_backoff = PIPELINE_CONFIG["retry_backoff"]

    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict :
        url = f"{self.base_url}{endpoint}"

        for attempt in range(1, self.retry_attempts + 1) :
            try :
                logger.debug(f"GET {url} | Attempt {attempt}")

                response = requests.get(
                    url,
                    params=params,
                    timeout=self.timeout
                )

                response.raise_for_status()
                return response.json()
            
            except requests.exceptions.RequestException as e :
                logger.warning(
                    f"Request failed (attempt {attempt}/{self.retry_attempts}): {e}"
                )

                if attempt == self.retry_attempts :
                    logger.error("Max retries exceeded")
                    raise

                sleep_time = self.retry_backoff ** attempt
                time.sleep(sleep_time)

    def get_supported_coins(self) -> List[Dict] :
        return self._get("/coins/list")

    def get_market_data(
            self,
            vs_currency: str = "usd",
            per_page: int = 50,
            page: int = 1
            ) -> List[Dict] :
        
        params = {
            "vs_currency": vs_currency,
            "order": "market_cap_desc",
            "per_page": per_page,
            "page": page,
            "sparkline": False
        }

        return self._get("/coins/markets", params=params)

    def get_coin_details(self, coin_id: str) -> Dict :
        return self._get(f"/coins/{coin_id}")