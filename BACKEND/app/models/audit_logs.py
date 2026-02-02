from sqlalchemy import Column, BigInteger, String, ForeignKey, JSON, text
from sqlalchemy.dialects.postgresql import TIMESTAMP
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    audit_id = Column(BigInteger, primary_key=True)

    table_name = Column(String(100), nullable=False)
    record_id = Column(BigInteger, nullable=False)

    action_type = Column(String(20), nullable=False)

    old_data = Column(JSON)
    new_data = Column(JSON)

    changed_by = Column(BigInteger, ForeignKey("users.user_id"))

    changed_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()")
    )
