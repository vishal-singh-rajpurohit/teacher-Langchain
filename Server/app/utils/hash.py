import hashlib
import hmac
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)    
    
def verify_webhook_signature(body: bytes, signature: str, secret: str) -> bool:
    generated_signature = hmac.new(
        bytes(secret, "utf-8"),
        body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(generated_signature, signature)