from datetime import datetime
from sqlalchemy.orm import sessionmaker
from .models import engine, ChatHistory
SessionLocal = sessionmaker(bind=engine)

def db_create_chat(topic: str, content: str = None):
    with SessionLocal() as session:
        new_msg = {"role": "user", "content": content}
        chat = ChatHistory(topic=topic, messages=[new_msg])
        chat.create_time = datetime.now()
        session.add(chat)
        session.commit()
        session.refresh(chat)
        return chat

def db_append_message(chat_id: str, role: str, content: str):
    with SessionLocal() as session:
        chat = session.query(ChatHistory).filter_by(id=chat_id).first()
        if not chat:
            return None
        new_msg = {"role": role, "content": content}
        chat.messages = (chat.messages or []) + [new_msg]
        chat.update_time = datetime.now()
        session.commit()
        session.refresh(chat)
        return chat

def db_get_chat(chat_id: str):
    with SessionLocal() as session:
        return session.query(ChatHistory).filter_by(id=chat_id).first()

def db_list_chat():
    with SessionLocal() as session:
        return session.query(ChatHistory).order_by(ChatHistory.update_time.desc()).all()