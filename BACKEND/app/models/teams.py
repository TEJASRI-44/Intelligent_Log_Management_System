from sqlalchemy import Column, BigInteger, String, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base

class Team(Base):
    __tablename__ = "teams"

    team_id = Column(BigInteger, primary_key=True)
    team_name = Column(String(150), unique=True, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()")
    )

    upload_policies = relationship(
        "TeamUploadPolicy",
        back_populates="team",
        cascade="all, delete-orphan"
    )
