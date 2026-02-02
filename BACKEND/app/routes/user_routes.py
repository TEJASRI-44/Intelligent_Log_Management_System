from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.audit_trail import AuditTrail
from app.database import get_db
from app.schemas.user import AdminCreateUserRequest, LoginRequest
from app.core.dependencies import get_current_user
from app.models.raw_files import RawFile
from app.models.log_entries import LogEntry
from app.models.log_severities import LogSeverity
from app.core.security import verify_password
from app.core.security import hash_password
from app.schemas.password import ChangePasswordRequest
from app.models.user_credentials import UserCredentials
from datetime import datetime
from fastapi import Query
import re

from app.services.user_service import (
    create_user_by_admin,
    get_all_users,
    login_user
)

from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.roles import Role
from app.models.teams import Team
from app.models.user_roles import UserRole
from app.models.user_teams import UserTeam
from app.models.user_profiles import UserProfile
from app.schemas.user_profiles import UserProfileResponse
from app.schemas.user_profiles import UserProfileUpdateRequest
router = APIRouter(prefix="/users", tags=["Users"])


# --------------------------------------------------
# 🔐 Helper: Require ADMIN role
# --------------------------------------------------
def require_admin(user):
    roles = user.get("roles", [])
    if "ADMIN" not in roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )


# --------------------------------------------------
# ➕ ADMIN CREATE USER
# --------------------------------------------------
@router.post("/create")
def admin_create_user(
    payload: AdminCreateUserRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    admin_id = int(current_user["sub"])

    user = create_user_by_admin(db, admin_id, payload)

    return {
        "message": "User created successfully",
        "user_id": user.user_id
    }


# --------------------------------------------------
# 👥 VIEW USERS (WITH ROLES & TEAMS + IDs)
# --------------------------------------------------
@router.get("/view")
def view_users(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    users = get_all_users(db)
    response = []

    for u in users:
        roles = (
            db.query(Role)
            .join(UserRole, Role.role_id == UserRole.role_id)
            .filter(UserRole.user_id == u.user_id)
            .all()
        )

        teams = (
            db.query(Team)
            .join(UserTeam, Team.team_id == UserTeam.team_id)
            .filter(UserTeam.user_id == u.user_id)
            .all()
        )

        response.append({
            "user_id": u.user_id,
            "email": u.email,
            "username": u.username,
            "is_active": u.is_active,
            "created_at": u.created_at,

            # ✅ Names for display
            "roles": [r.role_name for r in roles],
            "teams": [t.team_name for t in teams],

            # ✅ IDs for editing modal
            "role_ids": [r.role_id for r in roles],
            "team_ids": [t.team_id for t in teams],
        })

    return {
        "count": len(response),
        "users": response
    }

@router.get("/me", response_model=UserProfileResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = int(current_user["sub"])

    user = (
        db.query(User)
        .filter(User.user_id == user_id, User.is_deleted == False)
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == user_id)
        .first()
    )

    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    return {
        "user_id": user.user_id,
        "email": user.email,
        "username": user.username,
        "is_active": user.is_active,
        "created_at": user.created_at,

        "first_name": profile.first_name,
        "last_name": profile.last_name,
        "phone_number": profile.phone_number,
        "job_title": profile.job_title,
        "profile_image_url": profile.profile_image_url
    }




@router.put("/me", response_model=UserProfileResponse)
def update_my_profile(
    payload: UserProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = int(current_user["sub"])

    user = (
        db.query(User)
        .filter(User.user_id == user_id, User.is_deleted == False)
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == user_id)
        .first()
    )

    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")

   
    if payload.first_name is not None:
        profile.first_name = payload.first_name.strip()

    if payload.last_name is not None:
        profile.last_name = payload.last_name.strip()

    if payload.phone_number is not None:
        

        if payload.phone_number:
            if not re.match(r"^[0-9+\-\s]{7,20}$", payload.phone_number):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid phone number format"
                )

        profile.phone_number = payload.phone_number.strip()

    db.commit()
    db.refresh(profile)

    return {
        "user_id": user.user_id,
        "email": user.email,
        "username": user.username,
        "is_active": user.is_active,
        "created_at": user.created_at,

        "first_name": profile.first_name,
        "last_name": profile.last_name,
        "phone_number": profile.phone_number,
        "job_title": profile.job_title,
        "profile_image_url": profile.profile_image_url
    }
@router.put("/me/password")
def change_my_password(
    payload: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = int(current_user["sub"])

    creds = (
        db.query(UserCredentials)
        .filter(UserCredentials.user_id == user_id)
        .first()
    )

    if not creds:
        raise HTTPException(status_code=404, detail="Credentials not found")

    # ✅ Verify current password
    if not verify_password(payload.current_password, creds.password_hash):
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect"
        )

    # ✅ Prevent reuse
    if verify_password(payload.new_password, creds.password_hash):
        raise HTTPException(
            status_code=400,
            detail="New password must be different"
        )

    # ✅ Update password
    creds.password_hash = hash_password(payload.new_password)
    creds.password_changed_at = text("NOW()")
    creds.failed_attempts = 0
    creds.is_locked = False
    creds.locked_until = None

    # ✅ Audit
    db.add(AuditTrail(
        user_id=user_id,
        action_type="CHANGE_PASSWORD",
        entity_type="USER",
        entity_id=user_id
    ))

    db.commit()

    return {"message": "Password updated successfully"}

    
@router.get("/my-teams")
def get_my_teams(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    teams = (
        db.query(Team.team_id, Team.team_name)
        .join(UserTeam, UserTeam.team_id == Team.team_id)
        .filter(UserTeam.user_id == int(current_user["sub"]))
        .all()
    )

    return [
        {"team_id": t.team_id, "team_name": t.team_name}
        for t in teams
    ]

@router.get("/my-logs")
def get_my_logs(
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
    category: str | None = Query(None),
    severity: str | None = Query(None),
    keyword: str | None = Query(None),
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Fetch log entries ONLY from files uploaded by the current user
    (supports same filters as /logs/search)
    """

    user_id = int(current_user["sub"])

    query = (
        db.query(
            LogEntry.log_id.label("log_id"),
            LogEntry.log_timestamp.label("timestamp"),
            LogSeverity.severity_code.label("severity"),
            LogEntry.service_name.label("service"),
            LogEntry.message.label("message"),
        )
        .join(RawFile, RawFile.file_id == LogEntry.file_id)
        .join(LogSeverity, LogSeverity.severity_id == LogEntry.severity_id)
        .filter(
            RawFile.uploaded_by == user_id,
            RawFile.is_deleted == False,
            LogEntry.is_deleted == False
        )
    )

    # ===== APPLY FILTERS =====

    if start_date:
        query = query.filter(LogEntry.log_timestamp >= start_date)

    if end_date:
        query = query.filter(LogEntry.log_timestamp <= end_date)

    if category:
        query = query.filter(LogEntry.category == category)

    if severity:
        query = query.filter(LogSeverity.severity_code == severity)

    if keyword:
        query = query.filter(LogEntry.message.ilike(f"%{keyword}%"))

    total = query.count()

    logs = (
        query
        .order_by(LogEntry.log_timestamp.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "count": total,
        "results": [dict(log._mapping) for log in logs]
    }
