# ──────────────────────────────────────────────
# 2. 输出格式（固定格式，方便后续 HTML 报表生成）
# ──────────────────────────────────────────────
from typing import Dict, List, Any, Literal, TypedDict, Optional

from pydantic import BaseModel, Field

# class DescriptionStats(BaseModel):
#     """描述性统计指标"""
#     mean: Optional[float] = Field(None, description="均值")
#     median: Optional[float] = Field(None, description="中位数")
#     std: Optional[float] = Field(None, description="标准差")
#     min: Optional[float] = Field(None, description="最小值")
#     max: Optional[float] = Field(None, description="最大值")
#     q25: Optional[float] = Field(None, description="25% 分位数")
#     q75: Optional[float] = Field(None, description="75% 分位数")


class StatisticalAnalysisResult(BaseModel):
    """统计分析结果"""
    descriptive_stats: List[Dict[str, Any]] = Field(
        default_factory=list,  # 必须是 list，不能是 dict
        description="各字段的描述性统计"
    )
    group_stats: List[Dict[str, Any]] = Field(default_factory=list)
    correlations: List[Dict[str, Any]] = Field(default_factory=list)
    insights: List[str] = Field(default_factory=list)
    visualization_suggestions: List[Dict[str, Any]] = Field(default_factory=list)



class TrendPredictionResult(BaseModel):
    """趋势预测结果"""
    time_series_analysis: Dict[str, Any] = Field(default_factory=dict)
    predictions: List[Dict[str, Any]] = Field(default_factory=list)
    growth_rates: List[Dict[str, Any]] = Field(default_factory=list)
    insights: List[str] = Field(default_factory=list)
    visualization_suggestions: List[Dict[str, Any]] = Field(default_factory=list)


class AnomalyDetectionResult(BaseModel):
    """异常检测结果"""
    """异常检测结果"""
    outliers: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="异常值列表，每个元素包含row_index (int), field (str), value (Union[int, float]), method (str), reason (str)"
    )
    anomaly_patterns: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="异常模式列表，每个元素包含pattern_type (str), description (str), affected_rows (List[int]), severity (str)"
    )
    data_quality: Dict[str, Any] = Field(
        default_factory=dict,
        description="数据质量指标，包含missing_values (Dict), duplicates (int), format_errors (List)"
    )
    insights: List[str] = Field(default_factory=list, description="洞察总结")
    visualization_suggestions: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="可视化建议列表，每个元素包含chart_type (str), title (str), x_axis (str), y_axis (str), highlight_outliers (Optional[bool]), description (str)"
    )


class ReflectionResult(BaseModel):
    """反思节点结果"""
    completeness_score: int = Field(description="完成度分数 0-100")
    is_complete: bool = Field(description="是否已完成")
    missing_aspects: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    next_action: Literal["continue", "supplement"] = Field(description="下一步动作")


class DataAnalysisOutput(BaseModel):
    """数据分析 Agent 的最终输出格式"""
    statistical_analysis: Any = Field(description="统计分析结果")
    trend_prediction: Any = Field(description="趋势预测结果")
    anomaly_detection: Any = Field(description="异常检测结果")
    summary: str = Field(description="分析摘要")

# ──────────────────────────────────────────────
# 1. 输入格式（来自数据查询 Agent）
# ──────────────────────────────────────────────
class DataQueryOutput(BaseModel):
    """数据查询 Agent 的输出格式"""
    source: str = Field(description="文件类型，如csv")
    path: str = Field(description="文件举例路径，如data/sales.csv")
    columns: List[str] = Field(description="文件中的列表属性")
    row_count: int = Field(description="文件的行数")
    all_rows: List[Dict[str, Any]] = Field(description="展示所有行的内容")
