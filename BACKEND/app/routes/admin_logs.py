from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.log_entries import LogEntry
from app.models.log_severities import LogSeverity
from app.models.log_categories import LogCategory

# Router for Admin Log Search APIs
router = APIRouter(prefix="/admin/logs", tags=["Admin Logs"])


# Ensure only ADMIN users can access
def require_admin(user):
    roles = user.get("roles", [])
    if "ADMIN" not in roles:
        raise HTTPException(status_code=403, detail="Admin access required")


# Search logs with filters and pagination
@router.get("/search")
def admin_search_logs(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
    category: str | None = Query(None),
    severity: str | None = Query(None),
    keyword: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    # Base query with joins
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

    # Apply optional filters
    if start_date:
        query = query.filter(LogEntry.log_timestamp >= start_date)
    if end_date:
        query = query.filter(LogEntry.log_timestamp <= end_date)
    if category:
        query = query.filter(LogCategory.category_name == category.upper())
    if severity:
        query = query.filter(LogSeverity.severity_code == severity.upper())
    if keyword:
        query = query.filter(LogEntry.message.ilike(f"%{keyword}%"))

    total = query.count()  # Total matching records

    logs = (
        query
        .order_by(LogEntry.log_timestamp.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    # Return paginated results
    return {
        "count": len(logs),
        "page": page,
        "pageSize": limit,
        "results": [
            {
                "timestamp": row.log_timestamp,
                "severity": row.severity_code,
                "category": row.category_name,
                "service": row.service_name,
                "message": row.message
            }
            for row in logs
        ],
        "total": total
    }