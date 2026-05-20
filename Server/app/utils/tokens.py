import jwt
import datetime
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from fastapi import status, HTTPException

load_dotenv()

SESSION_SECRET = os.getenv("SESSION_SECRET")

class TokenPayload(BaseModel):
    id: int
    email:str

class SessionPayload(BaseModel):
    id: int


ALGO = os.getenv("ALGO")

def genrate_token(paylod:TokenPayload, secret_key:str, expiry: str = "30")->str:
    data = {
        "id": paylod.id,
        "email": paylod.email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=int(expiry)),
        "iat": datetime.datetime.utcnow()
    }

    encoded_jwt = jwt.encode(data, secret_key, algorithm=ALGO)

    return encoded_jwt


def genrate_session_token(payload: SessionPayload):
    data = {
        "id": payload.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=int(60)),
        "iat": datetime.datetime.utcnow()
    }

    encoded_jwt = jwt.encode(data, SESSION_SECRET, algorithm=ALGO)
    return encoded_jwt


def decrypt_token(token:str, secret_key: str):
    try:
        decoded_data = jwt.decode(token, secret_key, algorithms=[ALGO])
        return decoded_data
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Token expired"}
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Invalid token"}
        )


    
