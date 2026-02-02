from pydantic import BaseModel, Field

class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)
    
class AdminResetPasswordRequest(BaseModel):
    new_password: str = Field(..., min_length=8)
