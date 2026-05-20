from fastapi import Request, Response, HTTPException, Form, status, Depends, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableBranch
from langchain_core.output_parsers import PydanticOutputParser
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from langchain_community.document_loaders import PyPDFLoader

from ..core.config import get_settings
from ..db.session import get_db
from ..schema.req import SimplePromptReqSchema, ChatReqSchema, EmbeedReqSchema, QueryReqSchema, EditQueryReqSchema, ChatStreamReqSchema
from ..schema.resp import NewTaskResp, SimpleResp, FileUploadResp, AskQueryResp, AnswerDataResp, TaskChatResp, ChatDataResp, PdfFileResp
from ..models.tasks import Task
from ..models.user import User
from ..models.chats import Chat
from ..models.pdf_files import PdfFile
from ..services.chains import label_chain
from ..services.splitter import recursive_splitter
from ..services.vector_db import vector_store
from ..services.prompts import answer_prompt_template, general_query_prompt
from ..services.model import label_model
from ..services.parsers import pydantic_parser



from dotenv import load_dotenv
import os
import re
import shutil
import json
from datetime import datetime

from pathlib import Path

load_dotenv()

UPLOAD_DIR = "uploads"
settings = get_settings()
PLAIN_TEXT_FORMAT_INSTRUCTIONS = (
    "Return plain Markdown text only. Do not wrap the answer in JSON, code fences, "
    "or an object with an answer key."
)


def unwrap_answer_text(value: str) -> str:
    text = value.strip()
    if not text:
        return ""

    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            for key in ("answer", "response", "content"):
                if key in parsed and parsed[key] is not None:
                    return str(parsed[key]).strip()
    except json.JSONDecodeError:
        pass

    match = re.match(r'^\{\s*"?(answer|response|content)"?\s*:\s*"', text, flags=re.IGNORECASE)
    if not match:
        return value

    answer = text[match.end():]
    answer = re.sub(r'"\s*\}\s*$', "", answer)
    answer = answer.replace(r"\n", "\n").replace(r"\"", '"').replace(r"\\", "\\")
    return answer.strip()


def ensure_user_task(db: Session, user: User, task_id: int) -> Task:
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Task not found or unauthorized"}
        )

    return task


def build_file_response(file_record: PdfFile) -> PdfFileResp:
    return PdfFileResp.model_validate(file_record)


def delete_vectors_for_file(file_id: int):
    collection = getattr(vector_store, "_collection", None)
    if collection is not None:
        collection.delete(where={"file_id": {"$eq": str(file_id)}})


async def embed_pdf_file(file_path: Path, task: Task, user: User, file_record: PdfFile):
    loader = PyPDFLoader(file_path=str(file_path))
    batch = []

    for page_doc in loader.lazy_load():
        chunks = recursive_splitter.split_documents([page_doc])

        for chunk in chunks:
            chunk.metadata.update({
                "task_id": str(task.id),
                "user_id": str(user.id),
                "file_id": str(file_record.id),
                "source": file_record.name
            })

        batch.extend(chunks)

        if len(batch) >= 100:
            vector_store.add_documents(batch)
            batch = []

    if batch:
        vector_store.add_documents(batch)

async def create_new_task(req: Request, resp: Response, payload: SimplePromptReqSchema, db: Session = Depends(get_db)):

    if not req.state.user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                'message': 'Unautharized Access'
            })
    
    if not payload.prompt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                'message': 'Prompt Cannot be empty'
            })
    
    user = db.query(User).filter(User.email == req.state.user.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Unautharized Access"}
        )

    try:

        title = label_chain.invoke(payload.prompt)

        if not title:
            raise HTTPException(
                status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    'message': 'Chain Does not executed'
                })

        new_task = Task(
            user_id = user.id,
            title = title,
            initial_prompt = payload.prompt,
            is_active = True
        )

        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        return NewTaskResp(
            message = "New Task Created",
            task_id = new_task.id,
            title = new_task.title,
            updated_at = new_task.updated_at,
        )
    
    except Exception as e:
        db.rollback()
        # print('Error in: ', e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                'message': 'Error in getting exception'
            })

async def recive_pdf_file(req: Request, resp: Response, payload: ChatReqSchema, file: UploadFile, db: Session = Depends(get_db)):
    user = req.state.user

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Unauthorized Access"}
        )

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "File must be a PDF"}
        )

    if not payload.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Task id required"}
        )
    
    task = db.query(Task).filter(
        Task.id == int(payload.id),
        Task.user_id == user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Task not found or unauthorized"}
        )
    
    try:
        task.has_file = True

        db.commit()
        db.refresh(task)
    except Exception :
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "db not updated"}
        )

    # ✅ Create upload directory
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # ✅ Rename file → taskId_timestamp.pdf
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"{payload.id}_{timestamp}.pdf"
    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        # ✅ Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return FileUploadResp(
            success = True,
            message = "PDF uploaded successfully",
            file_path = file_path,
            task_id = payload.id
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "File upload failed"}
        )

async def create_file_embeddings(req: Request, payload: EmbeedReqSchema):
    if not req.state.user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                'message': 'Unautharized Access'
            })

    file_path = Path(payload.path)

    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {payload.path}")
    
    loader = PyPDFLoader(file_path=str(file_path))

    batch = []

    for page_doc in loader.lazy_load():
        chunks = recursive_splitter.split_documents([page_doc])

        for chunk in chunks:
                chunk.metadata.update({
                    "task_id": str(payload.id),
                    "user_id": str(req.state.user.id),
                    "source": str(file_path.name)
                })

        batch.extend(chunks)

        if len(batch) >= 100:
            vector_store.add_documents(batch)
            batch = []
    
    if batch:
        vector_store.add_documents(batch)
    
    os.remove(file_path)
    
    return SimpleResp(message="Embedding Created")

async def list_task_files(req: Request, task_id: int, db: Session = Depends(get_db)):
    user = req.state.user

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Unauthorized Access"}
        )

    ensure_user_task(db, user, task_id)

    files = (
        db.query(PdfFile)
        .filter(PdfFile.task_id == task_id)
        .order_by(asc(PdfFile.created_at))
        .all()
    )

    return {"files": [build_file_response(file_record) for file_record in files]}


async def upload_task_files(req: Request, task_id: int, files: list[UploadFile], db: Session = Depends(get_db)):
    user = req.state.user

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Unauthorized Access"}
        )

    task = ensure_user_task(db, user, task_id)

    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "At least one PDF is required"}
        )

    saved_files: list[PdfFile] = []
    saved_paths: list[Path] = []
    upload_dir = Path(UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)

    try:
        for upload in files:
            if upload.content_type != "application/pdf":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"message": f"{upload.filename or 'File'} must be a PDF"}
                )

            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
            safe_name = Path(upload.filename or "document.pdf").name
            storage_name = f"{task.id}_{timestamp}_{safe_name}"
            file_path = upload_dir / storage_name

            size = 0
            with file_path.open("wb") as buffer:
                saved_paths.append(file_path)
                while True:
                    chunk = await upload.read(1024 * 1024)
                    if not chunk:
                        break
                    size += len(chunk)
                    if size > settings.max_upload_bytes:
                        raise HTTPException(
                            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                            detail={"message": "PDF exceeds the configured upload limit"}
                        )
                    buffer.write(chunk)

            file_record = PdfFile(
                task_id=task.id,
                name=safe_name,
                size=size,
                storage_path=str(file_path),
            )
            db.add(file_record)
            db.flush()
            saved_files.append(file_record)

            await embed_pdf_file(file_path, task, user, file_record)
            file_record.vectorized = True

        task.has_file = True
        db.commit()

        for file_record in saved_files:
            db.refresh(file_record)

        return {
            "files": [build_file_response(file_record) for file_record in saved_files]
        }

    except HTTPException:
        db.rollback()
        for file_record in saved_files:
            if file_record.id:
                delete_vectors_for_file(file_record.id)
        for file_path in saved_paths:
            file_path.unlink(missing_ok=True)
        raise
    except Exception:
        db.rollback()
        for file_record in saved_files:
            if file_record.id:
                delete_vectors_for_file(file_record.id)
        for file_path in saved_paths:
            file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "File upload failed"}
        )


async def delete_task_file(req: Request, task_id: int, file_id: int, db: Session = Depends(get_db)):
    user = req.state.user

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Unauthorized Access"}
        )

    task = ensure_user_task(db, user, task_id)
    file_record = db.query(PdfFile).filter(
        PdfFile.id == file_id,
        PdfFile.task_id == task.id
    ).first()

    if not file_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "File not found"}
        )

    try:
        delete_vectors_for_file(file_record.id)
        Path(file_record.storage_path).unlink(missing_ok=True)
        db.delete(file_record)
        task.has_file = db.query(PdfFile).filter(
            PdfFile.task_id == task.id,
            PdfFile.id != file_id
        ).first() is not None
        db.commit()
        return {"success": True, "message": "File deleted"}
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Cannot delete file"}
        )


async def stream_task_chat(req: Request, task_id: int, payload: ChatStreamReqSchema, db: Session = Depends(get_db)):
    user = req.state.user

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Unauthorized Access"}
        )

    task = ensure_user_task(db, user, task_id)

    if not payload.prompt.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Prompt cannot be empty"}
        )

    async def event_generator():
        full_answer = ""
        visible_answer = ""
        effective_query = payload.prompt
        if payload.context:
            effective_query = f"Additional context:\n{payload.context}\n\nQuestion:\n{payload.prompt}"

        try:
            retriever = vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={
                    "k": 5,
                    "filter": {
                        "$and": [
                            {"task_id": {"$eq": str(task.id)}},
                            {"user_id": {"$eq": str(user.id)}}
                        ]
                    }
                }
            )

            if task.has_file:
                docs = retriever.invoke(effective_query)
                content = "\n\n".join([doc.page_content for doc in docs])

                prompt = answer_prompt_template.format_messages(
                    content=content,
                    query=effective_query,
                    format_instructions=PLAIN_TEXT_FORMAT_INSTRUCTIONS
                )
            else:
                prompt = general_query_prompt.format(
                    query=effective_query,
                    format_instructions=PLAIN_TEXT_FORMAT_INSTRUCTIONS
                )

            async for chunk in label_model.astream(prompt):
                token = chunk.content or ""
                full_answer += token
                next_visible_answer = unwrap_answer_text(full_answer)
                delta = next_visible_answer[len(visible_answer):]
                visible_answer = next_visible_answer

                if delta:
                    yield json.dumps({"type": "delta", "delta": delta}) + "\n"

            new_chat = Chat(
                task_id=task.id,
                prompt=payload.prompt,
                response=unwrap_answer_text(full_answer)
            )

            db.add(new_chat)
            db.commit()
            db.refresh(new_chat)

            message = ChatDataResp.model_validate(new_chat)
            yield json.dumps({
                "type": "done",
                "message": jsonable_encoder(message)
            }) + "\n"

        except Exception:
            db.rollback()
            yield json.dumps({
                "type": "error",
                "message": "Cannot process query"
            }) + "\n"

    return StreamingResponse(
        event_generator(),
        media_type="application/x-ndjson"
    )


async def ask_query(
    req: Request,
    payload: QueryReqSchema,
    db: Session = Depends(get_db)
):
    user = req.state.user

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Unauthorized Access"}
        )

    task = db.query(Task).filter(
        Task.id == int(payload.id),
        Task.user_id == user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Task not found or unauthorized"}
        )

    async def event_generator():
        full_answer = ""
        visible_answer = ""

        try:
            has_file = task.has_file

            retriever = vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={
                    "k": 5,
                    "filter": {
                        "$and": [
                            {"task_id": {"$eq": str(task.id)}},
                            {"user_id": {"$eq": str(user.id)}}
                        ]
                    }
                }
            )

            if has_file:
                docs = retriever.invoke(payload.query)
                content = "\n\n".join([doc.page_content for doc in docs])

                prompt = answer_prompt_template.format_messages(
                    content=content,
                    query=payload.query,
                    format_instructions=PLAIN_TEXT_FORMAT_INSTRUCTIONS
                )
            else:
                prompt = general_query_prompt.format(
                    query=payload.query,
                    format_instructions=PLAIN_TEXT_FORMAT_INSTRUCTIONS
                )

            async for chunk in label_model.astream(prompt):
                token = chunk.content or ""
                full_answer += token
                next_visible_answer = unwrap_answer_text(full_answer)
                delta = next_visible_answer[len(visible_answer):]
                visible_answer = next_visible_answer

                if delta:
                    yield f"data: {json.dumps({'token': delta})}\n\n"

            new_chat = Chat(
                task_id=task.id,
                prompt=payload.query,
                response=unwrap_answer_text(full_answer)
            )

            db.add(new_chat)
            db.commit()
            db.refresh(new_chat)

            yield f"data: {json.dumps({
                'done': True,
                'chat_id': new_chat.id,
                'task_id': task.id
            })}\n\n"

        except Exception as e:
            db.rollback()
            yield f"data: {json.dumps({
                'error': True,
                'message': 'Cannot process query'
            })}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

async def get_chats(req: Request, id: str, db: Session = Depends(get_db)):
    user = req.state.user

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Unauthorized Access"}
        )
    
    if not id :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Task id required"}
        )
    
    task = db.query(Task).filter(
        Task.id == int(id),
        Task.user_id == user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Task not found or unauthorized"}
        )
    
    chats = (
        db.query(Chat)
        .filter(Chat.task_id == int(id))
        .order_by(asc(Chat.created_at))
        .limit(10)
        .all()
    )

    chats_resp = [ChatDataResp.model_validate(chat) for chat in chats]

    return TaskChatResp(
        message="Here are Chats",
        success=True,
        task_id=task.id,
        result= chats_resp
    )

async def edit_ask_query(req: Request, payload: EditQueryReqSchema, db: Session = Depends(get_db)):
    user = req.state.user

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Unauthorized Access"}
        )
    
    if not payload.id or not payload.query or not payload.chat_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Query or id required"}
        )
    
    task = db.query(Task).filter(
        Task.id == int(payload.id),
        Task.user_id == user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Task not found or unauthorized"}
        )
    
    try:
        has_file = task.has_file

        retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": 5,
                "filter": {
                    "$and": [
                        {"task_id": {"$eq": str(task.id)}},
                        {"user_id": {"$eq": str(user.id)}}
                    ]
                }
            }
        )

        query_chain = (
            RunnableBranch(
                (
                    lambda x: has_file,
                    RunnableParallel({
                        "content": retriever,
                        "query": RunnablePassthrough()
                    })
                ),
                RunnableParallel({
                    "query": RunnablePassthrough(),
                })
            )
            |
            RunnablePassthrough.assign(
                format_instructions=lambda _: pydantic_parser.get_format_instructions()
            )
            |
            RunnableBranch(
                (
                    lambda x: has_file,
                    answer_prompt_template
                ),
                general_query_prompt
            )
            |
            label_model
            |
            pydantic_parser
        )

        result = query_chain.invoke(payload.query)

        chat = db.query(Chat).filter(Chat.id == int(payload.chat_id)).first()

        chat.is_revised = True
        chat.revised_prompt = payload.query
        chat.revised_response = result.answer

        db.commit()
        db.refresh(chat)

        data = AnswerDataResp(
            chat_id = chat.id,
            task_id = task.id,
            query = payload.query,
            answer = result.answer
        )

        return AskQueryResp(
            success = True,
            message = "Query answered successfully",
            result = data
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Cannot process query"}
        )
 
