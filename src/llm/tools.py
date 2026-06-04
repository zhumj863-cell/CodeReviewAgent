import subprocess
import tempfile

from langchain_core.tools import tool

LINTER_CONFIG = {
    "python": {"cmd": ["python3", "-m", "flake8", "--max-line-length=120"], "ext": ".py"},
    "javascript": {"cmd": ["eslint"], "ext": ".js"},
    "typescript": {"cmd": ["eslint"], "ext": ".ts"},
}


@tool
def run_lint(code: str, language: str) -> str:
    """对代码运行静态检查工具. language支持: python, javascript, typescript"""
    print(f"zmj run_lint called, language: {language}")
    config = LINTER_CONFIG.get(language)
    if not config:
        return f"不支持{language}的lint检查"
    with tempfile.NamedTemporaryFile(mode="w", suffix=config["ext"], delete=False) as f:
        f.write(code)
        f.flush()
        try:
            result = subprocess.run(
                config["cmd"] + [f.name],
                capture_output=True, text=True, timeout=10
            )
            output = result.stdout or result.stderr
            return output.strip() if output.strip() else "检查通过, 无问题"
        except subprocess.TimeoutExpired:
            return "检查超时"
        except FileNotFoundError:
            return f"{config['cmd'][0]}未安装"
