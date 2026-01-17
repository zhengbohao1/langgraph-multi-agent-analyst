import operator
from typing import TypedDict, Optional, Any, Dict, List, Annotated, Sequence

from app.agents.data_analyst_agent.format import DataAnalysisOutput, DataQueryOutput


class AnalystState(TypedDict):
    """数据分析 Agent 的状态"""
    # 输入数据
    input_data: DataQueryOutput

    # 中间分析结果
    statistical_result: Optional[str]
    trend_result: Optional[str]
    anomaly_result: Optional[str]

    # 反思结果
    stat_reflection: Optional[Dict[str, Any]]
    trend_reflection: Optional[Dict[str, Any]]
    anomaly_reflection: Optional[Dict[str, Any]]

    # 最终输出
    final_output: Optional[DataAnalysisOutput]
    saved_report_paths: Annotated[List[str], operator.add]

    # 控制流
    stat_iteration_count: int
    trend_iteration_count: int
    anomaly_iteration_count: int
    max_iteration: int


__all__=[AnalystState]