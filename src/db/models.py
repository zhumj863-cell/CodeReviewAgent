from datetime import datetime
import uuid

from sqlalchemy import create_engine, Column, String, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DATABASE_URL = "postgresql://zmj@localhost:5432/code_review"
engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase):
    pass

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    topic: Mapped[str] = mapped_column(String, nullable=False, index=True)
    create_time: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    update_time: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    messages = Column(JSONB, default=[])

    __table_args__ = (
        UniqueConstraint("topic", "create_time", name="uq_topic_create_time"),
    )

Base.metadata.create_all(engine)