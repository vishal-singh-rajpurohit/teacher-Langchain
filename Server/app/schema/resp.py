from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class LoginResp(BaseModel):
    message: str
    name: str
    email: str
    is_verified: bool
    credits_token: int
    tasks: List[TasksResp]
    class Config:
        from_attributes = True

class CheckEmailAvilableResp(BaseModel):
    message: str
    success: bool
    class Config:
        from_attributes = True

class TasksResp(BaseModel):
    id: int
    title: str
    updated_at: datetime
    
    class Config:
        populate_by_name = True
        from_attributes = True

class NewTaskResp(BaseModel):
    message: str
    task_id: int
    title: str
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SimpleResp(BaseModel):
    message: str
    
    class Config:
        from_attributes = True

class FileUploadResp(BaseModel):
    message: str
    success: bool
    file_path: str
    task_id: str

    class Config:
        from_attributes = True

class AnswerDataResp(BaseModel):
    chat_id: int
    task_id: int
    query: str
    answer: str
    class Config:
        from_attributes = True
        populate_by_name = True


class AskQueryResp(BaseModel):
    message: str
    success: bool
    result: AnswerDataResp

    class Config:
        from_attributes = True


class ChatDataResp(BaseModel):
    id: int
    prompt: str
    response: str
    task_id: int
    is_revised: bool
    revised_prompt: Optional[str] = None
    revised_response: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True

class TaskChatResp(BaseModel):
    message: str
    success: bool
    task_id: int
    result: List[ChatDataResp]

    class Config:
        from_attributes = True