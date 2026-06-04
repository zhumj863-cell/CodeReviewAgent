from langchain_community.chat_models import ChatAnthropic
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from ..utils.constant import OPENAI_MODEL, ALL_MINILM_MODEL, API_KEY, BASE_URL
from .tools import count_lines, list_functions

def get_llm(model: str):
    if model == 'gpt':
        return ChatOpenAI(model="gpt-4o", api_key=...)
    elif model == 'claude':
        return ChatAnthropic(model="claude-sonnet-4-20250514", api_key=...)
    else:
        return ChatOpenAI(
            model=OPENAI_MODEL,
            api_key=API_KEY,
            base_url=BASE_URL
        )
memory = MemorySaver()
def get_agent(model: str):
    return create_react_agent(get_llm(model), tools=[count_lines, list_functions], checkpointer=memory)

embeddings = HuggingFaceEmbeddings(model_name=ALL_MINILM_MODEL)