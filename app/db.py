from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Allow overriding the database URL via environment for CI or local runs.
# Default to a file-based SQLite DB to avoid requiring Postgres to be running.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
	# sqlite needs this for multithreaded access in test scenarios
	engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def get_db():
	"""FastAPI dependency that yields a SQLAlchemy Session and ensures it is closed."""
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
