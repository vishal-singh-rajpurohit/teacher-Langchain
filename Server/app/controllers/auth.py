from fastapi import Request, Response, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

import os
import random
from datetime import datetime, timedelta, timezone

from ..db.session import get_db
from ..schema.req import RegisterReqSchema, LoginReqSchema, CheckMailReqSchema, OTPReqSchema, ResetPassSchema, OTPEmailReqSchema
from ..schema.resp import LoginResp, CheckEmailAvilableResp
from ..utils.hash import hash_password, verify_password
from ..utils.tokens import genrate_token, TokenPayload, genrate_session_token, SessionPayload, decrypt_token
from ..models.user import User
from ..models.tasks import Task
from ..models.otp import OTP
from ..utils.constants import COOKIE_OPTIONS, ACCESS_TOKEN_EXPIRE_SECONDS, REFRESH_TOKEN_EXPIRE_SECONDS
from ..utils.mail.mail import send_registration_mail, send_verification_otp, send_verified_mail, send_forget_otp, password_reset_mail



ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET")
SESSION_SECRET = os.getenv("SESSION_SECRET")


def genrate_otp() -> int:
    return random.randint(100000, 999999)

async def signup(req: Request, resp: Response, payload: RegisterReqSchema, db: Session = Depends(get_db)):
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
    
    try:
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

        result = db.query(Task)\
        .join(User, Task.user_id == User.id)\
        .all()

        resp.set_cookie(
            key="ACCESS_TOKEN",
            value=access_token,
            httponly=COOKIE_OPTIONS['httponly'],
            secure=COOKIE_OPTIONS['secure'],  # True in production with HTTPS
            samesite=COOKIE_OPTIONS['samesite'],
            max_age=ACCESS_TOKEN_EXPIRE_SECONDS
        )

        resp.set_cookie(
            key="REFRESH_TOKEN",
            value=refresh_token,
            httponly=COOKIE_OPTIONS['httponly'],
            secure=COOKIE_OPTIONS['secure'],  # True in production with HTTPS
            samesite=COOKIE_OPTIONS['samesite'],
            max_age=REFRESH_TOKEN_EXPIRE_SECONDS
        )

        await send_registration_mail(
            to=new_user.email,
            name=new_user.name
        )

        otp = genrate_otp()

        new_otp = OTP(
            otp = otp,
            purpose = "Verification OTP",
            user_id = new_user.id
        )

        db.add(new_otp)
        db.commit()
        db.refresh(new_otp)

        await send_verification_otp(
            to=new_user.email, 
            name=new_user.name,
            otp=otp
        )

        return LoginResp(
            message="User registered successfully",
            name=new_user.name,
            email=new_user.email,
            credits_token=new_user.credits_token,
            is_verified=new_user.is_verified,
            updated_at=new_user.updated_at,
            tasks=result
        )
    except Exception as e:
        db.rollback()
        print('Error in: ', e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "User not created"}
        )

async def login(resp: Response, payload: LoginReqSchema, db: Session = Depends(get_db)):
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

    try:
        user.refresh_token = refresh_token
        db.commit()
        db.refresh(user)

        result = db.query(Task).filter(Task.user_id == user.id).all()

        resp.set_cookie(
            key="ACCESS_TOKEN",
            value=access_token,
            httponly=COOKIE_OPTIONS['httponly'],
            secure=COOKIE_OPTIONS['secure'],  # True in production with HTTPS
            samesite=COOKIE_OPTIONS['samesite'],
            max_age=ACCESS_TOKEN_EXPIRE_SECONDS
        )

        resp.set_cookie(
            key="REFRESH_TOKEN",
            value=refresh_token,
            httponly=COOKIE_OPTIONS['httponly'],
            secure=COOKIE_OPTIONS['secure'],  # True in production with HTTPS
            samesite=COOKIE_OPTIONS['samesite'],
            max_age= REFRESH_TOKEN_EXPIRE_SECONDS
        )


        if not user.is_verified:
            otp = genrate_otp()

            new_otp = OTP(
                otp = otp,
                purpose = "Verification OTP",
                user_id = user.id
            )

            db.add(new_otp)
            db.commit()
            db.refresh(new_otp)

            await send_verification_otp(
                to=user.email, 
                name=user.name,
                otp=otp
            )

        return LoginResp(
            message="User registered successfully",
            name=user.name,
            email=user.email,
            credits_token=user.credits_token,
            is_verified=user.is_verified,
            updated_at=user.updated_at,
            tasks=result
        )
    except Exception as e:
        db.rollback()
        print('Error in: ', e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                'message': 'Cannot Save details'
            }
        )

async def verify_account( req: Request, payload: OTPReqSchema, db: Session = Depends(get_db)):

    auth_user = req.state.user

    otp = payload.otp

    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Unauthorized user"}
        )

    user = db.query(User).filter(User.id == auth_user.id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "User not found"}
        )

    if user.is_verified:
        return {
            "success": True,
            "message": "Account already verified"
        }
    

    existing_otp = (
        db.query(OTP)
        .filter(
            OTP.user_id == user.id,
            OTP.otp == otp,
            OTP.purpose == "Verification OTP"
        )
        .order_by(desc(OTP.created_at))
        .first()
    )

    if not existing_otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Invalid OTP"}
        )

    try:
        user.is_verified = True

        db.delete(existing_otp)
        db.commit()
        db.refresh(user)

        await send_verified_mail(to=user.email ,name=user.name)

        return {
            "success": True,
            "message": "Account verified successfully",
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Cannot verify account"}
        )

async def check_email_available(payload: CheckMailReqSchema, db: Session = Depends(get_db)) -> bool:

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

async def check_already(req: Request, resp: Response, db:Session = Depends(get_db)):
    auth_user = req.state.user

    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                'message': 'Unautharized Acccess'
            })

    access_token = genrate_token(TokenPayload(id=auth_user.id, email=auth_user.email), ACCESS_TOKEN_SECRET)
    refresh_token = genrate_token(TokenPayload(id=auth_user.id, email=auth_user.email), REFRESH_TOKEN_SECRET)

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
    
    user.refresh_token = refresh_token
    
    db.commit()

    result = db.query(Task)\
        .join(User, Task.user_id == User.id)\
        .all()

    resp.set_cookie(
            key='ACCESS_TOKEN',
            value=access_token,
            httponly=COOKIE_OPTIONS['httponly'],
            secure=COOKIE_OPTIONS['secure'],
            samesite=COOKIE_OPTIONS['samesite'],
            max_age=ACCESS_TOKEN_EXPIRE_SECONDS
        )
    resp.set_cookie(
            key='REFRESH_TOKEN',
            value=refresh_token,
            httponly=COOKIE_OPTIONS['httponly'],
            secure=COOKIE_OPTIONS['secure'],
            samesite=COOKIE_OPTIONS['samesite'],
            max_age=REFRESH_TOKEN_EXPIRE_SECONDS
        )
    
    if not user.is_verified:
        otp = genrate_otp()

        new_otp = OTP(
            otp = otp,
            purpose = "Verification OTP",
            user_id = user.id
        )

        db.add(new_otp)
        db.commit()
        db.refresh(new_otp)

        await send_verification_otp(
            to=user.email, 
            name=user.name,
            otp=genrate_otp()
        )

    return LoginResp(
        message="User Loggedin successfully",
        name=user.name,
        email=user.email,
        credits_token=user.credits_token,
        is_verified=user.is_verified,
        updated_at=user.updated_at,
        tasks=result
    )

async def send_reset_otp(payload: CheckMailReqSchema, db: Session = Depends(get_db)):
    if not payload.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Email is required"}
        )

    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "User not found"}
        )

    otp = genrate_otp()

    try:
        new_otp = OTP(
            otp=otp,
            purpose="Password Reset OTP",
            user_id=user.id
        )

        db.add(new_otp)
        db.commit()
        db.refresh(new_otp)

        await send_forget_otp(
            to=user.email,
            name=user.name,
            otp=otp
        )

        return {
            "success": True,
            "message": "Password reset OTP sent successfully"
        }

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Cannot send password reset OTP"}
        )

async def verify_reset_otp( resp: Response, payload: OTPEmailReqSchema, db: Session = Depends(get_db)):
    if not payload.email or not payload.otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Email and OTP required"}
        )

    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "User not found"}
        )

    existing_otp = (
        db.query(OTP)
        .filter(
            OTP.user_id == user.id,
            OTP.otp == payload.otp,
            OTP.purpose == "Password Reset OTP"
        )
        .order_by(desc(OTP.created_at))
        .first()
    )

    if not existing_otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Invalid OTP"}
        )

    if existing_otp.created_at < datetime.now(timezone.utc) - timedelta(minutes=10):
        db.delete(existing_otp)
        db.commit()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "OTP expired"}
        )

    try:
        db.delete(existing_otp)
        db.commit()

        session_payload = SessionPayload(id=user.id)

        reset_token = genrate_session_token(session_payload)

        resp.set_cookie(
            key="RESET_TOKEN",
            value=reset_token,
            httponly=True,
            secure=False,  # True in production with HTTPS
            samesite="lax",
            max_age=60 * 60
        )

        return {
            "success": True,
            "message": "OTP verified successfully. You can now reset your password."
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Cannot verify OTP"}
        )

async def reset_password(
    req: Request,
    resp: Response,
    payload: ResetPassSchema,
    db: Session = Depends(get_db)
):
    
    
    if not payload.new_password or not payload.conform_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "New password and confirm password required"}
        )

    if payload.new_password != payload.conform_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Password not matching"}
        )
    
    

    reset_token = req.cookies.get("RESET_TOKEN")

    if not reset_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Reset token missing or expired"}
        )

    decoded_data = decrypt_token(
        token=reset_token,
        secret_key=SESSION_SECRET
    )

    user_id = decoded_data.get("id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"message": "Invalid reset token"}
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "User not found"}
        )

    try:
        
        user.password = hash_password(payload.new_password)

        # Optional: invalidate old refresh token after password reset
        user.refresh_token = None

        db.commit()
        db.refresh(user)

        

        await password_reset_mail(
            to=user.email,
            name = user.name
        )

        

        resp.delete_cookie("RESET_TOKEN")

        return {
            "success": True,
            "message": "Password reset successfully"
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Cannot reset password"}
        )

# Send Reset OTP
# Reset Password