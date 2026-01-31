from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from storage.base_snapshot import BaseSnapshot

class CryptoSnapshot(BaseSnapshot) :
    __tablename__ = "crypto_snapshot"

    id = Column(Integer, primary_key=True, autoincrement=True)
    coin_id = Column(String, index=True, nullable=False)
    symbol = Column(String, index=True, nullable=False)
    name = Column(String, nullable=False)
    current_price = Column(Float)
    market_cap = Column(Float)
    market_cap_rank = Column(Integer)
    total_volume = Column(Float)
    high_24h = Column(Float)
    low_24h = Column(Float)
    price_change_24h = Column(Float)
    price_change_percentage_24h = Column(Float)
    last_updated = Column(DateTime)
    ingested_at = Column(DateTime, default=datetime.utcnow)