from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Iterator

from storage.models_timeseries import CryptoTimeseries
from storage.base_timeseries import BaseTimeseries
from config.settings import TIMESERIES_DB_CONFIG
from utils.logger import get_logger

logger = get_logger(__name__)

_engine = None
_SessionLocal = None

def get_engine_timeseries() :
    global _engine

    if _engine is None :
        logger.info("Creating timeseries DB engine")
        user = TIMESERIES_DB_CONFIG["user"]
        password = TIMESERIES_DB_CONFIG["password"]
        host = TIMESERIES_DB_CONFIG["host"]
        port = TIMESERIES_DB_CONFIG["port"]
        database = TIMESERIES_DB_CONFIG["database"]
        db_url = (
            f"postgresql+psycopg2://{user}:{password}"
            f"@{host}:{port}/{database}"
        )
        _engine = create_engine(db_url, pool_pre_ping=True, echo=False)
        BaseTimeseries.metadata.create_all(bind=_engine)
    return _engine

@contextmanager
def get_session_timeseries() -> Iterator[Session] :
    global _SessionLocal

    if _SessionLocal is None :
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine_timeseries())
    session = _SessionLocal()
    try :
        yield session
        session.commit()
    except Exception :
        session.rollback()
        raise
    finally :
        session.close()