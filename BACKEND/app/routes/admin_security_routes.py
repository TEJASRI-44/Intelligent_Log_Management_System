# app/routes/admin_security_routes.py
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.login_history import LoginHistory
from app.models.user import User
from app.core.dependencies import get_current_user

# Router for admin security related APIs
router = APIRouter(
    prefix="/admin/security",
    tags=["Admin Security"]
)


# Simple function to check whether the user is ADMIN
def require_admin(user):
    if "ADMIN" not in user.get("roles", []):
        raise HTTPException(status_code=403, detail="Admin access required")


@router.get("/login-history")
def get_login_history(
    page: int = Query(1, ge=1),      # Page number
    limit: int = Query(10, le=50),   # Number of records per page
    success: bool | None = Query(None),  # Optional filter for success/failure
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Only admins should access login history
    require_admin(current_user)

    # Base query with join to fetch username
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
        .order_by(LoginHistory.login_time.desc())  # Latest logins first
    )

    # Apply success filter if provided
    if success is not None:
        query = query.filter(LoginHistory.success == success)

    total = query.count()  # Total matching records

    records = (
        query
        .offset((page - 1) * limit)  # Pagination offset
        .limit(limit)
        .all()
    )

    # Return paginated login history
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