from fastapi import Request, Response, HTTPException, status, Depends
from sqlalchemy.orm import Session

from ..db.session import get_db
from ..schema.req import RegisterReqSchema, LoginReqSchema, CheckMailReqSchema
from ..schema.resp import LoginResp, CheckEmailAvilableResp
from ..utils.hash import hash_password, verify_password
from ..utils.tokens import genrate_token, TokenPayload
from ..models.user import User
from ..utils.constants import COOKIE_OPTIONS
import os


ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET")


async def signup( req: Request, resp: Response, payload: RegisterReqSchema, db: Session = Depends(get_db)):
    if not payload.name or not payload.email or not payload.password or not payload.conform_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "All data required"}
        )

    if payload.password != payload.conform_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Password not matching"}
        )

    existing_user = db.query(User).filter(User.email == payload.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": "User already exists with this email"}
        )

    hashed_password = hash_password(payload.password)

    new_user = User(
        name=payload.name,
        email=payload.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token_payload = TokenPayload(
        id=new_user.id,
        email=new_user.email
    )

    access_token = genrate_token(
        paylod=token_payload,
        secret_key=ACCESS_TOKEN_SECRET,
        expiry="30"
    )

    refresh_token = genrate_token(
        paylod=token_payload,
        secret_key=REFRESH_TOKEN_SECRET,
        expiry="10080"  # 7 days
    )

    new_user.refresh_token = refresh_token
    db.commit()
    db.refresh(new_user)

    resp.set_cookie(
        key="ACCESS_TOKEN",
        value=access_token,
        httponly=True,
        secure=False,  # True in production with HTTPS
        samesite="lax",
        max_age=30 * 60
    )

    resp.set_cookie(
        key="REFRESH_TOKEN",
        value=refresh_token,
        httponly=True,
        secure=False,  # True in production with HTTPS
        samesite="lax",
        max_age=7 * 24 * 60 * 60
    )

    return LoginResp(
        message="User registered successfully",
        name=new_user.name,
        email=new_user.email,
        credits_token=new_user.credits_token,
        is_verified=new_user.is_verified
    )

async def login( resp: Response, payload: LoginReqSchema, db: Session = Depends(get_db)):
    if not payload.email or not payload.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Email and password required"}
        )

    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "User not found"}
        )

    is_password_correct = verify_password(payload.password, user.password)

    if not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Invalid email or password"}
        )

    token_payload = TokenPayload(
        id=user.id,
        email=user.email
    )

    access_token = genrate_token(
        paylod=token_payload,
        secret_key=ACCESS_TOKEN_SECRET,
        expiry="30"
    )

    refresh_token = genrate_token(
        paylod=token_payload,
        secret_key=REFRESH_TOKEN_SECRET,
        expiry="10080"
    )

    user.refresh_token = refresh_token
    db.commit()
    db.refresh(user)

    resp.set_cookie(
        key="ACCESS_TOKEN",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=30 * 60
    )

    resp.set_cookie(
        key="REFRESH_TOKEN",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=7 * 24 * 60 * 60
    )

    return LoginResp(
        message="User registered successfully",
        name=user.name,
        email=user.email,
        credits_token=user.credits_token,
        is_verified=user.is_verified
    )

async def check_email_available(payload: CheckMailReqSchema, db: Session) -> bool:

    if not payload.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                'message': 'email not found'
            }
        )

    user = db.query(User).filter(User.email == payload.email).first()

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": "Email already in use"}
        )

    return CheckEmailAvilableResp(
        message="Email is Avilable",
        success=True
    )

async def logout(req: Request, resp: Response, db: Session = Depends(get_db)):
    try:
        auth_user = req.state.user

        if not auth_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
                'message': 'Unautharized Access'
            })

        user = db.query(User).filter(User.id == auth_user.id).first()

        user.access_token = ""
        user.refresh_token = ""

        db.commit()

        resp.delete_cookie("ACCESS_TOKEN")
        resp.delete_cookie("REFRESH_TOKEN")

        return {
            'message': 'User Logged Out'
        }

    except Exception as e:
        db.rollback()
        print(f'error in: {e}')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
                'message': 'Unautharized access'
            })

async def check_already(req: Request, resp: Response, db:Session = Depends(get_db), ):
    auth_user = req.state.user

    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                'message': 'Unautharized Acccess'
            })

    access_token = genrate_token(TokenPayload(id=auth_user.id, email=auth_user.mail), ACCESS_TOKEN_SECRET)
    refresh_token = genrate_token(TokenPayload(id=auth_user.id, email=auth_user.mail), REFRESH_TOKEN_SECRET)

    if not refresh_token or not access_token:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,  detail={
                'message': 'Token not found'
            })

    user = db.query(User).filter(User.id == auth_user.id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
            'message': 'User not found but created'
        })
    
    user.access_token = access_token
    user.refresh_token = refresh_token
    
    db.commit()

    resp.set_cookie(
            key='ACCESS_TOKEN',
            value=access_token,
            httponly=COOKIE_OPTIONS['httponly'],
            secure=COOKIE_OPTIONS['secure'],
            samesite=COOKIE_OPTIONS['samesite']
            )
    resp.set_cookie(
            key='REFRESH_TOKEN',
            value=refresh_token,
            httponly=COOKIE_OPTIONS['httponly'],
            secure=COOKIE_OPTIONS['secure'],
            samesite=COOKIE_OPTIONS['samesite']
            )

    return LoginResp(
        message="User registered successfully",
        name=user.name,
        email=user.email,
        credits_token=user.credits_token,
        is_verified=user.is_verified
    )