from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

USER = "portafolios"
PASSWORD = "portafolios2025"
HOST = "localhost"
PORT = "1521"
SERVICE = "XE"

DATABASE_URL = (
    f"oracle+oracledb://{USER}:{PASSWORD}@{HOST}:{PORT}/?service_name={SERVICE}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
