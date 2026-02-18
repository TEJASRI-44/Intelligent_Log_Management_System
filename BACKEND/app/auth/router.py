""" from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.schemas import LoginRequest, TokenResponse
from app.auth.service import authenticate_user

router = APIRouter(prefix="/users", tags=["Auth"])


@router.post("/login-json", response_model=TokenResponse)
def login_json(
    payload: LoginRequest,
    db: Session = Depends(get_db)
):
    token = authenticate_user(db, payload.email, payload.password)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": token,
        "token_type": "bearer"
    }
 """