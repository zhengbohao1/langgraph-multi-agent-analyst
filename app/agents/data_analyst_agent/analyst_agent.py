from __future__ import annotations

import asyncio
from typing import Optional

from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.memory import InMemorySaver

from app.agents.data_analyst_agent.nodes.anomaly_detection_node import anomaly_detection_node
from app.agents.data_analyst_agent.nodes.generate_final_output_node import generate_final_output_node
from app.agents.data_analyst_agent.nodes.reflection_node import  stat_reflection_node, \
    trend_reflection_node, anomaly_reflection_node
from app.agents.data_analyst_agent.nodes.save2md import  save_markdown_reports_node1, \
    save_markdown_reports_node2, save_markdown_reports_node3
from app.agents.data_analyst_agent.nodes.statistical_analysis_node import statistical_analysis_node
from app.agents.data_analyst_agent.nodes.trend_prediction_node import trend_prediction_node
from app.agents.data_analyst_agent.should_continue import  \
    should_continue_after_reflection1, should_continue_after_reflection2, should_continue_after_reflection3
from app.agents.data_analyst_agent.format import DataAnalysisOutput, StatisticalAnalysisResult, TrendPredictionResult, \
    AnomalyDetectionResult, DataQueryOutput

from app.agents.data_analyst_agent.state import  AnalystState


# ──────────────────────────────────────────────
# DataAnalystAgent 类
# ──────────────────────────────────────────────
class DataAnalystAgent:
    """
    基于 LangGraph 的数据分析 Agent。
    
    采用 ReAct + Reflection 设计风格：
    - 统计分析节点 -> 反思节点 -> 趋势预测节点 -> 反思节点 -> 异常检测节点 -> 反思节点 -> 最终输出
    """
    
    def __init__(self, thread_id: Optional[str] = None):
        """
        :param thread_id: 线程 ID，用于状态管理
        """
        self.thread_id = thread_id or "default"
        self.checkpointer = InMemorySaver()
        self.graph = self._build_graph()

    
    def _build_graph(self) :
        """构建 LangGraph 图"""
        workflow = StateGraph(AnalystState)
        
        # 添加节点
        workflow.add_node("statistical_analysis", statistical_analysis_node)
        workflow.add_node("stat_reflection", stat_reflection_node)
        workflow.add_node("trend_prediction", trend_prediction_node)
        workflow.add_node("trend_reflection", trend_reflection_node)
        workflow.add_node("anomaly_detection", anomaly_detection_node)
        workflow.add_node("anomaly_reflection", anomaly_reflection_node)
        workflow.add_node("generate_output", generate_final_output_node)
        workflow.add_node("saveToMd1",save_markdown_reports_node1)
        workflow.add_node("saveToMd2", save_markdown_reports_node2)
        workflow.add_node("saveToMd3", save_markdown_reports_node3)
        # 定义边和路由
        workflow.add_edge(START, "statistical_analysis")
        workflow.add_edge(START, "trend_prediction")
        workflow.add_edge(START, "anomaly_detection")
        
        # 统计分析 -> 反思 -> 根据反思结果决定下一步
        workflow.add_edge("statistical_analysis", "stat_reflection")
        workflow.add_conditional_edges(
            "stat_reflection",
            should_continue_after_reflection1,
            {
                "continue": "saveToMd1",
                "supplement": "statistical_analysis"  # 如果需要补充，返回重新分析
            }
        )
        
        # 趋势预测 -> 反思 -> 根据反思结果决定下一步
        workflow.add_edge("trend_prediction", "trend_reflection")
        workflow.add_conditional_edges(
            "trend_reflection",
            should_continue_after_reflection2,
            {
                "continue": "saveToMd2",
                "supplement": "trend_prediction"
            }
        )
        
        # 异常检测 -> 反思 -> 生成最终输出
        workflow.add_edge("anomaly_detection", "anomaly_reflection")
        workflow.add_conditional_edges(
            "anomaly_reflection",
            should_continue_after_reflection3,
            {
                "continue": "saveToMd3",
                "supplement": "anomaly_detection"
            }
        )

        workflow.add_edge(["saveToMd1","saveToMd2","saveToMd3"],"generate_output")
        workflow.add_edge("generate_output", END)
        
        return workflow.compile(checkpointer=self.checkpointer)
    
    async def run(self, input_data: DataQueryOutput) -> DataAnalysisOutput:
        """
        执行数据分析
        
        :param input_data: 数据查询 Agent 的输出
        :return: 数据分析结果
        """
        # 初始化状态
        initial_state: AnalystState = {
            "input_data": input_data,
            "statistical_result": None,
            "trend_result": None,
            "anomaly_result": None,
            "stat_reflection": None,
            "trend_reflection": None,
            "anomaly_reflection": None,
            "final_output": None,
            "saved_report_paths":[],
            "stat_iteration_count": 0,
            "trend_iteration_count": 0,
            "anomaly_iteration_count": 0,
            "max_iteration":3
        }
        
        # 执行图
        config = {"configurable": {"thread_id": self.thread_id}}
        final_state =await self.graph.ainvoke(initial_state, config)
        
        # 返回最终输出
        if final_state.get("final_output"):
            return final_state["final_output"]
        else:
            # 如果未生成最终输出，返回默认值
            return DataAnalysisOutput(
                statistical_analysis=StatisticalAnalysisResult(),
                trend_prediction=TrendPredictionResult(),
                anomaly_detection=AnomalyDetectionResult(),
                summary="分析未完成"
            )


__all__ = [
    "DataAnalystAgent",
    "DataQueryOutput",
    "DataAnalysisOutput",
    "StatisticalAnalysisResult",
    "TrendPredictionResult",
    "AnomalyDetectionResult",
]


if __name__ == "__main__":
    # 测试示例
    # 注意：这里直接使用 DataQueryOutput，因为它是输入格式
    # 实际使用时，应该从数据查询 Agent 获取输出
    
    # 模拟数据查询 Agent 的输出
    mock_query_output = DataQueryOutput(
        source="csv",
        path="data/test_sales.csv",
        columns=["date", "sales", "region", "quantity", "category"],
        row_count=40,
        all_rows=[
            {"date": "2024-01-01", "sales": 1200, "region": "北京", "quantity": 8, "category": "电子产品"},
            {"date": "2024-01-02", "sales": 950, "region": "上海", "quantity": 5, "category": "家居用品"},
            {"date": "2024-01-03", "sales": 1800, "region": "广州", "quantity": 12, "category": "服装"},
            {"date": "2024-01-04", "sales": 1450, "region": "深圳", "quantity": 10, "category": "电子产品"},
            {"date": "2024-01-05", "sales": 2100, "region": "北京", "quantity": 15, "category": "美妆"},
            {"date": "2024-01-06", "sales": 880, "region": "成都", "quantity": 6, "category": "家居用品"},
            {"date": "2024-01-07", "sales": 1650, "region": "上海", "quantity": 11, "category": "服装"},
            {"date": "2024-01-08", "sales": 2300, "region": "广州", "quantity": 18, "category": "电子产品"},
            {"date": "2024-01-09", "sales": 1100, "region": "深圳", "quantity": 7, "category": "美妆"},
            {"date": "2024-01-10", "sales": 1950, "region": "北京", "quantity": 14, "category": "家居用品"},
            {"date": "2024-01-11", "sales": 750, "region": "成都", "quantity": 4, "category": "服装"},
            {"date": "2024-01-12", "sales": 2600, "region": "上海", "quantity": 20, "category": "电子产品"},
            {"date": "2024-01-13", "sales": 1350, "region": "广州", "quantity": 9, "category": "美妆"},
            {"date": "2024-01-14", "sales": 1700, "region": "深圳", "quantity": 12, "category": "家居用品"},
            {"date": "2024-01-15", "sales": 980, "region": "北京", "quantity": 6, "category": "服装"},
            {"date": "2024-01-16", "sales": 2450, "region": "成都", "quantity": 17, "category": "电子产品"},
            {"date": "2024-01-17", "sales": 1120, "region": "上海", "quantity": 8, "category": "美妆"},
            {"date": "2024-01-18", "sales": 1890, "region": "广州", "quantity": 13, "category": "家居用品"},
            {"date": "2024-01-19", "sales": 820, "region": "深圳", "quantity": 5, "category": "服装"},
            {"date": "2024-01-20", "sales": 2750, "region": "北京", "quantity": 22, "category": "电子产品"},
            {"date": "2024-01-21", "sales": 1400, "region": "成都", "quantity": 10, "category": "美妆"},
            {"date": "2024-01-22", "sales": 1600, "region": "上海", "quantity": 11, "category": "家居用品"},
            {"date": "2024-01-23", "sales": 1050, "region": "广州", "quantity": 7, "category": "服装"},
            {"date": "2024-01-24", "sales": 2200, "region": "深圳", "quantity": 16, "category": "电子产品"},
            {"date": "2024-01-25", "sales": 930, "region": "北京", "quantity": 6, "category": "美妆"},
            {"date": "2024-01-26", "sales": 2550, "region": "成都", "quantity": 19, "category": "家居用品"},
            {"date": "2024-01-27", "sales": 1280, "region": "上海", "quantity": 9, "category": "服装"},
            {"date": "2024-01-28", "sales": 1980, "region": "广州", "quantity": 14, "category": "电子产品"},
            {"date": "2024-01-29", "sales": 780, "region": "深圳", "quantity": 5, "category": "美妆"},
            {"date": "2024-01-30", "sales": 2850, "region": "北京", "quantity": 23, "category": "家居用品"},
            {"date": "2024-01-31", "sales": 1620, "region": "成都", "quantity": 12, "category": "服装"},
            {"date": "2024-02-01", "sales": 3100, "region": "上海", "quantity": 25, "category": "电子产品"},
            {"date": "2024-02-02", "sales": 1150, "region": "广州", "quantity": 8, "category": "美妆"},
            {"date": "2024-02-03", "sales": 2050, "region": "深圳", "quantity": 15, "category": "家居用品"},
            {"date": "2024-02-04", "sales": 890, "region": "北京", "quantity": 6, "category": "服装"},
            {"date": "2024-02-05", "sales": 3400, "region": "成都", "quantity": 28, "category": "电子产品"},
            {"date": "2024-02-06", "sales": 1330, "region": "上海", "quantity": 10, "category": "美妆"},
            {"date": "2024-02-07", "sales": 2180, "region": "广州", "quantity": 16, "category": "家居用品"},
            {"date": "2024-02-08", "sales": 960, "region": "深圳", "quantity": 7, "category": "服装"},
            {"date": "2024-02-09", "sales": 3650, "region": "北京", "quantity": 30, "category": "电子产品"},
        ]
    )
    
    # 创建数据分析 Agent
    analyst = DataAnalystAgent(thread_id="test_123")
    
    # 执行分析
    result = asyncio.run(analyst.run(mock_query_output))
    
    # 打印结果
    print("\n" + "="*50)
    print("数据分析结果：")
    print("="*50)
    print(result.model_dump_json(indent=2, ensure_ascii=False))
