from db_service import db_get_chat, db_list_chat


def get_history(chat_id: str):
    return db_get_chat(chat_id)

def list_chat_history():
    return db_list_chat()