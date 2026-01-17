from __future__ import annotations

import os
from typing import Any, Dict, Optional

import pandas as pd

from langchain_core.tools import tool


@tool
def _read_table_file(
    path: str,
    *,
    file_type: Optional[str] = None,
    encoding: str = "utf-8",
) -> Dict[str, Any]:
    """
    读取本地 CSV/Excel，返回结构化数据。
    "读取本地 CSV/Excel 文件并返回结构化数据。"
    "输入应包含文件路径，例如：'path=data/sales.csv'。"

    - 自动根据后缀推断类型，或通过 file_type 指定：csv / excel
    - 返回 {"columns": [...], "rows": [ {...}, ... ]}
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"文件不存在: {path}")

    ext = (os.path.splitext(path)[1] or "").lower()
    _type = file_type or ext.replace(".", "")

    if _type not in {"csv", "xlsx", "xls", "excel"}:
        raise ValueError(f"暂不支持的文件类型: {_type}")

    if _type == "csv":
        df = pd.read_csv(path, encoding=encoding)
    else:
        df = pd.read_excel(path)

    df.columns = [
        str(c).strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns
    ]
    return {
        "columns": list(df.columns),
        "rows": df.to_dict(orient="records"),
        "path": path,
        "type": "csv" if _type == "csv" else "excel",
    }

