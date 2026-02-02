from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.raw_files import RawFile
from app.models.log_entries import LogEntry
from app.models.log_severities import LogSeverity

router = APIRouter(
    prefix="/users/stats",
    tags=["User Statistics"]
)

@router.get("/summary")
def user_dashboard_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user_id = int(current_user["sub"])

    # Files uploaded
    print("user_id:", user_id)
    files_uploaded = (
        db.query(func.count(RawFile.file_id))
        .filter(RawFile.uploaded_by == user_id)
        .scalar()
    )

    # Total logs
    total_logs = (
        db.query(func.count(LogEntry.log_id))
        .join(RawFile, RawFile.file_id == LogEntry.file_id)
        .filter(RawFile.uploaded_by == user_id)
        .scalar()
    )

    # Error logs
    error_logs = (
        db.query(func.count(LogEntry.log_id))
        .join(RawFile, RawFile.file_id == LogEntry.file_id)
        .join(LogSeverity, LogSeverity.severity_id == LogEntry.severity_id)
        .filter(
            RawFile.uploaded_by == user_id,
            LogSeverity.severity_code == "ERROR"
        )
        .scalar()
    )

    # Warning logs
    warning_logs = (
        db.query(func.count(LogEntry.log_id))
        .join(RawFile, RawFile.file_id == LogEntry.file_id)
        .join(LogSeverity, LogSeverity.severity_id == LogEntry.severity_id)
        .filter(
            RawFile.uploaded_by == user_id,
            LogSeverity.severity_code == "WARN"
        )
        .scalar()
    )

    return {
        "files_uploaded": files_uploaded or 0,
        "total_logs": total_logs or 0,
        "error_logs": error_logs or 0,
        "warning_logs": warning_logs or 0
    }
