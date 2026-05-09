from pydantic import BaseModel


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