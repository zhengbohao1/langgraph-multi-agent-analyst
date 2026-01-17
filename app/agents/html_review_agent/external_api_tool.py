# ──────────────────────────────────────────────
# 6. 便捷函数
# ──────────────────────────────────────────────
from typing import Dict, Any, Optional

from langchain_core.tools import tool

from app.agents.html_review_agent.format import HTMLReportOutput, DataAnalysisInput, DataQueryInput


from app.agents.html_review_agent.html_agent import HTMLReviewAgent


@tool
def html_report_agent_chat(
        analysis_output: Dict[str, Any],
        query_output: Dict[str, Any],
        thread_id: int,
        user_query: Optional[str] = None,
) :
    """
    生成 HTML 报表的工具函数。

    :param analysis_output: 数据分析结果（字典格式）
    :param query_output: 数据查询结果（字典格式）
    :param thread_id: 线程 ID
    :param user_query: 用户原始查询（可选）
    :return: HTML 报表生成结果
    """
    # 转换为输入格式
    analysis_input = DataAnalysisInput(**analysis_output)
    query_input = DataQueryInput(**query_output)

    # 创建 Agent 并执行
    agent = HTMLReviewAgent(thread_id=str(thread_id))
    result = agent.run(analysis_input, query_input, user_query)

    print(f"HTML 报表生成完成：{result}")
    return result