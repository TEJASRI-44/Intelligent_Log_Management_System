from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.file_formats import FileFormat

# Router for fetching supported file formats
router = APIRouter(
    prefix="/file-formats",
    tags=["File Formats"]
)

@router.get("/")
def get_file_formats(db: Session = Depends(get_db)):
    # Fetch all available file formats from database
    formats = db.query(FileFormat).all()

    # Return only required fields in response
    return [
        {
            "format_id": f.format_id,
            "format_name": f.format_name
        }
        for f in formats
    ]