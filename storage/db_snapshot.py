from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Iterator

from storage.models_snapshot import CryptoSnapshot
from storage.base_snapshot import BaseSnapshot
from config.settings import SNAPSHOT_DB_CONFIG
from utils.logger import get_logger

logger = get_logger(__name__)

_engine = None
_SessionLocal = None

def get_engine_snapshot() :
    global _engine

    if _engine is None :
        logger.info("Creating new database engine")
        user = SNAPSHOT_DB_CONFIG["user"]
        password = SNAPSHOT_DB_CONFIG["password"]
        host = SNAPSHOT_DB_CONFIG["host"]
        port = SNAPSHOT_DB_CONFIG["port"]
        database = SNAPSHOT_DB_CONFIG["database"]

        db_url = (
            f"postgresql+psycopg2://{user}:{password}"
            f"@{host}:{port}/{database}"
        )
        _engine = create_engine(
            db_url,
            pool_pre_ping=True,
            echo=False
        )
        BaseSnapshot.metadata.create_all(bind=_engine)
    return _engine

@contextmanager
def get_session_snapshot() -> Iterator[Session] :
    global _SessionLocal

    if _SessionLocal is None :
        engine = get_engine_snapshot()
        _SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )

    session = _SessionLocal()

    try :
        yield session
        session.commit()

    except Exception as e :
        session.rollback()
        logger.exception("Session rollback due to error")
        raise
    finally :
        session.close()