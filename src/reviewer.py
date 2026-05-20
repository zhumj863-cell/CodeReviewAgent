import json

from ai_client import openai_client
from constant import OPENAI_MODEL
from src.tools import count_lines, list_functions
from tools import TOOLS

TOOL_MAP = {
    "count_lines": count_lines,
    "list_functions": list_functions,
}

def review(file_path):
    file_content = read_file(file_path)
    messages = [
        {"role": "system", "content": "你是一个代码审查专家，从正确性和代码质量两个维度审查代码"},
        {"role": "user", "content": "帮我审查下面的代码，文件路径是 {}, 内容是 {}".format(file_path, file_content)}
    ]
    while True:
        response = openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            tools=TOOLS,
        )
        message = response.choices[0].message
        if message.tool_calls:
            messages.append(message)
            for tool_call in message.tool_calls:
                func = TOOL_MAP.get(tool_call.function.name)
                args = json.loads(tool_call.function.arguments)
                result = func(**args) if func else 'None'
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })
        else:
            print(message.content)
            break


def read_file(file_path):
    with open(file_path, encoding="utf-8") as file:
        return file.read()
