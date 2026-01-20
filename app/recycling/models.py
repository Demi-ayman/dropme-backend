from sqlalchemy import Column, Integer, Float, String, ForeignKey , DateTime
from app.core.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Recycling(Base):
    __tablename__ = "recycling"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    material_type = Column(String, nullable=False)
    weight_kg = Column(Float, nullable=False)
    points_earned = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="recycling_transactions")