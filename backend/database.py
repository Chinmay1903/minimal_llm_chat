import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import load_env    

load_env()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local.db")
# Heroku sometimes provides 'postgres://'; SQLAlchemy expects 'postgresql+psycopg2://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)

print(f"Using database: {DATABASE_URL}")


engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        