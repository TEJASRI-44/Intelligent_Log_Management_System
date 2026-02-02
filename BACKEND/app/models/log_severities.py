from sqlalchemy import Column, SmallInteger, String, Integer
from app.database import Base

class LogSeverity(Base):
    __tablename__ = "log_severities"

    severity_id = Column(SmallInteger, primary_key=True)
    severity_code = Column(String(10), unique=True, nullable=False)
    severity_level = Column(Integer, nullable=False)
    description = Column(String)
