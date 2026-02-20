import io
import os
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import datetime
from dotenv import load_dotenv
from app.models.upload_statuses import UploadStatus
from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.raw_files import RawFile
from app.models.user import User
from app.models.teams import Team
from app.models.audit_trail import AuditTrail
from app.appwrite_client import get_appwrite_storage

load_dotenv()

# Router for Admin File Management APIs
router = APIRouter(prefix="/admin/files", tags=["Admin Files"])


# Ensure only ADMIN users can access these APIs
def require_admin(user):
    if "ADMIN" not in user.get("roles", []):
        raise HTTPException(status_code=403, detail="Admin access required")


# List all files with filters and pagination
@router.get("")
def list_all_files(
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
    name: str | None = Query(None),
    team_id: int | None = Query(None),
    status: str | None = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    # Base query with joins
    query = (
        db.query(RawFile)
        .join(User, RawFile.uploaded_by == User.user_id)
        .join(Team, RawFile.team_id == Team.team_id)
        .join(UploadStatus, RawFile.status_id == UploadStatus.status_id)
    )

    # Apply optional filters
    if start_date:
        query = query.filter(RawFile.uploaded_at >= start_date)
    if end_date:
        query = query.filter(RawFile.uploaded_at <= end_date)
    if name:
        query = query.filter(RawFile.original_name.ilike(f"%{name}%"))
    if team_id:
        query = query.filter(RawFile.team_id == team_id)
    if status:
        query = query.filter(UploadStatus.status_code == status)

    total = query.count()  # Total matching records

    files = (
        query
        .order_by(RawFile.uploaded_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    # Return paginated file list
    return {
        "count": total,
        "results": [
            {
                "file_id": f.file_id,
                "name": f.original_name,
                "uploaded_at": f.uploaded_at,
                "file_size": f.file_size_bytes,
                "uploaded_by": f.user.username,
                "team": f.team.team_name,
                "is_deleted": f.is_deleted,
                "status": f.status.status_code if f.status else "UNKNOWN",
                "parsed_percentage": f.parsed_percentage
            }
            for f in files
        ]
    }


# Soft delete a file
@router.delete("/{file_id}")
def admin_delete_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    file = (
        db.query(RawFile)
        .filter(RawFile.file_id == file_id, RawFile.is_deleted == False)
        .first()
    )

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    file.is_deleted = True  # Soft delete

    # Log action in audit trail
    db.add(AuditTrail(
        user_id=int(current_user["sub"]),
        action_type="SOFT DELETED FILE",
        entity_type="RAW FILE",
        entity_id=file_id
    ))

    db.commit()

    return {"message": "File deleted successfully"}


# Restore a soft-deleted file
@router.post("/{file_id}/restore")
def restore_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    file = db.query(RawFile).filter(RawFile.file_id == file_id).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    file.is_deleted = False  # Restore file

    # Log restore action
    db.add(AuditTrail(
        user_id=int(current_user["sub"]),
        action_type="RESTORED FILE",
        entity_type="RAW FILE",
        entity_id=file_id
    ))

    db.commit()

    return {"message": "File restored successfully"}


# Download file from Appwrite storage
@router.get("/{file_id}/download")
def admin_download_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    file = db.query(RawFile).filter(RawFile.file_id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    try:
        storage = get_appwrite_storage()

        # Fetch file bytes using stored Appwrite file ID
        file_bytes = storage.get_file_download(
            bucket_id=os.getenv("APPWRITE_BUCKET_ID"),
            file_id=file.storage_path
        )

        # Stream file to client
        return StreamingResponse(
            io.BytesIO(file_bytes),
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f"attachment; filename={file.original_name}"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")