from sqlalchemy import Column, SmallInteger, String
from app.database import Base

class UploadStatus(Base):
    __tablename__ = "upload_statuses"

    status_id = Column(SmallInteger, primary_key=True)
    status_code = Column(String(30), unique=True, nullable=False)
    description = Column(String)

    