from pathlib import Path
from typing import Optional
from langchain_core.tools import tool


@tool
def read_md(
    filepath: str,
    encoding: str = "utf-8",
) -> str:
    """
    读取指定路径的 Markdown (.md) 文件并返回其内容。

    Args:
        filepath (str): Markdown 文件的路径（绝对路径或相对于当前工作目录的相对路径）
        encoding (str, optional): 文件编码方式，默认为 "utf-8"

    Returns:
        str: 文件的完整文本内容

    Raises:
        FileNotFoundError: 当文件不存在时
        IsADirectoryError: 当路径指向的是文件夹而非文件时
        UnicodeDecodeError: 当文件编码与指定编码不匹配时
        PermissionError: 当没有读取权限时

    Example:
        content = read_md(filepath="reports/统计分析报告_20250117.md")
    """
    path = Path(filepath)
    print(f"正在读取{filepath}文件")

    # 基本路径检查
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {path}")

    if not path.is_file():
        raise IsADirectoryError(f"路径指向的是目录而非文件: {path}")

    # 尝试读取文件
    try:
        content = path.read_text(encoding=encoding)
        content = content.strip()
        print(f"{filepath}文件正常读取成功")
        return content

    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(
            f"文件编码错误，无法使用 {encoding} 解码文件 {path}。\n"
            f"建议尝试其他编码（如 'gbk', 'utf-8-sig'）或检查文件是否损坏。"
        ) from e

    except PermissionError as e:
        raise PermissionError(f"没有权限读取文件: {path}") from e

    except Exception as e:
        raise RuntimeError(f"读取 Markdown 文件失败: {path}\n原因: {str(e)}") from e