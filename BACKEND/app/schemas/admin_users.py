from pydantic import BaseModel, Field
from typing import Optional


class AdminUserProfileUpdateRequest(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    job_title: Optional[str] = Field(None, max_length=100)

    class Config:
        orm_mode = True


class AdminUserProfileUpdateResponse(BaseModel):
    message: str
from typing import List


class AdminUserAccessUpdateRequest(BaseModel):
    role_ids: List[int] = []
    team_ids: List[int] = []

    class Config:
        orm_mode = True


class AdminUserAccessUpdateResponse(BaseModel):
    message: str
