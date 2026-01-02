from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Use SQLite for development if PostgreSQL is not available
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Default to SQLite for easier setup
    DATABASE_URL = "sqlite:///./student_performance.db"
elif DATABASE_URL.startswith("postgresql"):
    # Try PostgreSQL, fallback to SQLite if connection fails
    try:
        test_engine = create_engine(DATABASE_URL, connect_args={"connect_timeout": 2})
        test_engine.connect()
        test_engine.dispose()
    except Exception:
        print("PostgreSQL not available, using SQLite instead")
        DATABASE_URL = "sqlite:///./student_performance.db"

# SQLite needs check_same_thread=False
connect_args = {} if DATABASE_URL.startswith("sqlite") else {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

