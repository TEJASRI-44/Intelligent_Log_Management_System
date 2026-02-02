from sqlalchemy import Column, SmallInteger, String
from app.database import Base

class LogSource(Base):
    __tablename__ = "log_sources"

    source_id = Column(SmallInteger, primary_key=True)
    source_name = Column(String(50), unique=True)
