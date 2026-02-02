from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from typing import List

class UserProfileResponse(BaseModel):
    user_id: int
    email: str
    username: Optional[str]

    is_active: bool
    created_at: datetime

    first_name: str
    last_name: Optional[str]
    phone_number: Optional[str]
    job_title: Optional[str]
    profile_image_url: Optional[str]

    class Config:
        from_attributes = True


class UserProfileUpdateRequest(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    phone_number: Optional[str] = Field(None, max_length=20)


class UserAccessUpdate(BaseModel):
    role_ids: List[int]
    team_ids: List[int]


class UserStatusUpdate(BaseModel):
    is_active: bool
