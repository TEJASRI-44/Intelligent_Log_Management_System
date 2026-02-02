from sqlalchemy import Column, BigInteger, Boolean, String, ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP, INET
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import text

class LoginHistory(Base):
    __tablename__ = "login_history"

    login_id = Column(BigInteger, primary_key=True)

    user_id = Column(
        BigInteger,
        ForeignKey("users.user_id", ondelete="CASCADE")
    )

    login_time = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()")
    )

    login_ip = Column(INET)
    user_agent = Column(String)
    success = Column(Boolean)
    failure_reason = Column(String(100))

    user = relationship("User", back_populates="login_history")
