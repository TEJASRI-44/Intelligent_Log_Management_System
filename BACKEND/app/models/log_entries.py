from sqlalchemy import Boolean, Column, BigInteger, SmallInteger, String, ForeignKey, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base

class LogEntry(Base):
    __tablename__ = "log_entries"

    log_id = Column(BigInteger, primary_key=True)

    file_id = Column(
        BigInteger,
        ForeignKey("raw_files.file_id", ondelete="CASCADE"),
        nullable=False
    )

    log_timestamp = Column(TIMESTAMP(timezone=True), nullable=False)

    severity_id = Column(SmallInteger, ForeignKey("log_severities.severity_id"))
    category_id = Column(SmallInteger, ForeignKey("log_categories.category_id"))
    environment_id = Column(SmallInteger, ForeignKey("environments.environment_id"))

    service_name = Column(String(150))
    host_name = Column(String(150))

    message = Column(String, nullable=False)
    raw_log = Column(String)
    is_deleted = Column(Boolean, default=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()")
    )

    # ✅ MATCHES RawFile.logs
    file = relationship(
        "RawFile",
        back_populates="logs"
    )
