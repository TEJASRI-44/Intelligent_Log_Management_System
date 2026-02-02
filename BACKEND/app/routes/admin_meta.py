from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.roles import Role
from app.models.teams import Team

router = APIRouter(prefix="/admin", tags=["Admin Meta"])


@router.get("/roles")
def fetch_roles(db: Session = Depends(get_db)):
    return db.query(Role).all()


@router.get("/teams")
def fetch_teams(db: Session = Depends(get_db)):
    return db.query(Team).all()
