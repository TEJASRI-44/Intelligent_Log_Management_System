from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.team_upload_policies import TeamUploadPolicy
from app.models.log_sources import LogSource
from app.models.file_formats import FileFormat

router = APIRouter(prefix="/lookups", tags=["Lookups"])


@router.get("/team/{team_id}/sources")
def get_allowed_sources(team_id: int, db: Session = Depends(get_db)):
    sources = (
        db.query(LogSource.source_id, LogSource.source_name)
        .join(TeamUploadPolicy, TeamUploadPolicy.source_id == LogSource.source_id)
        .filter(
            TeamUploadPolicy.team_id == team_id,
            TeamUploadPolicy.is_allowed == True
        )
        .distinct()
        .all()
    )

    return [
        {"source_id": s.source_id, "source_name": s.source_name}
        for s in sources
    ]


@router.get("/team/{team_id}/source/{source_id}/formats")
def get_allowed_formats(
    team_id: int,
    source_id: int,
    db: Session = Depends(get_db)
):
    formats = (
        db.query(FileFormat.format_id, FileFormat.format_name)
        .join(TeamUploadPolicy, TeamUploadPolicy.format_id == FileFormat.format_id)
        .filter(
            TeamUploadPolicy.team_id == team_id,
            TeamUploadPolicy.source_id == source_id,
            TeamUploadPolicy.is_allowed == True
        )
        .distinct()
        .all()
    )

    return [
        {"format_id": f.format_id, "format_name": f.format_name}
        for f in formats
    ]
