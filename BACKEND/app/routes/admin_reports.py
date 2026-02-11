
from fastapi import APIRouter, Depends,HTTPException
from datetime import datetime, timedelta
from fastapi.params import Query
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date, desc

from app.database import get_db
from app.core.dependencies import get_current_user

from app.models.log_entries import LogEntry
from app.models.log_severities import LogSeverity
from app.models.raw_files import RawFile
from app.models.log_categories import LogCategory

router = APIRouter(
    prefix="/admin/reports",
    tags=["Admin Reports"]
)

# ---------------------------------------------------------
# Helper: Admin access check
# ---------------------------------------------------------
def require_admin(user):
    roles = user.get("roles", [])
    if "ADMIN" not in roles:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

# ---------------------------------------------------------
# 1️⃣ Logs Per Day
# ---------------------------------------------------------
from sqlalchemy import func, cast, Date, desc

@router.get("/logs-per-day")
def logs_per_day(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    log_date_expr = cast(LogEntry.log_timestamp, Date)

    results = (
        db.query(
            log_date_expr.label("log_date"),
            func.count(LogEntry.log_id).label("total_logs")
        )
        .group_by(log_date_expr)
        .order_by(desc(log_date_expr))
        .limit(30)
        .all()
    )
    print(results)

    return [
        {
            "log_date": row.log_date,
            "total_logs": row.total_logs
        }
        for row in results
    ]

# ---------------------------------------------------------
# 2️⃣ Top Error Types (ERROR + FATAL)
# ---------------------------------------------------------
@router.get("/top-errors")
def top_error_types(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    response = []

    # Fetch ERROR + FATAL severities
    severities = (
        db.query(LogSeverity)
        .filter(LogSeverity.severity_code.in_(["ERROR", "FATAL"]))
        .all()
    )

    for sev in severities:
        # Total error count
        total_count = (
            db.query(func.count(LogEntry.log_id))
            .filter(LogEntry.severity_id == sev.severity_id)
            .scalar()
        )

        # Latest error log samples
        logs = (
            db.query(LogEntry)
            .filter(LogEntry.severity_id == sev.severity_id)
            .order_by(LogEntry.log_timestamp.desc())
            .all()
        )

        response.append({
            "severity": sev.severity_code,
            "count": total_count,
            "sample_logs": [
                {
                    "timestamp": log.log_timestamp,
                    "service": log.service_name,
                    "message": log.message
                }
                for log in logs
            ]
        })

    return response


# ---------------------------------------------------------
# 3️⃣ Most Active Systems (by service_name)
# ---------------------------------------------------------



@router.get("/active-systems")
def most_active_systems(
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    query = db.query(LogEntry)

    # 🔹 Date range filtering (IMPORTANT)
    if start_date:
        query = query.filter(LogEntry.log_timestamp >= start_date)
    if end_date:
        query = query.filter(LogEntry.log_timestamp <= end_date)

    # 🔹 Step 1: Aggregate most active systems
    systems = (
        query
        .with_entities(
            LogEntry.service_name.label("service"),
            func.count(LogEntry.log_id).label("log_count")
        )
        .filter(LogEntry.service_name.isnot(None))
        .group_by(LogEntry.service_name)
        .order_by(func.count(LogEntry.log_id).desc())
        .limit(5)
        .all()
    )

    response = []

    # 🔹 Step 2: Fetch recent logs per system
    for sys in systems:
        recent_logs = (
            db.query(
                LogEntry.log_timestamp,
                LogSeverity.severity_code,
                LogEntry.message
            )
            .join(LogSeverity, LogEntry.severity_id == LogSeverity.severity_id)
            .filter(LogEntry.service_name == sys.service)
            .order_by(LogEntry.log_timestamp.desc())
            .limit(5)
            .all()
        )

        response.append({
            "service_name": sys.service,
            "log_count": sys.log_count,
            "recent_logs": [
                {
                    "timestamp": log.log_timestamp,
                    "severity": log.severity_code,
                    "message": log.message
                }
                for log in recent_logs
            ]
        })

    # ✅ RETURN ARRAY (CRITICAL FIX)
    return response



# ---------------------------------------------------------
# 4️⃣ Logs By Category (APPLICATION, SECURITY, etc.)
# ---------------------------------------------------------
@router.get("/logs-by-category")
def logs_by_category(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    results = (
        db.query(
            LogCategory.category_name,
            func.count(LogEntry.log_id).label("count")
        )
        .join(LogEntry, LogEntry.category_id == LogCategory.category_id)
        .group_by(LogCategory.category_name)
        .order_by(func.count(LogEntry.log_id).desc())
        .all()
    )

    return [
        {
            "category": row.category_name,
            "count": row.count
        }
        for row in results
    ]

# ---------------------------------------------------------
# 5️⃣ Logs By Severity (ALL severities)
# ---------------------------------------------------------
@router.get("/logs-by-severity")
def logs_by_severity(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    results = (
        db.query(
            LogSeverity.severity_code,
            func.count(LogEntry.log_id).label("count")
        )
        .join(LogEntry, LogEntry.severity_id == LogSeverity.severity_id)
        .group_by(LogSeverity.severity_code)
        .order_by(func.count(LogEntry.log_id).desc())
        .all()
    )

    return [
        {
            "severity": row.severity_code,
            "count": row.count
        }
        for row in results
    ]

# ---------------------------------------------------------
# 6️⃣ Files Uploaded Per Day
# ---------------------------------------------------------
@router.get("/files-per-day")
def files_uploaded_per_day(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    results = (
        db.query(
            cast(RawFile.uploaded_at, Date).label("upload_date"),
            func.count(RawFile.file_id).label("files_uploaded")
        )
        .group_by("upload_date")
        .order_by("upload_date DESC")
        .limit(30)
        .all()
    )

    return [
        {
            "upload_date": row.upload_date,
            "files_uploaded": row.files_uploaded
        }
        for row in results
    ]


@router.get("/recent-logs")
def fetch_recent_logs(
    days: int = Query(10, ge=1, le=30),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=50),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    cutoff = datetime.utcnow() - timedelta(days=days)
    offset = (page - 1) * limit

    logs = (
        db.query(
            LogEntry.log_timestamp,
            LogSeverity.severity_code,
            LogEntry.service_name,
            LogEntry.message
        )
        .join(LogSeverity, LogEntry.severity_id == LogSeverity.severity_id)
        .filter(LogEntry.log_timestamp >= cutoff)
        .order_by(LogEntry.log_timestamp.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "page": page,
        "limit": limit,
        "days": days,
        "results": [
            {
                "timestamp": row.log_timestamp,
                "severity": row.severity_code,
                "service": row.service_name,
                "message": row.message
            }
            for row in logs
        ]
    }
