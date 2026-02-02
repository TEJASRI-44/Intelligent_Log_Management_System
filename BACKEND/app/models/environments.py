from sqlalchemy import Column, SmallInteger, String
from app.database import Base

class Environment(Base):
    __tablename__ = "environments"

    environment_id = Column(SmallInteger, primary_key=True)
    environment_code = Column(String(20), unique=True, nullable=False)
    description = Column(String)
