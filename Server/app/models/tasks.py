from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.session import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    title = Column(Text, nullable=False)
    initial_prompt = Column(String, nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)

    has_file = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 🔗 Relationships
    user = relationship("User", back_populates="tasks")
    chats = relationship("Chat", back_populates="task", cascade="all, delete")
    pdf_files = relationship("PdfFile", back_populates="task", cascade="all, delete")
