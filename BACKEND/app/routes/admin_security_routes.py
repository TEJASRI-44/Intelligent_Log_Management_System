# app/routes/admin_security_routes.py
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.login_history import LoginHistory
from app.models.user import User
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix="/admin/security",
    tags=["Admin Security"]
)


def require_admin(user):
    if "ADMIN" not in user.get("roles", []):
        raise HTTPException(status_code=403, detail="Admin access required")


@router.get("/login-history")
def get_login_history(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=50),
    success: bool | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    query = (
        db.query(
            LoginHistory.login_id,
            LoginHistory.login_time,
            LoginHistory.login_ip,
            LoginHistory.user_agent,
            LoginHistory.success,
            LoginHistory.failure_reason,
            User.username
        )
        .outerjoin(User, User.user_id == LoginHistory.user_id)
        .order_by(LoginHistory.login_time.desc())
    )

    if success is not None:
        query = query.filter(LoginHistory.success == success)

    total = query.count()

    records = (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "count": total,
        "results": [
            {
                "login_time": r.login_time,
                "username": r.username,
                "ip": str(r.login_ip) if r.login_ip else None,
                "user_agent": r.user_agent,
                "success": r.success,
                "failure_reason": r.failure_reason
            }
            for r in records
        ]
    }
