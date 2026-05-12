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

class SimplePromptReqSchema(BaseModel):
    prompt: str

class OTPReqSchema(BaseModel):
    otp: str

class OTPEmailReqSchema(BaseModel):
    email: EmailStr
    otp: str

class ResetPassSchema(BaseModel):
    new_password: str
    conform_password: str

class ChatReqSchema(BaseModel):
    id: str

class EmbeedReqSchema(BaseModel):
    id: str
    path: str

class QueryReqSchema(BaseModel):
    id: str
    query: str

class EditQueryReqSchema(QueryReqSchema):
    chat_id: str

