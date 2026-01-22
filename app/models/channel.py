# app/models/channel.py
from sqlalchemy import Column, String, DateTime, Text
from app.db.session import Base

class Channel(Base):
    __tablename__ = "channels"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime(timezone=True))  # ← Теперь с временной зоной
    last_checked_at = Column(DateTime(timezone=True), nullable=True)  # ← И здесь тоже