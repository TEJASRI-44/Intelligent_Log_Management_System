from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.raw_files import RawFile
from app.models.log_entries import LogEntry
from sqlalchemy import func

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats")
def get_user_stats(
    team_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user_id = int(current_user["sub"])

    files_uploaded = db.query(RawFile).filter(
        RawFile.uploaded_by == user_id,
        RawFile.team_id == team_id
    ).count()

    total_logs = db.query(LogEntry).join(RawFile).filter(
        RawFile.uploaded_by == user_id,
        RawFile.team_id == team_id
    ).count()

    error_logs = db.query(LogEntry).join(RawFile).filter(
        RawFile.uploaded_by == user_id,
        RawFile.team_id == team_id,
        LogEntry.severity == "ERROR"
    ).count()

    warning_logs = db.query(LogEntry).join(RawFile).filter(
        RawFile.uploaded_by == user_id,
        RawFile.team_id == team_id,
        LogEntry.severity == "WARN"
    ).count()

    return {
        "files_uploaded": files_uploaded,
        "total_logs": total_logs,
        "error_logs": error_logs,
        "warning_logs": warning_logs
    }
