from fastapi import Request, Response, HTTPException, Form, status, Depends, UploadFile
from fastapi.responses import StreamingResponse
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableBranch
from langchain_core.output_parsers import PydanticOutputParser
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from langchain_community.document_loaders import PyPDFLoader

from ..db.session import get_db
from ..schema.req import SimplePromptReqSchema, ChatReqSchema, EmbeedReqSchema, QueryReqSchema, EditQueryReqSchema
from ..schema.resp import NewTaskResp, SimpleResp, FileUploadResp, AskQueryResp, AnswerDataResp, TaskChatResp, ChatDataResp
from ..models.tasks import Task
from ..models.user import User
from ..models.chats import Chat
from ..services.chains import label_chain
from ..services.splitter import recursive_splitter
from ..services.vector_db import vector_store
from ..services.prompts import answer_prompt_template, general_query_prompt
from ..services.model import label_model
from ..services.parsers import pydantic_parser



from dotenv import load_dotenv
import os
import shutil
from datetime import datetime

from pathlib import Path

load_dotenv()

UPLOAD_DIR = "uploads"

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

from fastapi.responses import StreamingResponse
import json


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
                    format_instructions="Return only the answer text."
                )
            else:
                prompt = general_query_prompt.format_messages(
                    query=payload.query
                )

            async for chunk in label_model.astream(prompt):
                token = chunk.content or ""
                full_answer += token

                yield f"data: {json.dumps({'token': token})}\n\n"

            new_chat = Chat(
                task_id=task.id,
                prompt=payload.query,
                response=full_answer
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

        print('do')
        db.commit()
        db.refresh(chat)
        print('done')

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
        print('Error in: ', e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Cannot process query"}
        )
 