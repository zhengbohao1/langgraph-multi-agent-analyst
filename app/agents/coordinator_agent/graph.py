from __future__ import annotations

import asyncio
from typing import TypedDict, Annotated, Optional, Any
from operator import itemgetter

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from app.agents.data_analyst_agent.analyst_agent import DataAnalystAgent
from app.agents.data_analyst_agent.format import DataAnalysisOutput
from app.agents.data_query_agent.query_agent import json_response_format,DataQueryAgent
from app.agents.html_review_agent.html_agent import HTMLReviewAgent


# ──────────────────────────────────────────────
# 整体状态定义
# ──────────────────────────────────────────────
class OverallState(TypedDict):
    user_query: str  # 用户原始问题
    thread_id: str  # 统一线程ID

    query_result: Optional[json_response_format]  # 数据获取结果
    analyst_result: Optional[DataAnalysisOutput]  # 分析结果（结构化）

    stat_md_path: Optional[str]  # 统计 md 文件路径
    trend_md_path: Optional[str]
    anomaly_md_path: Optional[str]

    html_result: Any  # HTML Agent 最终返回（可根据需要调整类型）
    final_report_path: Optional[str]  # 可选：最终 HTML 文件路径（如果有返回）


# ──────────────────────────────────────────────
# 节点函数（每个节点调用对应 Agent）
# ──────────────────────────────────────────────

async def call_data_query_node(state: OverallState) -> OverallState:
    agent = DataQueryAgent(
        thread_id=state["thread_id"],
        userinput=state["user_query"]
    )
    result = await agent.run()
    return {"query_result": result}


async def call_data_analyst_node(state: OverallState) -> OverallState:
    agent = DataAnalystAgent(thread_id=state["thread_id"])

    # 注意：你的 DataAnalystAgent.run() 期望 DataQueryOutput
    # 这里假设 json_response_format 可以直接兼容或稍作转换
    # 如果字段不完全匹配，需要做字段映射
    input_for_analyst = state["query_result"]  # 或做转换

    result = await agent.run(input_for_analyst)

    # 假设你的分析 Agent 内部已经把 md 路径写入了某个地方
    # 这里演示一种常见做法：从 result 中取，或从已知路径构造
    # 你可以根据实际情况替换下面三行
    base_path = f"reports/{state['thread_id']}"
    return {
        "analyst_result": result,
        "stat_md_path": f"{base_path}/统计分析报告.md",
        "trend_md_path": f"{base_path}/趋势预测报告.md",
        "anomaly_md_path": f"{base_path}/异常检测报告.md",
    }


async def call_html_report_node(state: OverallState) -> OverallState:
    agent = HTMLReviewAgent(thread_id=state["thread_id"])

    result = await agent.run(
        stat_md_path=state["stat_md_path"],
        trend_md_path=state["trend_md_path"],
        anomaly_md_path=state["anomaly_md_path"],
        user_query=state["user_query"],
    )

    # 根据你的 HTML Agent 返回格式调整
    # 这里假设返回的是最后一条消息，或有 .content 属性
    report_content = getattr(result, "content", result) if result else None

    return {"html_result": report_content}


# ──────────────────────────────────────────────
# Supervisor 图构建
# ──────────────────────────────────────────────
def build_supervisor_graph():
    workflow = StateGraph(OverallState)

    workflow.add_node("data_query", call_data_query_node)
    workflow.add_node("data_analyst", call_data_analyst_node)
    workflow.add_node("html_report", call_html_report_node)

    # 严格串行流
    workflow.add_edge(START, "data_query")
    workflow.add_edge("data_query", "data_analyst")
    workflow.add_edge("data_analyst", "html_report")
    workflow.add_edge("html_report", END)

    return workflow.compile(checkpointer=InMemorySaver())


# ──────────────────────────────────────────────
# 使用示例
# ──────────────────────────────────────────────
async def run_full_pipeline(user_query: str, thread_id: str = "demo_001"):
    graph = build_supervisor_graph()

    initial_state = {
        "user_query": user_query,
        "thread_id": thread_id,
        "query_result": None,
        "analyst_result": None,
        "stat_md_path": None,
        "trend_md_path": None,
        "anomaly_md_path": None,
        "html_result": None,
    }

    config = {"configurable": {"thread_id": thread_id}}

    final_state = await graph.ainvoke(initial_state, config)

    return final_state


if __name__ == "__main__":
    query = "分析最近一个月的销售数据趋势和异常点"
    result = asyncio.run(run_full_pipeline(query, thread_id="test_20260117"))

    print("最终状态：")
    print(result)