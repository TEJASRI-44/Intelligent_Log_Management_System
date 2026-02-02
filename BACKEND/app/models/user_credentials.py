from sqlalchemy import Column, BigInteger, String, Boolean, ForeignKey, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base

class UserCredentials(Base):
    __tablename__ = "user_credentials"

    credential_id = Column(BigInteger, primary_key=True)

    user_id = Column(
        BigInteger,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    password_hash = Column(String, nullable=False)
    password_algo = Column(String(50), nullable=False)

    failed_attempts = Column(BigInteger, server_default=text("0"))
    last_failed_at = Column(TIMESTAMP(timezone=True))

    is_locked = Column(Boolean, server_default=text("false"))
    locked_until = Column(TIMESTAMP(timezone=True))

    password_changed_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()")
    )

    user = relationship("User", back_populates="credentials")
