from fastapi import APIRouter, Request, Response, Depends, status
from sqlalchemy.orm import Session
from ..middleware.auth_middleware import is_loggedin
from ..db.session import get_db
from ..schema.req import SimplePromptReqSchema

from ..controllers.task import create_new_task


task_router = APIRouter(prefix='/llm', tags=['LLM'], dependencies=[Depends(is_loggedin)])

@task_router.post('/new', status_code=status.HTTP_201_CREATED)
async def root(req: Request, resp: Response, payload: SimplePromptReqSchema, db: Session = Depends(get_db)):
    return await create_new_task(req, resp, payload, db)