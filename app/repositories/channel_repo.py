from sqlalchemy.orm import Session
from datetime import datetime
from app.models.channel import Channel

class ChannelRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Channel).all()

    def update_last_checked(self, channel_id: str):
        channel = self.db.query(Channel).filter(Channel.id == channel_id).first()
        if channel:
            channel.last_checked_at = datetime.utcnow()
            self.db.commit()

    def get_by_id(self, channel_id: str):
        return self.db.query(Channel).filter(Channel.id == channel_id).first()