import os
from fastapi import APIRouter, Depends, HTTPException, Query,status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.models.teams import Team
from app.appwrite_client import get_appwrite_storage
from app.models.log_entries import LogEntry
from app.database import get_db
from app.core.dependencies import get_current_user

from app.models.raw_files import RawFile
from app.models.file_formats import FileFormat
from app.models.log_sources import LogSource
from app.models.upload_statuses import UploadStatus
from app.models.audit_trail import AuditTrail

router = APIRouter(
    prefix="/users/files",
    tags=["User Files"]
)
def require_admin(user):
    roles = user.get("roles", [])
    if "ADMIN" not in roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
import os

UPLOAD_DIR = "uploads"  

@router.delete("/{file_id}")
def delete_uploaded_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user_id = int(current_user["sub"])

    raw_file = (
        db.query(RawFile)
        .filter(
            RawFile.file_id == file_id,
            RawFile.is_deleted == False
        )
        .first()
    )

    if not raw_file:
        raise HTTPException(status_code=404, detail="File not found")

    if raw_file.uploaded_by != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")


    """ file_path = raw_file.storage_path
    if not file_path.startswith(UPLOAD_DIR):
        file_path = os.path.join(UPLOAD_DIR, file_path)

    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        
        print(f"[WARN] File not found on disk: {file_path}") """

    raw_file.is_deleted = True

    db.query(LogEntry).filter(
        LogEntry.file_id == file_id
    ).update({"is_deleted": True})

    audit = AuditTrail(
        user_id=user_id,
        action_type="DELETED FILE",
        entity_type="RAW FILE",
        entity_id=file_id
    )

    db.add(audit)
    db.commit()

    return {"message": "File deleted successfully"}

@router.get("/my-files")
def my_uploaded_files(
    page: int = 1,
    limit: int = 10,
    team_id: int | None = None,
    name: str | None = None,
    status: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = int(current_user["sub"])

    query = (
        db.query(
            RawFile.file_id,
            RawFile.original_name,
            RawFile.uploaded_at,
            RawFile.file_size_bytes,
            RawFile.is_deleted,
            RawFile.parsed_percentage,
            Team.team_name,
            UploadStatus.status_code
        )
        .join(Team, Team.team_id == RawFile.team_id)
        .join(UploadStatus, UploadStatus.status_id == RawFile.status_id)
        .filter(RawFile.uploaded_by == user_id)
    )

    if team_id:
        query = query.filter(RawFile.team_id == team_id)

    if name:
        query = query.filter(RawFile.original_name.ilike(f"%{name}%"))

    if status:
        query = query.filter(UploadStatus.status_code == status)

    total = query.count()

    files = (
        query
        .order_by(RawFile.uploaded_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    print("MY FILES RAW RESULT:", files)

    return {
        "results": [
            {
                "file_id": f.file_id,
                "name": f.original_name,
                "uploaded_at": f.uploaded_at,
                "file_size": f.file_size_bytes,
                "team": f.team_name,
                "status": f.status_code,
                "parsed_percentage":f.parsed_percentage,    
                "is_deleted": f.is_deleted
            }
            for f in files
        ],
        "count": total
    }

@router.patch("/{file_id}/restore")
def restore_uploaded_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user_id = int(current_user["sub"])

    raw_file = (
        db.query(RawFile)
        .filter(
            RawFile.file_id == file_id,
            RawFile.is_deleted == True
        )
        .first()
    )

    if not raw_file:
        raise HTTPException(status_code=404, detail="Deleted file not found")

    if raw_file.uploaded_by != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

   
    raw_file.is_deleted = False

    db.query(LogEntry).filter(
        LogEntry.file_id == file_id
    ).update({"is_deleted": False})

    audit = AuditTrail(
        user_id=user_id,
        action_type="RESTORE_FILE",
        entity_type="RAW_FILE",
        entity_id=file_id
    )

    db.add(audit)
    db.commit()

    return {"message": "File restored successfully"}

@router.get("/{file_id}/download")
def admin_download_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    file = db.query(RawFile).filter(RawFile.file_id == file_id).first()
    if not file:
        raise HTTPException(404, "File not found")

    return FileResponse(
        path=file.storage_path,     # adjust if different
        filename=file.original_name,
        media_type="application/octet-stream"
    )
