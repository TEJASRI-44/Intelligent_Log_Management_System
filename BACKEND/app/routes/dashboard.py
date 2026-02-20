from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.raw_files import RawFile
from app.models.log_entries import LogEntry
from sqlalchemy import func

# Router for user dashboard APIs
router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats")
def get_user_stats(
    team_id: int,  # Team for which we need stats
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Get logged-in user id from token
    user_id = int(current_user["sub"])

    # Count how many files this user uploaded in this team
    files_uploaded = db.query(RawFile).filter(
        RawFile.uploaded_by == user_id,
        RawFile.team_id == team_id
    ).count()

    # Count total logs generated from those uploaded files
    total_logs = db.query(LogEntry).join(RawFile).filter(
        RawFile.uploaded_by == user_id,
        RawFile.team_id == team_id
    ).count()

    # Count how many ERROR logs are present
    error_logs = db.query(LogEntry).join(RawFile).filter(
        RawFile.uploaded_by == user_id,
        RawFile.team_id == team_id,
        LogEntry.severity == "ERROR"
    ).count()

    # Count how many WARN logs are present
    warning_logs = db.query(LogEntry).join(RawFile).filter(
        RawFile.uploaded_by == user_id,
        RawFile.team_id == team_id,
        LogEntry.severity == "WARN"
    ).count()

    # Return dashboard statistics
    return {
        "files_uploaded": files_uploaded,
        "total_logs": total_logs,
        "error_logs": error_logs,
        "warning_logs": warning_logs
    }