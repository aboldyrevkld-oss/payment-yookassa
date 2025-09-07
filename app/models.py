from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.sql import func
from app.db import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True, index=True)  # id из YooKassa
    amount = Column(Float, nullable=False)
    currency = Column(String(8), default="RUB")
    description = Column(String, nullable=True)
    status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
