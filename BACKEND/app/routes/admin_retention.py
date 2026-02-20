from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user
from app.services.log_retention_service import archive_files_by_retention

# This router handles everything related to retention management
router = APIRouter(prefix="/admin/retention", tags=["Retention"])


# Simple role check to make sure only admins can trigger retention jobs
def require_admin(user):
    if "ADMIN" not in user.get("roles", []):
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )


# This endpoint allows an admin to manually run the retention policy
# It archives files that exceed the configured retention period
@router.post("/archive-now") # Run the retention logic (moves eligible files to archive)
def archive_now(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
   
    require_admin(current_user)

    # Run the retention logic (moves eligible files to archive)
    count = archive_files_by_retention(db)

    # Return how many files were archived in this run
    return {
        "message": "Retention job executed successfully",
        "archived_files": count
    }