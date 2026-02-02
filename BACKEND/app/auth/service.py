from sqlalchemy.orm import Session

from app.models.user import User
from app.models.user_credentials import UserCredentials
from app.core.security import verify_password
from app.core.jwt_utils import create_access_token


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(
        User.email == email,
        User.is_active == True,
        User.is_deleted == False
    ).first()

    if not user:
        return None

    creds = db.query(UserCredentials).filter(
        UserCredentials.user_id == user.user_id
    ).first()

    if not creds:
        return None

    if not verify_password(password, creds.password_hash):
        return None

    return create_access_token(user.user_id)
