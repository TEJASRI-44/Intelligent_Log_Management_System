from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.log_sources import LogSource

# Router to fetch available log sources
router = APIRouter(
    prefix="/log-sources",
    tags=["Log Sources"]
)

@router.get("/")
def get_log_sources(db: Session = Depends(get_db)):
    # Fetch all log sources from database
    sources = db.query(LogSource).all()

    # Return only required fields
    return [
        {
            "source_id": s.source_id,
            "source_name": s.source_name
        }
        for s in sources
    ]