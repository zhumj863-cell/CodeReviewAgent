from db_service import db_list_chat, db_get_chat

def get_chat_history():
    chat_histories = db_list_chat()
    result = []
    for chat in chat_histories:
        result.append({
            "topic": chat.topic,
            "createTime": chat.create_time,
            "chatId": chat.id,
        })
    return result

def query_chat(chat_id: str):
    chat = db_get_chat(chat_id)
    return {
        "topic": chat.topic,
        "createTime": chat.create_time,
        "chatId": chat.id,
        "messages": chat.messages
    }
