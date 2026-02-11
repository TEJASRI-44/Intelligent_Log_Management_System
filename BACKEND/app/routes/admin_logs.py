from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.core.dependencies import get_current_user
from fastapi import HTTPException
from app.models.log_entries import LogEntry
from app.models.log_severities import LogSeverity
from app.models.log_categories import LogCategory

router = APIRouter(prefix="/admin/logs", tags=["Admin Logs"])

def require_admin(user):
    roles = user.get("roles", [])
    if "ADMIN" not in roles:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
@router.get("/search")
def admin_search_logs(
    page: int = Query(1, ge=1),
    start_date: datetime | None = Query(None),
    limit:int=Query(10,ge=1,le=100),
    end_date: datetime | None = Query(None),
    category: str | None = Query(None),
    severity: str | None = Query(None),
    keyword: str | None = Query(None),
    db: Session = Depends(get_db),
   
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

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

    logs = (query
                .order_by(LogEntry.log_timestamp.desc())
                .offset((page-1)*limit)
                .limit(limit)
                .all())
    total=query.count()
    return {
        "count": len(logs),
        "page":page,
        "pageSize":limit,    
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
