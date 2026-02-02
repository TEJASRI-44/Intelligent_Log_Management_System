from sqlalchemy import Column, BigInteger, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class Archive(Base):
    __tablename__ = "archives"

    archive_id = Column(
        BigInteger,
        primary_key=True,
        index=True
    )

    file_id = Column(
        BigInteger,
        ForeignKey("raw_files.file_id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    archived_on = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    total_records = Column(
        Integer,
        nullable=False
    )
