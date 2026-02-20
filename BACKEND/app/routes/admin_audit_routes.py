# app/routes/admin_audit_routes.py

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.audit_trail import AuditTrail
from app.models.user import User
from app.core.dependencies import get_current_user

# Router for Admin Audit APIs
router = APIRouter(
    prefix="/admin/audits",
    tags=["Admin Audits"]
)

# Check if current user has ADMIN role
def require_admin(user):
    if "ADMIN" not in user.get("roles", []):
        raise HTTPException(status_code=403, detail="Admin access required")


# Get audit logs with pagination and optional filters
@router.get("")
def get_audit_logs(
    page: int = Query(1, ge=1),        # Page number
    limit: int = Query(10, le=50),     # Records per page (max 50)
    action_type: str | None = Query(None),
    entity_type: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)  # Restrict access to admins

    # Base query with join to fetch username
    query = (
        db.query(
            AuditTrail.audit_id,
            AuditTrail.action_time,
            AuditTrail.action_type,
            AuditTrail.entity_type,
            AuditTrail.entity_id,
            User.username
        )
        .outerjoin(User, User.user_id == AuditTrail.user_id)
        .order_by(AuditTrail.action_time.desc())
    )

    # Apply filters if provided
    if action_type:
        query = query.filter(AuditTrail.action_type == action_type)

    if entity_type:
        query = query.filter(AuditTrail.entity_type == entity_type)

    total = query.count()  # Total matching records

    rows = (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    # Return paginated response
    return {
        "count": total,
        "results": [
            {
                "time": r.action_time,
                "username": r.username or "System",
                "action": r.action_type,
                "entity_type": r.entity_type,
                "entity_id": r.entity_id
            }
            for r in rows
        ]
    }