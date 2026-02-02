from sqlalchemy import Column, SmallInteger, String
from app.database import Base

class FileFormat(Base):
    __tablename__ = "file_formats"

    format_id = Column(SmallInteger, primary_key=True)
    format_name = Column(String(20), unique=True, nullable=False)
