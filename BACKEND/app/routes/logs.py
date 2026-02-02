from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.dependencies import get_current_user
from app.models.raw_files import RawFile
from app.models.log_entries import LogEntry
from app.models.log_severities import LogSeverity

router = APIRouter(prefix="/logs", tags=["User Logs"])



