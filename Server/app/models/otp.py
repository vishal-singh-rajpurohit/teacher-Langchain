from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.session import Base

class OTP(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True, index=True)
    otp = Column(String(6), nullable=False)
    purpose = Column(String(50), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationship
    user = relationship("User", back_populates="otps")