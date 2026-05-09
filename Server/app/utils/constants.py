ACCESS_TOKEN_EXPIRE_SECONDS = 15 * 60          # 15 minutes
REFRESH_TOKEN_EXPIRE_SECONDS = 7 * 24 * 60 * 60  # 7 days

COOKIE_OPTIONS = {
    'httponly' : True,
    'secure' : False,
    'samesite': "lax",
}