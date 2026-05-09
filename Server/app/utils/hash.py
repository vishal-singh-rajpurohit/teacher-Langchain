import hashlib
import hmac
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    sha = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return pwd_context.hash(sha)

def verify_password(plain_password: str, hashed: str) -> bool:
    sha = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
    return pwd_context.verify(sha, hashed)
    
def verify_webhook_signature(body: bytes, signature: str, secret: str) -> bool:
    generated_signature = hmac.new(
        bytes(secret, "utf-8"),
        body,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(generated_signature, signature)