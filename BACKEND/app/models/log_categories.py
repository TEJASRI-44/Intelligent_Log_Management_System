from sqlalchemy import Column, SmallInteger, String
from app.database import Base

class LogCategory(Base):
    __tablename__ = "log_categories"

    category_id = Column(SmallInteger, primary_key=True)
    category_name = Column(String(50), unique=True, nullable=False)
