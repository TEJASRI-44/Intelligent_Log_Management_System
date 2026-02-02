from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user
from app.services.log_retention_service import archive_files_by_retention
from app.routes.admin_users import require_admin

router = APIRouter(prefix="/admin/retention", tags=["Retention"])

def require_admin(user):
    if "ADMIN" not in user.get("roles", []):
        raise HTTPException(status_code=403, detail="Admin access required")
    
@router.post("/archive-now")
def archive_now(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    require_admin(current_user)

    count = archive_files_by_retention(db)
    return {
        "message": "Retention job executed successfully",
        "archived_files": count
    }
