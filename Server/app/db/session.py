from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DB_URI = os.getenv('PGQL_URL')

# print('PGQL_URL: ', DB_URI)

engine = create_engine(DB_URI)

LocalSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()