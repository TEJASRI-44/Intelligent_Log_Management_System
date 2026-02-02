import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import SessionLocal
from app.appwrite_client import get_appwrite_storage

from app.models.raw_files import RawFile
from app.models.log_entries import LogEntry
from app.models.upload_statuses import UploadStatus
from app.models.archives import Archive
from app.models.audit_trail import AuditTrail


RETENTION_DAYS = 90
ARCHIVE_BASE_DIR = "archivals"
SYSTEM_USER_ID = None  # automated job


def archive_files_by_retention(db: Session):
    cutoff_date = datetime.utcnow() - timedelta(days=RETENTION_DAYS)

    # Fetch ARCHIVED status
    archived_status = db.query(UploadStatus).filter(
        UploadStatus.status_code == "ARCHIVED"
    ).first()

    if not archived_status:
        raise Exception("ARCHIVED status not found")

    # Find files eligible for archival
    eligible_files = (
        db.query(
            RawFile.file_id,
            func.count(LogEntry.log_id).label("total_records")
        )
        .join(LogEntry, LogEntry.file_id == RawFile.file_id)
        .filter(
            RawFile.is_deleted == False,
            RawFile.status_id != archived_status.status_id
        )
        .group_by(RawFile.file_id)
        .having(func.max(LogEntry.log_timestamp) < cutoff_date)
        .all()
    )

    storage = get_appwrite_storage()
    archived_count = 0

    for file_id, total_records in eligible_files:
        raw_file = db.query(RawFile).filter(
            RawFile.file_id == file_id
        ).first()

        if not raw_file:
            continue

       
        db.add(Archive(
            file_id=file_id,
            total_records=total_records
        ))

        try:
            file_bytes = storage.get_file_download(
                bucket_id=os.getenv("APPWRITE_BUCKET_ID"),
                file_id=raw_file.storage_path
            )
        except Exception as e:
            print(f" Failed to download from Appwrite: {e}")
            continue

        team_dir = os.path.join(ARCHIVE_BASE_DIR, str("team_"+raw_file.team_id))
        os.makedirs(team_dir, exist_ok=True)

        archived_file_path = os.path.join(
            team_dir,
            raw_file.original_name
        )

        with open(archived_file_path, "wb") as f:
            f.write(file_bytes)


        try:
            storage.delete_file(
                bucket_id=os.getenv("APPWRITE_BUCKET_ID"),
                file_id=raw_file.storage_path
            )
        except Exception as e:
            print(f" Appwrite delete failed: {e}")

        raw_file.storage_path = archived_file_path
        raw_file.status_id = archived_status.status_id


        db.add(AuditTrail(
            user_id=SYSTEM_USER_ID,
            action_type="ARCHIVE_FILE",
            entity_type="RAW_FILE",
            entity_id=file_id
        ))

        archived_count += 1
        print(f"Archived file_id={file_id}")

    db.commit()
    return archived_count
