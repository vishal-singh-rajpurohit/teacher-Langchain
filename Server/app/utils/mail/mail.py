import resend
import random
import base64
from typing import Dict
from dotenv import load_dotenv
import os

from .templates import forget_passowrd_otp, password_reset_mail, registration_mail, verification_otp, verified_mail

load_dotenv()

resend.api_key = os.getenv("RESENDER_API_KEY")

ADMIN_EMAIL = os.getenv("ADMIN_MAIL_ADDRESS")

async def send_registration_mail(to:str, name: str) -> Dict:

    params: resend.Emails.SendParams = {
        "from": "onboarding@resend.dev",
        "to": [f'{to}'],
        "subject": f'Registration Successful',
        "html":  registration_mail(name),
    }
    email: resend.Email = resend.Emails.send(params)

    return email

async def send_verification_otp(to: str, name: str, otp: str):
    params: resend.Emails.SendParams = {
        "from": "onboarding@resend.dev",
        "to": [f'{to}'],
        "subject": f'Verification OTP',
        "html":  verification_otp(name, otp) ,
    }
    email: resend.Email = resend.Emails.send(params)

    return email

async def send_forget_otp(to: str, name: str, otp: str):
    params: resend.Emails.SendParams = {
        "from": "onboarding@resend.dev",
        "to": [f'{to}'],
        "subject": f'Verify otp for reset the password',
        "html":  forget_passowrd_otp(name, otp) ,
    }
    email: resend.Email = resend.Emails.send(params)

    return email

async def password_reset_mail(to: str, name: str):
    params: resend.Emails.SendParams = {
        "from": "onboarding@resend.dev",
        "to": [f'{to}'],
        "subject": f'Your account password is successully reset',
        "html":  password_reset_mail(name) ,
    }
    email: resend.Email = resend.Emails.send(params)

    return email

async def send_verified_mail(to: str, name: str):
    params: resend.Emails.SendParams = {
        "from": "onboarding@resend.dev",
        "to": [f'{to}'],
        "subject": f'Account Verification Successful',
        "html":  verified_mail(name) ,
    }
    email: resend.Email = resend.Emails.send(params)

    return email
