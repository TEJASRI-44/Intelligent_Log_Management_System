# Force SQLAlchemy to register ALL models

from app.models.user import User
from app.models.user_profiles import UserProfile
from app.models.user_credentials import UserCredentials
from app.models.roles import Role
from app.models.user_roles import UserRole
from app.models.teams import Team
from app.models.user_teams import UserTeam
from app.models.team_upload_policies import TeamUploadPolicy
from app.models.log_sources import LogSource
from app.models.file_formats import FileFormat
from app.models.storage_types import StorageType
from app.models.upload_statuses import UploadStatus

from app.models.raw_files import RawFile
from app.models.log_entries import LogEntry

# audit / history tables – no relationships needed
from .environments import Environment  