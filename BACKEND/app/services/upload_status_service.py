from sqlalchemy.orm import Session
from app.models.upload_statuses import UploadStatus


def get_status_id(db: Session, status_code: str) -> int:
    status = (
        db.query(UploadStatus)
        .filter(UploadStatus.status_code == status_code)
        .first()
    )

    if not status:
        raise ValueError(f"Upload status '{status_code}' not found")

    return status.status_id
