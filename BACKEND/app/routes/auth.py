from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status,Request

from app.models.login_history import LoginHistory
from app.database import get_db
from app.models.user import User
from app.models.roles import Role
from app.models.user_roles import UserRole
from app.models.user_credentials import UserCredentials
from app.schemas.user import LoginRequest
from app.core.jwt_utils import create_access_token
from app.core.security import verify_password

router = APIRouter(
    prefix="/users",
    tags=["Authentication"]
)
@router.post("/login-json")
def login_user(
    payload: LoginRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    email = payload.email
    password = payload.password

    ip = request.client.host if request.client else None
    ua = request.headers.get("user-agent")

    now = datetime.now(timezone.utc)

    user = (
        db.query(User)
        .filter(
            User.email == email,
            User.is_active == True,
            User.is_deleted == False
        )
        .first()
    )

    if not user:
        db.add(LoginHistory(
            user_id=None,
            login_ip=ip,
            user_agent=ua,
            success=False,
            failure_reason="USER_NOT_FOUND"
        ))
        db.commit()
        raise HTTPException(status_code=401, detail="Invalid credentials")

    creds = (
        db.query(UserCredentials)
        .filter(UserCredentials.user_id == user.user_id)
        .first()
    )

    if not creds:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if creds.is_locked and creds.locked_until:
        if creds.locked_until > now:
            raise HTTPException(
                status_code=403,
                detail=f"Account locked. Try again after {creds.locked_until}"
            )
        else:
            # Auto unlock after time passed
            creds.is_locked = False
            creds.failed_attempts = 0
            creds.locked_until = None
            db.commit()

    if not verify_password(password, creds.password_hash):

        creds.failed_attempts = (creds.failed_attempts or 0) + 1
        creds.last_failed_at = now

        if creds.failed_attempts >= 3:
            creds.is_locked = True
            creds.locked_until = now + timedelta(minutes=10)

        db.add(LoginHistory(
            user_id=user.user_id,
            login_ip=ip,
            user_agent=ua,
            success=False,
            failure_reason="INVALID_PASSWORD"
        ))

        db.commit()

        raise HTTPException(status_code=401, detail="Invalid credentials")


    creds.failed_attempts = 0
    creds.is_locked = False
    creds.locked_until = None

    roles = (
        db.query(Role.role_name)
        .join(UserRole, UserRole.role_id == Role.role_id)
        .filter(UserRole.user_id == user.user_id)
        .all()
    )

    role_names = [r.role_name for r in roles]

    db.add(LoginHistory(
        user_id=user.user_id,
        login_ip=ip,
        user_agent=ua,
        success=True,
        failure_reason=None
    ))

    db.commit()

    access_token = create_access_token({
        "sub": str(user.user_id),
        "email": user.email,
        "roles": role_names
    })

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": role_names[0] if role_names else None
    }
