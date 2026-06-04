from __future__ import annotations

import operator
from typing import Annotated, TypedDict
from langchain_community.chat_models import ChatAnthropic
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.prebuilt import create_react_agent

from .tools import run_lint
from ..utils.constant import OPENAI_MODEL, ALL_MINILM_MODEL, API_KEY, BASE_URL


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

general_agent = None
def get_general_agent(model: str):
    global general_agent
    if general_agent is None:
        general_agent = create_react_agent(get_llm(model), tools=[],
                              prompt="你是一个代码审查助手，帮助用户解答代码相关问题。"
                                     "如果用户的问题与代码无关，礼貌地拒绝并引导用户回到代码审查话题。",
                              checkpointer=memory)
    return general_agent

class ReviewState(TypedDict):
    messages: Annotated[list, operator.add]
    rules: str

def should_lint(state):
    code = state["messages"][0]["content"]
    supported = ["def ", "import ", "function ", "const ", "let ", "interface "]
    if any(kw in code for kw in supported):
        return "lint"
    return "skip"

review_graph = None
def get_review_graph(model):
    global review_graph
    if review_graph is None:
        correctness_agent = create_react_agent(
            get_llm(model),
            tools=[],
            prompt=f"你是代码正确性审查专家，专注于逻辑错误、潜在bug和边界情况."
        )
        # standards_agent = create_react_agent(
        #     get_llm(model),
        #     # tools=[count_lines, list_functions],
        #     tools=[],
        #     prompt=f"你是代码规范性审查专家...根据以下编码规范审查代码\n{rules}"
        # )

        async def standards_node(state):
            rules = state.get("rules", "")
            llm = get_llm(model)
            messages = [
                SystemMessage(f"你是代码规范性审查专家...根据以下编码规范审查代码\n{rules}"),
                *state["messages"]
            ]
            resp = await llm.ainvoke(messages)
            return {"messages" : [resp]}

        lint_agent = create_react_agent(
            get_llm(model),
            tools=[run_lint],
            prompt="你是代码静态检查专家。识别用户代码的语言，然后用 run_lint 工具检查。"
                   "只支持 python、javascript、typescript，其他语言直接说明不支持。"
        )

        summarize_agent = create_react_agent(
            get_llm(model),
            # tools=[count_lines, list_functions],
            tools=[],
            prompt=f"将上面专家的审查结果整合为一份完整的审查报告，去重并分类展示."
        )
        graph = StateGraph(ReviewState)
        graph.add_node("correctness", correctness_agent)
        graph.add_node("standards", standards_node)
        graph.add_node("lint", lint_agent)
        graph.add_node("summarize", summarize_agent)

        graph.add_edge(START, "correctness")
        graph.add_edge(START, "standards")
        # graph.add_edge(START, "lint")
        graph.add_conditional_edges(START, should_lint, {
            "lint": "lint",
            "skip": "summarize"
        })
        graph.add_edge("correctness", "summarize")
        graph.add_edge("standards", "summarize")
        graph.add_edge("lint", "summarize")
        graph.add_edge("summarize", END)

        review_graph = graph.compile(checkpointer=memory)
    return review_graph

embeddings = HuggingFaceEmbeddings(model_name=ALL_MINILM_MODEL)
