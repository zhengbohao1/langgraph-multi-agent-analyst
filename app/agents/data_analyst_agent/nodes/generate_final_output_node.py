# ──────────────────────────────────────────────
# 9. 节点函数：生成最终输出
# ──────────────────────────────────────────────
from app.agents.data_analyst_agent.format import DataAnalysisOutput, StatisticalAnalysisResult, \
    TrendPredictionResult, AnomalyDetectionResult
from app.agents.data_analyst_agent.state import AnalystState


async def generate_final_output_node(state: AnalystState) -> AnalystState:
    """生成最终输出节点"""
    print("📊 生成最终分析报告...")

    # 整合所有分析结果
    stat_result = state["statistical_result"]
    trend_result = state["trend_result"]
    anomaly_result = state["anomaly_result"]
    saved_files_path=state["saved_report_paths"]

    # 构建最终输出
    try:
        final_output = DataAnalysisOutput(
            statistical_analysis=stat_result,
            trend_prediction=trend_result,
            anomaly_detection=anomaly_result,
            summary=f"数据分析完成，包含统计分析、趋势预测和异常检测三个维度的结果。各自报告分别保存在{saved_files_path}。"
        )
    except Exception as e:
        # 如果解析失败，使用默认值
        print(f"⚠️ 解析分析结果时出错: {e}")
        final_output = DataAnalysisOutput(
            statistical_analysis=StatisticalAnalysisResult(),
            trend_prediction=TrendPredictionResult(),
            anomaly_detection=AnomalyDetectionResult(),
            summary="数据分析完成"
        )

    state["final_output"] = final_output

    return state