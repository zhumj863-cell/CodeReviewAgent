from langchain_openai import ChatOpenAI

from constant import OPENAI_MODEL
from tools import TOOLS

llm = ChatOpenAI(
    model=OPENAI_MODEL,
    api_key="",
    base_url="https://api.deepseek.com"
)
llm_with_tools = llm.bind_tools(TOOLS)