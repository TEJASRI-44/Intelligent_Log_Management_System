from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.roles import Role
from app.models.user_roles import UserRole
from app.models.teams import Team
from app.models.user_teams import UserTeam
from app.models.audit_trail import AuditTrail
from app.models.user_profiles import UserProfile
from app.schemas.user_profiles import UserProfileResponse
from app.schemas.user_profiles import UserProfileUpdateRequest
from app.schemas.user_profiles import UserStatusUpdate
router = APIRouter(
    prefix="/admin/users",
    tags=["Admin User Management"]
)


def require_admin(user):
    if "ADMIN" not in user.get("roles", []):
        raise HTTPException(status_code=403, detail="Admin access required")


# -------------------------------------------------
# GET ALL USERS (with roles & teams)
# -------------------------------------------------
@router.get("/")
def list_users(
    email: str | None = None,
    team_id: int | None = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    query = (
        db.query(User)
        .filter(
            User.is_deleted == False,
            User.user_id != int(current_user["sub"])  # hide current admin
        )
    )

    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))

    if team_id:
        query = (
            query
            .join(UserTeam, User.user_id == UserTeam.user_id)
            .filter(UserTeam.team_id == team_id)
        )

   
    total = query.count()

    users = (
        query
        .order_by(User.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    response = []

    for u in users:
        profile = u.profile

        role_rows = (
            db.query(Role.role_id, Role.role_name)
            .join(UserRole, UserRole.role_id == Role.role_id)
            .filter(UserRole.user_id == u.user_id)
            .all()
        )

        team_rows = (
            db.query(Team.team_id, Team.team_name)
            .join(UserTeam, UserTeam.team_id == Team.team_id)
            .filter(UserTeam.user_id == u.user_id)
            .all()
        )

        response.append({
            "user_id": u.user_id,
            "email": u.email,
            "username": u.username,
            "is_active": u.is_active,
            "created_at": u.created_at,

            "profile": {
                "first_name": profile.first_name if profile else "",
                "last_name": profile.last_name if profile else "",
                "phone_number": profile.phone_number if profile else "",
                "job_title": profile.job_title if profile else ""
            },

            "role_ids": [r.role_id for r in role_rows],
            "team_ids": [t.team_id for t in team_rows],

            "roles": [r.role_name for r in role_rows],
            "teams": [t.team_name for t in team_rows]
        })

    return {
        "results": response,
        "count": total
    }



from app.schemas.admin_users import (
    AdminUserProfileUpdateRequest,
    AdminUserProfileUpdateResponse
)

@router.put(
    "/{user_id}/profile",
    response_model=AdminUserProfileUpdateResponse
)
def update_user_profile(
    user_id: int,
    payload: AdminUserProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    user = (
        db.query(User)
        .filter(User.user_id == user_id, User.is_deleted == False)
        .first()
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.profile:
        user.profile = UserProfile(user_id=user_id)

    if payload.first_name is not None:
        user.profile.first_name = payload.first_name.strip()

    if payload.last_name is not None:
        user.profile.last_name = payload.last_name.strip()

    if payload.phone_number is not None:
        user.profile.phone_number = payload.phone_number.strip()

    if payload.job_title is not None:
        user.profile.job_title = payload.job_title.strip()

    db.add(AuditTrail(
        user_id=int(current_user["sub"]),
        action_type="UPDATE_USER_PROFILE",
        entity_type="USER",
        entity_id=user_id
    ))

    db.commit()
    return {"message": "User profile updated successfully"}


from app.schemas.admin_users import (
    AdminUserAccessUpdateRequest,
    AdminUserAccessUpdateResponse
)

@router.put(
    "/{user_id}/access",
    response_model=AdminUserAccessUpdateResponse
)
def update_user_access(
    user_id: int,
    payload: AdminUserAccessUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    db.query(UserRole).filter(UserRole.user_id == user_id).delete()
    db.query(UserTeam).filter(UserTeam.user_id == user_id).delete()

    for role_id in payload.role_ids:
        db.add(UserRole(user_id=user_id, role_id=role_id))

    for team_id in payload.team_ids:
        db.add(UserTeam(user_id=user_id, team_id=team_id))

    db.add(AuditTrail(
        user_id=int(current_user["sub"]),
        action_type="UPDATE_USER_ACCESS",
        entity_type="USER",
        entity_id=user_id
    ))

    db.commit()
    return {"message": "User roles and teams updated successfully"}

@router.patch("/{user_id}/status")
def update_user_status(
    user_id: int,
    payload: UserStatusUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    user.is_active = payload.is_active

    db.add(AuditTrail(
        user_id=int(current_user["sub"]),
        action_type="UPDATE_USER_STATUS",
        entity_type="USER",
        entity_id=user_id
    ))

    db.commit()
    return {"message": "User status updated"}

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    user.is_deleted = True
    user.is_active = False

    db.add(AuditTrail(
        user_id=int(current_user["sub"]),
        action_type="DELETE_USER",
        entity_type="USER",
        entity_id=user_id
    ))

    db.commit()
    return {"message": "User deleted"}
