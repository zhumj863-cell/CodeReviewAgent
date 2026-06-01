from db_service import get_chat, list_chat


def get_history(chat_id: str):
    return get_chat(chat_id)

def list_chat_history():
    return list_chat()