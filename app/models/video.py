from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.types import Enum as SQLEnum
from app.db.session import Base
from enum import Enum

class VideoStatus(str, Enum):
    transcript_pending = "transcript_pending"
    transcript_done = "transcript_done"
    error = "error"

class Video(Base):
    __tablename__ = "videos"

    id = Column(String, primary_key=True, index=True)
    channel_id = Column(String, index=True)
    title = Column(String)
    publish_date = Column(DateTime)
    transcript = Column(Text, nullable=True)
    status = Column(SQLEnum(VideoStatus), default=VideoStatus.transcript_pending)