from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import os, urllib.parse
load_dotenv()
# Fetch variables
USER = os.getenv("user")
PASS = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")
PASSWORD = urllib.parse.quote_plus(str(PASS))
print(f"USER: {USER}, PASSWORD: {PASSWORD}, HOST: {HOST}, PORT: {PORT}, DBNAME: {DBNAME}")
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)



Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
