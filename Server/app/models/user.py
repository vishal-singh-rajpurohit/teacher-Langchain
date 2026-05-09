from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(30), nullable=False)
    email = Column(String(60), nullable=False, unique=True, index=True)
    password = Column(String(200), nullable=False)

    is_verified = Column(Boolean, default=False, nullable=False)
    credits_token = Column(Integer, default=0, nullable=False)

    refresh_token = Column(String(200), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 🔗 Relationships
    tasks = relationship("Task", back_populates="user", cascade="all, delete")