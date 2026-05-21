from ai_client import agent

def review(file_path):
    file_content = read_file(file_path)
    messages = [
        {"role": "system", "content": "你是一个代码审查专家，从正确性和代码质量两个维度审查代码"},
        {"role": "user", "content": "帮我审查下面的代码，文件路径是 {}, 内容是 {}".format(file_path, file_content)}
    ]
    response = agent.invoke({
        "messages": messages
    })
    print(response)


def read_file(file_path):
    with open(file_path, encoding="utf-8") as file:
        return file.read()
