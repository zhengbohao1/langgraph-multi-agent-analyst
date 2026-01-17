# ──────────────────────────────────────────────
# 6. 节点函数：异常检测
# ──────────────────────────────────────────────
import json

from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.types import Command

from app.agents.data_analyst_agent.format import AnomalyDetectionResult
from app.models.LLM_MODEL import ModelInstances
from app.prompts.data_analyst_agent_prompt import ANOMALY_DETECTION_PROMPT, DATA_ANALYST_AGENT_SYSTEM_PROMPT
from app.agents.data_analyst_agent.state import AnalystState

async def anomaly_detection_node(state: AnalystState) :
    """异常检测节点"""
    print("⚠️ 执行异常检测节点...")

    input_data = state["input_data"]

    # 准备提示词
    prompt = ANOMALY_DETECTION_PROMPT.format(
        source=input_data.source,
        path=input_data.path,
        columns=", ".join(input_data.columns),
        row_count=input_data.row_count,
        all_rows=input_data.all_rows,
        reflection="" if not state["anomaly_reflection"] else state["anomaly_reflection"]
    )

    # 将数据行转换为字符串
    sample_rows = input_data.all_rows[:100]
    data_sample = json.dumps(sample_rows, ensure_ascii=False, indent=2)
    prompt += f"\n\n数据样本（前100行）：\n{data_sample}"

    # 调用 LLM
    messages = [
        SystemMessage(content=DATA_ANALYST_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ]

    llm = ModelInstances.analyst_llm
    response = await llm.ainvoke(messages)

    return Command(update={"anomaly_result":response.content})