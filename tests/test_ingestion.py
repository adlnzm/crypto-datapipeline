import pytest
from unittest.mock import patch

from ingestion import CoinGeckoClient
from ingestion import fetch_market_snapshot
from ingestion import fetch_market_timeseries

@pytest.fixture
def sample_market_response() :
    return [
        {
            "id": "bitcoin",
            "symbol": "btc",
            "name": "Bitcoin",
            "current_price": 50000,
            "market_cap": 900000000,
            "total_volume": 35000000,
            "high_24h": 51000,
            "low_24h": 48000,
            "price_change_24h": 1000,
            "price_change_percentage_24h": 2.0,
            "last_updated": "2024-01-01T00:00:00Z",
        }
    ]

@pytest.fixture
def sample_timeseries_response() :
    return {
        "prices": [
            [1700000000000, 50000.0],
            [1700003600000, 50500.0],
        ],
        "market_cap": [
            [1700000000000, 900000000],
            [1700003600000, 910000000],
        ],
        "total_volume": [
            [1700000000000, 35000000],
            [1700003600000, 36000000],
        ],
    }

def test_coingecko_client_instantiation() :
    client = CoinGeckoClient()
    assert client.base_url is not None
    assert client.timeout  > 0

@patch("ingestion.coingecko_client.requests.get")
def test_fetch_market_data_success(mock_get, sample_snapshot_response) :
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = sample_snapshot_response
    mock_get.return_value.raise_for_status.return_value = None

    records = fetch_market_snapshot()

    assert isinstance(records, list)
    assert len(records) > 0
    assert records[0]["id"] == "bitcoin"

@patch("ingestion.coingecko_client.requests.get") 
def test_fetch_market_data_empty_response(mock_get) :
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = []
    mock_get.return_value.raise_for_status.return_value = None

    records = fetch_market_snapshot()
    assert records == []

def test_fetch_market_timeseries_success(mock_get, sample_timeseries_response) :
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = sample_timeseries_response
    mock_get.return_value.raise_for_status.return_value = None

    records = fetch_market_timeseries(
        coin_id="bitcoin",
        from_ts="1700000000000",
        to_ts=1700003600,
    )

    assert isinstance(records, list)
    assert len(records) == 2

    assert records[0]["coin_id"] == "bitcoin"
    assert "price" in records[0]
    assert "market_cap" in records[0]
    assert "volume" in records[0]