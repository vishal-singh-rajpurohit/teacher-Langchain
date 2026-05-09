from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.session import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)

    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)

    is_revised = Column(Boolean, default=False)

    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    revised_prompt = Column(Text, nullable=True)
    revised_response = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # 🔗 Relationships
    task = relationship("Task", back_populates="chats")