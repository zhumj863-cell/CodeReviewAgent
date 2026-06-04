import json

from langchain_community.vectorstores import Chroma
from ..llm.client import embeddings
from ..db.service import db_create_chat, db_append_message, db_get_chat
from ..llm.client import get_agent

SYSTEM_MSG_TEMPLATE = ("你是一个代码审查专家，帮助用户审查代码、优化代码、解答代码相关问题。"
                       "如果用户的问题与代码无关，礼貌地拒绝并引导用户回到代码审查话题。"
                       "根据以下编码规范审查代码\n{}")
CODE_REVIEW_TEMPLATE = ("帮我审查下面的代码，内容是\n{}")


async def review(code: str, model: str, chat_id: str = None):
    # file_content = read_file(file_path)
    file_content = code
    standards_text = await get_standards(file_content)
    llmMessages = []
    agent = get_agent(model)
    if chat_id == None:
        chat = db_create_chat(code[:30], code)
        chat_id = chat.id
        # 第一条先把 chat_id 发给前端
        yield json.dumps({"type": "chat_id", "data": chat_id}) + "\n"
        llmMessages = [
            {
                "role": "system",
                "content": SYSTEM_MSG_TEMPLATE.format(standards_text)
            },
            {
                "role": "user",
                "content": CODE_REVIEW_TEMPLATE.format(code)
            }
        ]
    else:
        db_append_message(chat_id, "user", code)
        llmMessages.append({
            "role": "user",
            "content": code
        })
    config = {"configurable": {"thread_id": chat_id}}
    assistant_message = ''
    async for event in agent.astream_events({"messages": llmMessages}, config=config, version="v2"):
        if event["event"] == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                assistant_message = assistant_message + content
                yield json.dumps({"type": "content", "data": content}) + "\n"
    db_append_message(chat_id, "assistant", assistant_message)


async def get_standards(file_content: str) -> str:
    vector_stores = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    related_standards = vector_stores.similarity_search(file_content, k=3)
    standards_text = "\n".join([doc.page_content for doc in related_standards])
    return standards_text


def read_file(file_path):
    with open(file_path, encoding="utf-8") as file:
        return file.read()
