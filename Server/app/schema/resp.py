from pydantic import BaseModel
from datetime import datetime

class LoginResp(BaseModel):
    message: str
    name: str
    email: str
    is_verified: bool
    credits_token: int

    class Config:
        from_attributes = True

class CheckEmailAvilableResp(BaseModel):
    message: str
    success: bool
    class Config:
        from_attributes = True

class NewTaskResp(BaseModel):
    message: str
    task_id: int
    title: str
    updated_at: datetime

    class Config:
        from_attributes = True