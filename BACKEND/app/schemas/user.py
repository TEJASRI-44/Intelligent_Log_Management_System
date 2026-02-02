from pydantic import BaseModel, EmailStr
from typing import List

class AdminCreateUserRequest(BaseModel):
    email: EmailStr
    username: str
    password: str

    first_name: str
    last_name: str | None = None
    phone_number: str | None = None
    job_title: str | None = None

    role_ids: List[int]
    team_ids: List[int]


class LoginRequest(BaseModel):
    email: EmailStr
    password: str