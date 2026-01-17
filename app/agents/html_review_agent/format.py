# ──────────────────────────────────────────────
# 1. 输入格式定义
# ──────────────────────────────────────────────
from typing import Dict, Any, List, Optional

from pydantic import BaseModel, Field


class DataAnalysisInput(BaseModel):
    """数据分析 Agent 的输出格式（简化版，用于输入）"""
    statistical_analysis: Dict[str, Any] = Field(default_factory=dict)
    trend_prediction: Dict[str, Any] = Field(default_factory=dict)
    anomaly_detection: Dict[str, Any] = Field(default_factory=dict)
    overall_insights: List[str] = Field(default_factory=list)
    summary: str = Field(default="")


class DataQueryInput(BaseModel):
    """数据查询 Agent 的输出格式（简化版，用于输入）"""
    source: str = Field(default="")
    path: str = Field(default="")
    columns: List[str] = Field(default_factory=list)
    row_count: int = Field(default=0)
    all_rows: List[Dict[str, Any]] = Field(default_factory=list)


# ──────────────────────────────────────────────
# 2. 输出格式定义
# ──────────────────────────────────────────────
class HTMLReportOutput(BaseModel):
    """HTML 报表生成 Agent 的最终输出格式"""
    html_link: str = Field(description="生成的 HTML 报表链接")
    charts_generated: List[Dict[str, Any]] = Field(default_factory=list, description="生成的图表列表")
    sections: List[Dict[str, Any]] = Field(default_factory=list, description="报表章节列表")
    summary: str = Field(description="报表生成摘要")