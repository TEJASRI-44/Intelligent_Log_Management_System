from sqlalchemy import Column, SmallInteger, String
from app.database import Base

class Permission(Base):
    __tablename__ = "permissions"

    permission_id = Column(SmallInteger, primary_key=True)
    permission_key = Column(String(100), unique=True, nullable=False)
    description = Column(String)
