from fastapi import Request, Response, HTTPException, status, Depends
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..middleware.auth_middleware import is_loggedin
from ..schema.req import SimplePromptReqSchema
from ..schema.resp import NewTaskResp
from ..models.tasks import Task
from ..models.user import User
from ..models.chats import Chat
from ..services.chains import label_chain

from dotenv import load_dotenv
import os


load_dotenv()


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
        print('Error in: ', e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                'message': 'Error in getting exception'
            })

    

async def recive_file(req: Request, resp: Response, db: Session = Depends(get_db)):
    pass

async def create_file_embeddings(req: Request, resp: Response, db: Session = Depends(get_db)):
    pass

