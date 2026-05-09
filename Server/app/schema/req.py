from pydantic import BaseModel, EmailStr


class RegisterReqSchema(BaseModel):
    email: EmailStr
    name: str
    password: str
    conform_password: str


class LoginReqSchema(BaseModel):
    email: EmailStr
    password: str

class CheckMailReqSchema(BaseModel):
    email: EmailStr