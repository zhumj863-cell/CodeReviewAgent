from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma

from src.ai_client import embeddings

loader = TextLoader("coding_standards.md", encoding="utf-8")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50
)

chunks = splitter.split_documents(docs)

# 测试：打印分块结果
# if __name__ == "__main__":
#     print(f"原始文档数: {len(docs)}")
#     print(f"分块数: {len(chunks)}")
#     for i, chunk in enumerate(chunks):
#         print(f"\n--- Chunk {i} (长度: {len(chunk.page_content)}) ---")
#         print(chunk.page_content)

# 正式嵌入（测试时可注释掉）
vector_stores = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")

# 查看所有存储的文档内容
results = vector_stores.get()
for i, doc in enumerate(results["documents"]):
    print(f"\n--- 文档 {i} ---")
    print(doc)