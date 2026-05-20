from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy import text

from .core.config import get_settings
from .db.session import Base, engine
from .models.chats import Chat
from .models.otp import OTP
from .models.pdf_files import PdfFile
from .models.tasks import Task
from .models.user import User
from .routes.auth import auth_router
from .routes.task import task_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.create_tables_on_startup:
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

if settings.allowed_hosts != ["*"]:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.include_router(auth_router, prefix=settings.api_prefix)
app.include_router(task_router, prefix=settings.api_prefix)


@app.get("/")
def root():
    return {"message": "PDF Analyzer API is running"}


@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}


@app.get("/ready", include_in_schema=False)
def ready():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ready"}
