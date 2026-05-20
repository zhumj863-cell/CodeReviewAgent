"""
写一个 code_parser.py，实现函数 parse_file(file_path: str) -> dict：


输入：一个 Python 文件路径
输出：字典，包含：
{
    "file_name": "example.py",
    "total_lines": 50,
    "blank_lines": 5,
    "comment_lines": 8,
    "functions": ["main", "read_lines", "parse_file"]
}
要求：

functions 提取所有 def xxx( 开头的函数名
comment_lines 统计以 # 开头的行（去掉前导空白后）
blank_lines 统计空行
文件不存在抛异常
验收：用你自己写的 stack.py 或 read_lines.py 作为输入测试。
"""
import os.path


def parser(file_path):
    with open(file_path) as file:
        file_name = os.path.basename(file_path)
        all_lines = 0
        comment_lines = 0
        function_lines = []
        blank_lines = 0
        for line in file:
            all_lines += 1
            line_data = line.strip()
            if (not line_data):
                blank_lines += 1
                continue
            if line_data.startswith("def "):
                function_lines.append(line_data[4: line_data.find("(")])
            if line_data.startswith("#"):
                comment_lines += 1
        return {
            "file_name": file_name,
            "total_lines": all_lines,
            "blank_lines": blank_lines,
            "comment_lines": comment_lines,
            "functions": function_lines
        }
