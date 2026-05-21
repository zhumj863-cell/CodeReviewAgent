from langchain_community.vectorstores import Chroma

from ai_client import agent
from src.ai_client import embeddings


def review(file_path):
    file_content = read_file(file_path)
    vector_stores = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    related_standards = vector_stores.similarity_search(file_content, k=3)
    standards_text = "\n".join([doc.page_content for doc in related_standards])
    print(len(standards_text))
    print(standards_text)
    messages = [
        {"role": "system", "content": "你是一个代码审查专家, 根据以下编码规范审查代码：\n{}".format(standards_text)},
        {"role": "user", "content": "帮我审查下面的代码，文件路径是 {}, 内容是 {}".format(file_path, file_content)}
    ]
    response = agent.invoke({
        "messages": messages
    })
    print(response["messages"][-1].content)


def read_file(file_path):
    with open(file_path, encoding="utf-8") as file:
        return file.read()
