from sqlalchemy import Column, BigInteger, String, Boolean, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True)

    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(100), unique=True)

    is_active = Column(Boolean, server_default=text("true"), nullable=False)
    is_deleted = Column(Boolean, server_default=text("false"), nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()"),
        nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()"),
        onupdate=text("NOW()"),
        nullable=False
    )

    # Relationships
    profile = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete"
    )

    credentials = relationship(
        "UserCredentials",
        back_populates="user",
        uselist=False,
        cascade="all, delete"
    )

    roles = relationship(
        "UserRole",
        back_populates="user",
        cascade="all, delete"
    )

    teams = relationship(
        "UserTeam",
        back_populates="user",
        cascade="all, delete"
    )

    login_history = relationship(
        "LoginHistory",
        back_populates="user",
        cascade="all, delete-orphan"
    )
