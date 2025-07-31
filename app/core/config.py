from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from fastapi import Depends

DATABASE_URL = "postgresql://neondb_owner:npg_r64CjIuEcTYy@ep-broad-salad-ae35mqgx-pooler.c-2.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    core = SessionLocal()
    try:
        yield core
    finally:
        core.close()
