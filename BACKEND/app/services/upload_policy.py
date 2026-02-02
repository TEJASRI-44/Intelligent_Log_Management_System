from sqlalchemy.orm import Session
from app.models.team_upload_policies import TeamUploadPolicy

def is_upload_allowed(
    db: Session,
    team_id: int,
    source_id: int,
    format_id: int
) -> bool:
    policy = db.query(TeamUploadPolicy).filter(
        TeamUploadPolicy.team_id == team_id,
        TeamUploadPolicy.source_id == source_id,
        TeamUploadPolicy.format_id == format_id,
        TeamUploadPolicy.is_allowed == True
    ).first()

    return policy is not None
