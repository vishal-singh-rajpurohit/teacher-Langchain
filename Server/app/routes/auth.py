from fastapi import APIRouter, status, Request, Depends, Response
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from typing import Annotated
import os

from ..db.session import get_db
from ..middleware.auth_middleware import is_loggedin
from ..schema.resp import LoginResp, CheckEmailAvilableResp
from ..schema.req import CheckMailReqSchema, LoginReqSchema, RegisterReqSchema, OTPEmailReqSchema, ResetPassSchema, OTPReqSchema

from ..controllers.auth import check_email_available, check_already, login, signup, logout, verify_account, send_reset_otp, verify_reset_otp, reset_password

load_dotenv()

auth_router = APIRouter(prefix='/auth', tags=['AUTH'])

ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET")

db_depandency = Annotated[Session, Depends(get_db)]

# @auth_router.post('/', response_model=LoginResp, status_code=status.HTTP_200_OK, dependencies= [Depends(is_loggedin)])
# async def root(payload: CheckMailReqSchema, db:Session = Depends(get_db)):
#     return await check_email_available(payload, db)

@auth_router.get('/', response_model=LoginResp, status_code=status.HTTP_200_OK, dependencies= [Depends(is_loggedin)])
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

@auth_router.post('/verify-account', status_code=status.HTTP_200_OK, dependencies= [Depends(is_loggedin)])
async def root(req: Request, payload: OTPReqSchema, db:Session = Depends(get_db)):
    return await verify_account(req, payload, db)

@auth_router.post('/forgot-password', status_code=status.HTTP_200_OK)
async def root(payload: CheckMailReqSchema, db:Session = Depends(get_db)):
    return await send_reset_otp(payload, db)

@auth_router.post('/verify-forgot-password', status_code=status.HTTP_200_OK)
async def root(resp: Response, payload: OTPEmailReqSchema, db:Session = Depends(get_db)):
    return await verify_reset_otp(resp,payload, db)

@auth_router.post('/reset-password', status_code=status.HTTP_200_OK)
async def root(req: Request, resp: Response, payload: ResetPassSchema, db:Session = Depends(get_db)):
    return await reset_password(req, resp, payload, db)

