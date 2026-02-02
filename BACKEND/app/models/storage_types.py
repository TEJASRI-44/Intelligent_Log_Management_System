from sqlalchemy import Column, SmallInteger, String
from app.database import Base

class StorageType(Base):
    __tablename__ = "storage_types"

    storage_type_id = Column(SmallInteger, primary_key=True)
    storage_name = Column(String(30), unique=True)
