from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user import User
from app.models.user_profiles import UserProfile
from app.models.user_credentials import UserCredentials
from app.models.user_roles import UserRole
from app.models.user_teams import UserTeam
from app.models.audit_trail import AuditTrail
from app.models.roles import Role

from app.core.security import hash_password, verify_password
from app.core.jwt_utils import create_access_token


# Admin creates a new user
def create_user_by_admin(db: Session, admin_id: int, payload):

    # Check if email already exists
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise ValueError("Email already exists")

    # Create basic user record
    user = User(
        email=payload.email,
        username=payload.username,
        is_active=True,
        is_deleted=False
    )
    db.add(user)
    db.flush()  # Get generated user_id before commit

    # Create user profile
    db.add(UserProfile(
        user_id=user.user_id,
        first_name=payload.first_name,
        last_name=payload.last_name,
        phone_number=payload.phone_number,
        job_title=payload.job_title
    ))

    # Store hashed password in credentials table
    db.add(UserCredentials(
        user_id=user.user_id,
        password_hash=hash_password(payload.password),
        password_algo="bcrypt"
    ))

    # Assign roles
    for role_id in payload.role_ids:
        db.add(UserRole(user_id=user.user_id, role_id=role_id))

    # Assign teams
    for team_id in payload.team_ids:
        db.add(UserTeam(user_id=user.user_id, team_id=team_id))

    # Log this action in audit trail
    db.add(AuditTrail(
        user_id=admin_id,
        action_type="CREATED USER",
        entity_type="USER",
        entity_id=user.user_id
    ))

    db.commit()
    return user


# Fetch all non-deleted users
def get_all_users(db: Session):
    return db.query(User).filter(User.is_deleted == False).all()


# Login using JSON payload (email + password)
def login_user(db: Session, payload):

    # Check if user exists and is active
    user = db.query(User).filter(
        User.email == payload.email,
        User.is_active == True,
        User.is_deleted == False
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Fetch user credentials
    creds = db.query(UserCredentials).filter(
        UserCredentials.user_id == user.user_id
    ).first()

    # Verify password
    if not creds or not verify_password(payload.password, creds.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Fetch roles assigned to user
    roles = (
        db.query(Role.role_name)
        .join(UserRole, Role.role_id == UserRole.role_id)
        .filter(UserRole.user_id == user.user_id)
        .all()
    )

    role_names = [r.role_name for r in roles]

    # Generate JWT token
    access_token = create_access_token({
        "sub": str(user.user_id),
        "email": user.email,
        "roles": role_names
    })

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": role_names[0] if role_names else "USER"
    }


# Login using form data (username/email + password)
def login_user_form(db: Session, form_data: OAuth2PasswordRequestForm):

    # Allow login using either email or username
    user = db.query(User).filter(
        and_(
            or_(
                User.email == form_data.username,
                User.username == form_data.username
            ),
            User.is_active == True,
            User.is_deleted == False
        )
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Fetch credentials
    creds = db.query(UserCredentials).filter(
        UserCredentials.user_id == user.user_id
    ).first()

    # Verify password
    if not creds or not verify_password(form_data.password, creds.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Fetch user roles
    roles = (
        db.query(Role.role_name)
        .join(UserRole, Role.role_id == UserRole.role_id)
        .filter(UserRole.user_id == user.user_id)
        .all()
    )

    role_names = [r.role_name for r in roles]

    # Generate JWT token
    access_token = create_access_token({
        "sub": str(user.user_id),
        "email": user.email,
        "roles": role_names
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }