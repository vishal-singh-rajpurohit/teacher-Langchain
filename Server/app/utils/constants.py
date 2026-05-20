from ..core.config import get_settings

settings = get_settings()

ACCESS_TOKEN_EXPIRE_SECONDS = settings.access_token_expire_seconds
REFRESH_TOKEN_EXPIRE_SECONDS = settings.refresh_token_expire_seconds

COOKIE_OPTIONS = {
    "httponly": True,
    "secure": settings.cookie_secure or settings.is_production,
    "samesite": settings.cookie_samesite,
}

MODELS_DICT = {
    "label_gen_model": "deepseek-ai/DeepSeek-V4-Pro"
}

QUERY_TYPES = {
    "SUMMARIZE_PDF": "SUMMARIZE THE PDF",
}
