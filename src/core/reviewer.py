import json

from langchain_community.vectorstores import Chroma
from langchain_core.messages import SystemMessage, HumanMessage

from ..llm.client import embeddings, get_llm
from ..db.service import db_create_chat, db_append_message, db_get_chat
from ..llm.client import get_general_agent, get_review_graph

async def review(message_from_user: str, model: str, chat_id: str = None):
    # file_content = read_file(file_path)
    file_content = message_from_user
    llmMessages = [
        {
            "role": "user",
            "content": message_from_user
        }
    ]
    need_review_code = await is_review_request(message_from_user, model)

    if need_review_code:
        standards_text = await get_standards(file_content)
        review_agent = get_review_graph(model)
        input_data = {"messages": llmMessages, "rules": standards_text}
        target_node = "summarize"
    else:
        review_agent = get_general_agent(model)
        input_data = {"messages": llmMessages}
        target_node = "agent"
    if chat_id == None:
        chat = db_create_chat(message_from_user[:30], message_from_user)
        chat_id = chat.id
        # 第一条先把 chat_id 发给前端
        yield json.dumps({"type": "chat_id", "data": chat_id}) + "\n"
    else:
        db_append_message(chat_id, "user", message_from_user)
    config = {"configurable": {"thread_id": chat_id}}
    assistant_message = ''
    async for event in review_agent.astream_events(input_data, config=config, version="v2"):
        if event["event"] == "on_chat_model_stream":
            node = event.get("metadata", {}).get("checkpoint_ns")
            if node.startswith(target_node):
                content = event["data"]["chunk"].content
                if content:
                    assistant_message = assistant_message + content
                    yield json.dumps({"type": "content", "data": content}) + "\n"
    db_append_message(chat_id, "assistant", assistant_message)

async def get_standards(file_content: str) -> str:
    vector_stores = Chroma(persist_directory="./src/chroma_db", embedding_function=embeddings)
    related_standards = vector_stores.similarity_search(file_content, k=3)
    standards_text = "\n".join([doc.page_content for doc in related_standards])
    return standards_text
# def read_file(file_path):
#     with open(file_path, encoding="utf-8") as file:
#         return file.read()

async def is_review_request(message: str, model: str) -> bool:
    llm = get_llm(model)
    resp = await llm.ainvoke([
        SystemMessage("判断用户意图是否为代码审查。只回答 yes 或 no"),
        HumanMessage(message)
    ])
    return "yes" in resp.content.lower()
