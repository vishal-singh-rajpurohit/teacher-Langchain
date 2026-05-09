from fastapi import APIRouter, status, Request, Depends, Response
from sqlalchemy.orm import Session
from ..db.session import get_db
from typing import Annotated
from ..middleware.auth_middleware import is_loggedin
import os
from dotenv import load_dotenv

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