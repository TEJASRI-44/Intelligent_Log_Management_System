from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models.log_entries import LogEntry
from app.models.log_categories import LogCategory
from app.models.log_severities import LogSeverity

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

    #  Date filters
    if start_date:
        query = query.filter(LogEntry.log_timestamp >= start_date)
    if end_date:
        query = query.filter(LogEntry.log_timestamp <= end_date)

    # Category filter
    if category:
        query = query.filter(LogCategory.category_name == category.upper())

    # Severity filter
    if severity:
        query = query.filter(LogSeverity.severity_code == severity.upper())

    #  Keyword search
    if keyword:
        query = query.filter(LogEntry.message.ilike(f"%{keyword}%"))

    logs = query.order_by(LogEntry.log_timestamp.desc()).limit(200).all()

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
