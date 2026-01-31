from sqlalchemy import Column, Integer, String, Float, BigInteger, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from storage.base_timeseries import BaseTimeseries

class CryptoTimeseries(BaseTimeseries) :
    __tablename__ = "crypto_timeseries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    coin_id = Column(String, index=True, nullable=False)
    timestamp = Column(DateTime, index=True, nullable=False)
    price = Column(Float)
    market_cap = Column(Float)
    volume = Column(Float)
    ingested_at = Column(DateTime, default=datetime.utcnow)