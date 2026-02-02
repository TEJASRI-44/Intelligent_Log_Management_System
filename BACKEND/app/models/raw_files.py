from sqlalchemy import Column, BigInteger, String,Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class RawFile(Base):
    __tablename__ = "raw_files"

    file_id = Column(BigInteger, primary_key=True)
    team_id = Column(BigInteger, ForeignKey("teams.team_id"))
    uploaded_by = Column(BigInteger, ForeignKey("users.user_id"))

    original_name = Column(String(255), nullable=False)
    file_size_bytes = Column(BigInteger, nullable=False)
    checksum = Column(String(64), unique=True, nullable=False)

    format_id = Column(BigInteger, ForeignKey("file_formats.format_id"))
    source_id = Column(BigInteger, ForeignKey("log_sources.source_id"))

    storage_type_id = Column(BigInteger)
    storage_path = Column(String, nullable=False)
    status_id = Column(
        BigInteger,
        ForeignKey("upload_statuses.status_id"), 
    )
    is_deleted = Column(Boolean, default=False) 

    uploaded_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    
    logs = relationship(
        "LogEntry",
        back_populates="file",
        cascade="all, delete-orphan"
    )
    user = relationship("User", backref="uploaded_files")
    team = relationship("Team", backref="team_files")
   
    # RawFile model
    status = relationship(
    "UploadStatus",
    primaryjoin="RawFile.status_id == UploadStatus.status_id",
    lazy="joined"
    )
 