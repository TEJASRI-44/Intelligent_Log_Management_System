from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.log_entries import LogEntry
from app.models.log_categories import LogCategory
from app.models.log_severities import LogSeverity

# Router for log search and filtering APIs
router = APIRouter(prefix="/logs", tags=["Log Processing"])


@router.get("/search")
def search_logs(
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
    category: str | None = Query(None),
    severity: str | None = Query(None),
    keyword: str | None = Query(None),
    db: Session = Depends(get_db)
):
    # Base query joining severity and category tables
    query = (
        db.query(
            LogEntry.log_timestamp,
            LogEntry.service_name,
            LogEntry.message,
            LogSeverity.severity_code,
            LogCategory.category_name
        )
        .join(LogSeverity, LogEntry.severity_id == LogSeverity.severity_id)
        .join(LogCategory, LogEntry.category_id == LogCategory.category_id)
    )

    # Apply date range filters if provided
    if start_date:
        query = query.filter(LogEntry.log_timestamp >= start_date)
    if end_date:
        query = query.filter(LogEntry.log_timestamp <= end_date)

    # Filter by category if given
    if category:
        query = query.filter(LogCategory.category_name == category.upper())

    # Filter by severity if given
    if severity:
        query = query.filter(LogSeverity.severity_code == severity.upper())

    # Search logs by keyword inside message
    if keyword:
        query = query.filter(LogEntry.message.ilike(f"%{keyword}%"))

    # Limit results to latest 200 logs
    logs = query.order_by(LogEntry.log_timestamp.desc()).limit(200).all()

    # Return filtered log results
    return {
        "count": len(logs),
        "results": [
            {
                "timestamp": row.log_timestamp,
                "severity": row.severity_code,
                "category": row.category_name,
                "service": row.service_name,
                "message": row.message
            }
            for row in logs
        ]
    }