from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.teams import Team

router = APIRouter(
    prefix="/teams",
    tags=["Teams"]
)

@router.get("/")
def get_teams(db: Session = Depends(get_db)):
    teams = db.query(Team).all()

    return [
        {
            "team_id": t.team_id,
            "team_name": t.team_name
        }
        for t in teams
    ]
