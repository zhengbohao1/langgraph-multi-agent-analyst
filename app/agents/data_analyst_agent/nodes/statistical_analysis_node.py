# ──────────────────────────────────────────────
# 4. 节点函数：统计分析
# ──────────────────────────────────────────────
import json


from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.types import Command


from app.agents.data_analyst_agent.state import AnalystState
from app.models.LLM_MODEL import ModelInstances
from app.prompts.data_analyst_agent_prompt import STATISTICAL_ANALYSIS_PROMPT, DATA_ANALYST_AGENT_SYSTEM_PROMPT


async def statistical_analysis_node(state: AnalystState) :
    """统计分析节点"""
    print("🔍 执行统计分析节点...")

    input_data = state["input_data"]

    # 准备提示词
    prompt = STATISTICAL_ANALYSIS_PROMPT.format(
        source=input_data.source,
        path=input_data.path,
        columns=", ".join(input_data.columns),
        row_count=input_data.row_count,
        reflection="" if not state["stat_reflection"] else state["stat_reflection"]
    )

    # 将数据行转换为字符串，方便 LLM 理解
    sample_rows = input_data.all_rows[:100]  # 限制样本数量，避免 token 过多
    data_sample = json.dumps(sample_rows, ensure_ascii=False, indent=2)
    prompt += f"\n\n数据样本（前100行）：\n{data_sample}"
    # print(f"检查提示词：{prompt}")

    # 调用 LLM
    messages = [
        SystemMessage(content=DATA_ANALYST_AGENT_SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ]

    llm = ModelInstances.analyst_llm
    response =await llm.ainvoke(messages)

    #保存md格式输出

    return Command(update={"statistical_result":response.content})