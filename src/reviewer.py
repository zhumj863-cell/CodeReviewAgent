from src.ai_client import llm_with_tools
from src.tools import count_lines, list_functions

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
        response = llm_with_tools.invoke(messages)
        print(response)
        if response.tool_calls:
            messages.append(response)
            for tool_call in response.tool_calls:
                func = TOOL_MAP.get(tool_call["name"])
                args = tool_call["args"]
                result = func.invoke(args) if func else 'None'
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": str(result)
                })
        else:
            break

def read_file(file_path):
    with open(file_path, encoding="utf-8") as file:
        return file.read()
