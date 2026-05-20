from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..models.user import User
from ..utils.tokens import decrypt_token
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET")

async def is_loggedin(req: Request, db: Session = Depends(get_db)):
    refresh_token = req.cookies.get("REFRESH_TOKEN")

    if not refresh_token:
        req.state.user = None
        return req.state.user

    try:
        decoded_data = decrypt_token(token=refresh_token, secret_key=REFRESH_TOKEN_SECRET)
    except HTTPException:
        req.state.user = None
        return req.state.user

    user = db.query(User).filter(User.id == decoded_data['id']).first()

    if not user or user.refresh_token != refresh_token:
        req.state.user = None
        return req.state.user

    req.state.user = user
    return req.state.user
