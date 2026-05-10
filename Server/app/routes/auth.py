from fastapi import APIRouter, status, Request, Depends, Response
from sqlalchemy.orm import Session
from ..db.session import get_db
from typing import Annotated
from ..middleware.auth_middleware import is_loggedin
from ..controllers.auth import check_email_available, check_already, login, signup, logout
from ..schema.resp import LoginResp, CheckEmailAvilableResp
from ..schema.req import CheckMailReqSchema, LoginReqSchema, RegisterReqSchema 
from dotenv import load_dotenv
import os

load_dotenv()

auth_router = APIRouter(prefix='/auth', tags=['AUTH'])

ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET")

db_depandency = Annotated[Session, Depends(get_db)]

@auth_router.get('/')
def root():
    return{
        'message': 'Hello'
    }

# @auth_router.post('/', response_model=LoginResp, status_code=status.HTTP_200_OK, dependencies= [Depends(is_loggedin)])
# async def root(payload: CheckMailReqSchema, db:Session = Depends(get_db)):
#     return await check_email_available(payload, db)

@auth_router.post('/', response_model=LoginResp, status_code=status.HTTP_200_OK, dependencies= [Depends(is_loggedin)])
async def root(req: Request, resp: Response, db:Session = Depends(get_db)):
    return await check_already(req, resp, db)

@auth_router.post('/register', response_model=LoginResp, status_code=status.HTTP_201_CREATED)
async def root(req: Request, resp: Response, payload: RegisterReqSchema, db:Session = Depends(get_db)):
    return await signup(req, resp, payload, db)

@auth_router.post('/login', response_model=LoginResp, status_code=status.HTTP_200_OK)
async def root(resp: Response, payload: LoginReqSchema, db:Session = Depends(get_db)):
    return await login(resp, payload, db)

@auth_router.get('/logout', status_code=status.HTTP_200_OK, dependencies= [Depends(is_loggedin)])
async def root(req: Request, resp: Response, db:Session = Depends(get_db)):
    return await logout(req, resp, db)

@auth_router.post('/is-email-avilable', response_model=CheckEmailAvilableResp, status_code=status.HTTP_200_OK)
async def root(payload: CheckMailReqSchema, db:Session = Depends(get_db)):
    return await check_email_available(payload, db)



