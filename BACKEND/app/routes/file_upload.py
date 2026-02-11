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
def upload_log_file(
    team_id: int,
    source_id: int,
    format_id: int,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
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

   
    content = file.file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    checksum = hashlib.sha256(content).hexdigest()

    if db.query(RawFile).filter(RawFile.checksum == checksum).first():
        raise HTTPException(status_code=409, detail="Duplicate file")

  
    """ team_dir = os.path.join(BASE_UPLOAD_DIR, str(team_id))
    os.makedirs(team_dir, exist_ok=True)

    file_uuid = str(uuid.uuid4())
    stored_filename = f"{file_uuid}_{file.filename}"
    file_path = os.path.join(team_dir, stored_filename)

    with open(file_path, "wb") as f:
        f.write(content)
    # -------------------- """

        
    storage = get_appwrite_storage()
    file.file.seek(0)

    try:
        uploaded = storage.create_file(
            bucket_id=os.getenv("APPWRITE_BUCKET_ID"),
            file_id="unique()",
            file=InputFile.from_bytes(content, file.filename)
        )
    except AppwriteException as e:
        print(" Appwrite upload failed")
        print("Status:", e.code)
        print("Message:", e.message)
        raise HTTPException(
            status_code=500,
            detail=f"Appwrite upload failed: {e.message}"
        )
    except Exception as e:
        print("Unknown upload error:", str(e))
        raise

   
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

   
    background_tasks.add_task(
        process_uploaded_file,
        raw_file.file_id
    )

    return {
        "message": "File uploaded successfully. Log processing started.",
        "file_id": raw_file.file_id
    }
