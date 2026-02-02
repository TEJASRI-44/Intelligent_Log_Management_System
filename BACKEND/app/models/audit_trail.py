from sqlalchemy import Column, BigInteger, String, func
from sqlalchemy.dialects.postgresql import TIMESTAMP


from app.database import Base

class AuditTrail(Base):
    __tablename__ = "audit_trail"

    audit_id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)

    action_type = Column(String(50), nullable=False)
    entity_type = Column(String(50))
    entity_id = Column(BigInteger)

   
    action_time = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),   # ✅ FIX
        nullable=False
    )
