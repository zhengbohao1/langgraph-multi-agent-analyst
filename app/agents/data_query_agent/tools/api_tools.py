from __future__ import annotations

from typing import Any, Dict, Optional

import requests

import pandas as pd
from langchain_core.tools import tool


def _extract_data_by_path(obj: Any, data_path: Optional[str]) -> Any:
    """从嵌套 JSON 中按 data_path 提取数据，例如 data.items。"""
    if not data_path:
        return obj
    cur = obj
    for key in data_path.split("."):
        if isinstance(cur, dict):
            cur = cur.get(key)
        else:
            raise KeyError(f"无法在非字典对象上取 key: {key}")
    return cur


def _request_api(
    url: str,
    method: str = "GET",
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    json_body: Optional[Dict[str, Any]] = None,
    data_path: Optional[str] = None,
) -> Dict[str, Any]:
    resp = requests.request(
        method=method,
        url=url,
        params=params,
        headers=headers,
        json=json_body,
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    data = _extract_data_by_path(data, data_path)

    # 尝试归一化为表格结构
    try:
        df = pd.json_normalize(data)
        df.columns = [
            str(c).strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns
        ]
        return {
            "columns": list(df.columns),
            "rows": df.to_dict(orient="records"),
            "url": url,
            "method": method,
            "data_path": data_path,
        }
    except Exception:
        # 如果无法表格化，就直接返回原始数据
        return {
            "raw": data,
            "url": url,
            "method": method,
            "data_path": data_path,
        }


import json

@tool
def _api_reader_tool(input_str: str) -> Dict[str, Any]:
    """
    构建一个用于 ReAct Agent 的 HTTP API 读取 Tool。

    由于 ReAct 以自然语言规划，这里简化为：
    - 输入字符串的格式为一个简单的 JSON 字符串
      例如：{"url": "...", "method": "GET", "data_path": "data.items"}
    """
    payload = json.loads(input_str)
    url = payload["url"]
    method = payload.get("method", "GET")
    params = payload.get("params")
    headers = payload.get("headers")
    json_body = payload.get("json_body")
    data_path = payload.get("data_path")
    return _request_api(
        url=url,
        method=method,
        params=params,
        headers=headers,
        json_body=json_body,
        data_path=data_path,
    )

