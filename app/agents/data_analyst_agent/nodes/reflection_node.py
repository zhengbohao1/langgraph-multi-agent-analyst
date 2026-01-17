# ──────────────────────────────────────────────
# 7. 节点函数：反思节点（通用）
# ──────────────────────────────────────────────
import json

from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.types import Command

from app.agents.data_analyst_agent.format import ReflectionResult
from app.agents.data_analyst_agent.state import AnalystState
from app.models.LLM_MODEL import ModelInstances
from app.prompts.data_analyst_agent_prompt import DATA_ANALYST_AGENT_SYSTEM_PROMPT, REFLECTION_PROMPT, \
    ANOMALY_REFLECTION_PROMPT, TREND_REFLECTION_PROMPT, STAT_REFLECTION_PROMPT


async def stat_reflection_node(state: AnalystState) :
    """反思统计分析报告的质量"""
    print("🤔 执行统计分析反思节点...")


    analysis_summary = json.dumps(state.get("statistical_result", {}), ensure_ascii=False)
    node_name = "统计分析"
    state["stat_iteration_count"] += 1
    iteration_count = state["stat_iteration_count"]

    prompt = STAT_REFLECTION_PROMPT.format(
        node_name=node_name,
        analysis_summary=analysis_summary[:3000]  # 可适当放宽长度，因为 Markdown 可能较长
    )

    messages = [
        SystemMessage(content=DATA_ANALYST_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ]

    llm = ModelInstances.analyst_llm.with_structured_output(ReflectionResult)
    response = await llm.ainvoke(messages)

    reflection_result = response.model_dump()
    # state["stat_reflection"] = reflection_result

    print(f"统计分析反思 - 当前步数：{iteration_count}，结果：{reflection_result}")

    return Command(update={"stat_iteration_count":iteration_count,"stat_reflection":reflection_result})
# ──────────────────────────────────────────────
# 反思节点：趋势预测专用
# ──────────────────────────────────────────────
async def trend_reflection_node(state: AnalystState):
    """反思趋势预测报告的质量"""
    print("🤔 执行趋势预测反思节点...")

    analysis_summary = json.dumps(state.get("trend_result", {}), ensure_ascii=False)
    node_name = "趋势预测"
    state["trend_iteration_count"] += 1
    iteration_count = state["trend_iteration_count"]

    prompt = TREND_REFLECTION_PROMPT.format(
        node_name=node_name,
        analysis_summary=analysis_summary[:3000]
    )

    messages = [
        SystemMessage(content=DATA_ANALYST_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ]

    llm = ModelInstances.analyst_llm.with_structured_output(ReflectionResult)
    response = await llm.ainvoke(messages)

    reflection_result = response.model_dump()
    state["trend_reflection"] = reflection_result

    print(f"趋势预测反思 - 当前步数：{iteration_count}，结果：{reflection_result}")

    return Command(update={"trend_iteration_count":iteration_count,"trend_reflection":reflection_result})


# ──────────────────────────────────────────────
# 反思节点：异常检测专用
# ──────────────────────────────────────────────
async def anomaly_reflection_node(state: AnalystState) :
    """反思异常检测报告的质量"""
    print("🤔 执行异常检测反思节点...")

    analysis_summary = json.dumps(state.get("anomaly_result", {}), ensure_ascii=False)
    node_name = "异常检测"
    state["anomaly_iteration_count"] += 1
    iteration_count = state["anomaly_iteration_count"]

    prompt = ANOMALY_REFLECTION_PROMPT.format(
        node_name=node_name,
        analysis_summary=analysis_summary[:3000]
    )

    messages = [
        SystemMessage(content=DATA_ANALYST_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ]

    llm = ModelInstances.analyst_llm.with_structured_output(ReflectionResult)
    response = await llm.ainvoke(messages)

    reflection_result = response.model_dump()
    state["anomaly_reflection"] = reflection_result

    print(f"异常检测反思 - 当前步数：{iteration_count}，结果：{reflection_result}")

    return Command(update={"anomaly_iteration_count":iteration_count,"anomaly_reflection":reflection_result})