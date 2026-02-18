from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException,
    BackgroundTasks
)
from sqlalchemy.orm import Session
import os, uuid, hashlib
from typing import List


from app.database import get_db
from app.models.raw_files import RawFile
from app.services.upload_policy import is_upload_allowed
from app.services.log_background_processor import process_uploaded_file
from app.core.dependencies import get_current_user
from app.appwrite_client import get_appwrite_storage
from appwrite.input_file import InputFile
from appwrite.exception import AppwriteException

router = APIRouter(prefix="/files", tags=["File Upload"])

""" BASE_UPLOAD_DIR = "uploads" """


@router.post("/upload")
def upload_log_files(
    team_id: int,
    source_id: int,
    format_id: int,
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),  
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    user_id = int(current_user["sub"])

    if not is_upload_allowed(
        db=db,
        team_id=team_id,
        source_id=source_id,
        format_id=format_id
    ):
        raise HTTPException(status_code=403, detail="Upload not allowed")

    storage = get_appwrite_storage()

    uploaded_files = []
    skipped_files = []

    for file in files:

        content = file.file.read()

        if not content:
            skipped_files.append({
                "filename": file.filename,
                "reason": "Empty file"
            })
            continue

        checksum = hashlib.sha256(content).hexdigest()

        # Duplicate check
        if db.query(RawFile).filter(RawFile.checksum == checksum).first():
            skipped_files.append({
                "filename": file.filename,
                "reason": "Duplicate file"
            })
            continue

        try:
            uploaded = storage.create_file(
                bucket_id=os.getenv("APPWRITE_BUCKET_ID"),
                file_id="unique()",
                file=InputFile.from_bytes(content, file.filename)
            )
        except AppwriteException as e:
            skipped_files.append({
                "filename": file.filename,
                "reason": f"Upload failed: {e.message}"
            })
            continue

        raw_file = RawFile(
            team_id=team_id,
            uploaded_by=user_id,
            original_name=file.filename,
            file_size_bytes=len(content),
            checksum=checksum,
            format_id=format_id,
            source_id=source_id,
            storage_type_id=2,
            storage_path=uploaded["$id"],
            status_id=1
        )

        db.add(raw_file)
        db.commit()
        db.refresh(raw_file)

        # Background processing
        background_tasks.add_task(
            process_uploaded_file,
            raw_file.file_id
        )

        uploaded_files.append({
            "file_id": raw_file.file_id,
            "filename": file.filename
        })

    if not uploaded_files and not skipped_files:
        raise HTTPException(
            status_code=400,
            detail="No files were processed"
        )

    return {
        "message": "Upload completed",
        "uploaded_files": uploaded_files,
        "skipped_files": skipped_files
    }
