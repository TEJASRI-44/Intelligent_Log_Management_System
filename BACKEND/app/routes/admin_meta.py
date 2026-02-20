from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.roles import Role
from app.models.teams import Team

# Router for Admin metadata APIs (roles & teams)
router = APIRouter(prefix="/admin", tags=["Admin Meta"])


# Fetch all available roles
@router.get("/roles")
def fetch_roles(db: Session = Depends(get_db)):
    return db.query(Role).all()


# Fetch all available teams
@router.get("/teams")
def fetch_teams(db: Session = Depends(get_db)):
    return db.query(Team).all()