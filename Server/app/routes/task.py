from fastapi import APIRouter, Request, Response, Depends, status, UploadFile, Form, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from ..middleware.auth_middleware import is_loggedin
from ..db.session import get_db
from ..schema.req import SimplePromptReqSchema, ChatReqSchema, EmbeedReqSchema, QueryReqSchema, EditQueryReqSchema, ChatStreamReqSchema
from ..schema.resp import FileUploadResp, SimpleResp, NewTaskResp

from ..controllers.task import create_new_task, recive_pdf_file, create_file_embeddings, ask_query, get_chats, edit_ask_query, list_task_files, upload_task_files, delete_task_file, stream_task_chat


task_router = APIRouter(prefix='/llm', tags=['LLM'], dependencies=[Depends(is_loggedin)])

@task_router.post('/new', response_model=NewTaskResp, status_code=status.HTTP_201_CREATED)
async def root(req: Request, resp: Response, payload: SimplePromptReqSchema, db: Session = Depends(get_db)):
    return await create_new_task(req, resp, payload, db)

@task_router.post('/upload-file', response_model=FileUploadResp, status_code=status.HTTP_201_CREATED)
async def root(
    req: Request,
    resp: Response,
    id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)):
    
    payload = ChatReqSchema(id=id)
    return await recive_pdf_file(req, resp, payload, file, db)

@task_router.get('/{task_id}/files', status_code=status.HTTP_200_OK)
async def root(req: Request, task_id: int, db: Session = Depends(get_db)):
    return await list_task_files(req, task_id, db)

@task_router.post('/{task_id}/files', status_code=status.HTTP_201_CREATED)
async def root(
    req: Request,
    task_id: int,
    files: list[UploadFile] = File(..., alias="files[]"),
    db: Session = Depends(get_db)
):
    return await upload_task_files(req, task_id, files, db)

@task_router.delete('/{task_id}/files/{file_id}', status_code=status.HTTP_200_OK)
async def root(req: Request, task_id: int, file_id: int, db: Session = Depends(get_db)):
    return await delete_task_file(req, task_id, file_id, db)

@task_router.post('/{task_id}/chat/stream', status_code=status.HTTP_200_OK)
async def root(req: Request, task_id: int, payload: ChatStreamReqSchema, db: Session = Depends(get_db)):
    return await stream_task_chat(req, task_id, payload, db)

@task_router.post('/genreate-enbeddings', response_model=SimpleResp, status_code=status.HTTP_200_OK)
async def root(req: Request, payload: EmbeedReqSchema):
    return await create_file_embeddings(req, payload)

@task_router.post('/query', status_code=status.HTTP_200_OK)
async def root(req: Request, resp: Response, paylod: QueryReqSchema, db: Session = Depends(get_db)):
    return await ask_query(req, paylod, db)

@task_router.post('/edit-query', status_code=status.HTTP_200_OK)
async def root(req: Request, payload: EditQueryReqSchema, db: Session = Depends(get_db)):
    return await edit_ask_query(req, payload, db)

@task_router.get('/get-chats', status_code=status.HTTP_200_OK)
async def root(req: Request, id: str, db: Session = Depends(get_db)):
    return await get_chats(req, id, db)

