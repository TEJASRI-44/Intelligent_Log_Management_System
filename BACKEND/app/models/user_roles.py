from sqlalchemy import Column, BigInteger, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class UserRole(Base):
    __tablename__ = "user_roles"

    user_id = Column(
        BigInteger,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True
    )
    role_id = Column(
        SmallInteger,
        ForeignKey("roles.role_id", ondelete="CASCADE"),
        primary_key=True
    )

    user = relationship("User", back_populates="roles")
    role = relationship("Role")
