from sqlalchemy import Column, SmallInteger, String
from sqlalchemy.orm import relationship
from app.database import Base

class Role(Base):
    __tablename__ = "roles"

    role_id = Column(SmallInteger, primary_key=True)
    role_name = Column(String(50), unique=True, nullable=False)
    description = Column(String)

    # ✅ FIXED: Role links to UserRole, NOT User
    user_roles = relationship(
        "UserRole",
        back_populates="role",
        cascade="all, delete-orphan"
    )
