from langchain_core.tools import tool
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "count_lines",
            "description": "统计文件行数",
            "parameters":  {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "文件路径",
                    },
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_functions",
            "description": "列出文件中所有的函数名",
            "parameters":  {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "文件路径",
                    },
                },
                "required": ["file_path"]
            }
        }
    }
]
@tool
def count_lines(file_path) -> int:
    """统计文件行数"""
    with open(file_path) as file:
        return len(file.readlines())

@tool
def list_functions(file_path) -> list[str]:
    """列出文件中所有的函数名"""
    with open(file_path) as file:
        function_lines = []
        for line in file:
            line_data = line.strip()
            if line_data.startswith("def "):
                function_lines.append(line_data[4: line_data.find("(")])
        return function_lines
