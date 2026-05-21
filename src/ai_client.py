from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langgraph.prebuilt import create_react_agent
from constant import OPENAI_MODEL, ALL_MINILM_MODEL
from src.constant import API_KEY, BASE_URL
from tools import count_lines, list_functions

llm = ChatOpenAI(
    model=OPENAI_MODEL,
    api_key=API_KEY,
    base_url=BASE_URL
)
agent = create_react_agent(llm, tools=[count_lines, list_functions])

embeddings = HuggingFaceEmbeddings(model_name=ALL_MINILM_MODEL)