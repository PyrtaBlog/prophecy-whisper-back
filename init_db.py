from app.db.session import engine, Base
from app.models.channel import Channel
from app.models.video import Video

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created")