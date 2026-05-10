from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from .db.session import Base, engine

from .routes.auth import auth_router
from .routes.task import task_router

from .models.user import User
from .models.chats import Chat
from .models.tasks import Task


load_dotenv()

origins = [
    os.getenv("CORS_ORIGIN"),
    os.getenv("CORS_ORIGIN_"),
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


app.include_router(auth_router, prefix='/api/v1')
app.include_router(task_router, prefix='/api/v1')


@app.get('/')
def root():
    return {
        'message': 'it works!! 👍👍👍👍'
    }