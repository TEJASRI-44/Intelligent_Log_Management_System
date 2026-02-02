from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.upload_statuses import UploadStatus
from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.raw_files import RawFile
from app.models.user import User
from app.models.teams import Team
from app.models.audit_trail import AuditTrail

router = APIRouter(prefix="/admin/files", tags=["Admin Files"])


def require_admin(user):
    if "ADMIN" not in user.get("roles", []):
        raise HTTPException(status_code=403, detail="Admin access required")


@router.get("")
def list_all_files(
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
    name: str | None = Query(None),
    team_id: int | None = Query(None),
    status: str | None = Query(None),
    page: int = Query(1, ge=1),          # ✅
    limit: int = Query(10, le=100),      # ✅
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    query = (
    db.query(RawFile)
    .join(User, RawFile.uploaded_by == User.user_id)
    .join(Team, RawFile.team_id == Team.team_id)
    .join(UploadStatus, RawFile.status_id == UploadStatus.status_id)
)



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




    total = query.count()   # ✅ total rows

    files = (
        query
        .order_by(RawFile.uploaded_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )
    print("=== ADMIN FILES DEBUG ===")
    for f in files:
        print(
            f"file_id={f.file_id}, "
            f"name={f.original_name}, "
            f"status={f.status.status_code if f.status else 'UNKNOWN'}, "
            f"is_deleted={f.is_deleted}"
        )
    print("=========================")
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
                "status": f.status.status_code if f.status else "UNKNOWN"
            }
            for f in files
        ]
    }


@router.delete("/{file_id}")
def admin_delete_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    file = (
        db.query(RawFile)
        .filter(
            RawFile.file_id == file_id,
            RawFile.is_deleted == False
        )
        .first()
    )

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    # ✅ SOFT DELETE
    file.is_deleted = True

    db.add(AuditTrail(
        user_id=int(current_user["sub"]),
        action_type="SOFT_DELETE_FILE",
        entity_type="RAW_FILE",
        entity_id=file_id
    ))

    db.commit()

    return {"message": "File deleted successfully"}

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

    file.is_deleted = False

    db.add(AuditTrail(
        user_id=int(current_user["sub"]),
        action_type="RESTORE_FILE",
        entity_type="RAW_FILE",
        entity_id=file_id
    ))

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
