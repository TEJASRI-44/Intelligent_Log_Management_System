from sqlalchemy import Column, BigInteger, SmallInteger, Boolean, ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from app.database import Base
from sqlalchemy.orm import relationship

class TeamUploadPolicy(Base):
    __tablename__ = "team_upload_policies"

    policy_id = Column(BigInteger, primary_key=True)

    team_id = Column(
        BigInteger,
        ForeignKey("teams.team_id", ondelete="CASCADE"),
        nullable=False
    )

    source_id = Column(
        SmallInteger,
        ForeignKey("log_sources.source_id"),
        nullable=False
    )

    format_id = Column(
        SmallInteger,
        ForeignKey("file_formats.format_id"),
        nullable=False
    )

    is_allowed = Column(Boolean, nullable=False, server_default=text("true"))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))

    __table_args__ = (
        UniqueConstraint(
            "team_id",
            "source_id",
            "format_id",
            name="uq_team_source_format"
        ),
    )

    # ✅ ADD THIS
    team = relationship(
        "Team",
        back_populates="upload_policies"
    )
