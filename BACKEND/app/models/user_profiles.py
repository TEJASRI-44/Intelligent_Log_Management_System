from sqlalchemy import Column, BigInteger, String, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy import text
from app.database import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    profile_id = Column(BigInteger, primary_key=True)

    user_id = Column(
        BigInteger,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100))
    phone_number = Column(String(20))
    profile_image_url = Column(String)
    job_title = Column(String(150))

    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()"),
        onupdate=text("NOW()")
    )

    user = relationship("User", back_populates="profile")
