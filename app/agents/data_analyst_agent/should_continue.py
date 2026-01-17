# ──────────────────────────────────────────────
# 8. 路由函数：决定是否继续或补充
# ──────────────────────────────────────────────
from typing import Literal

from langgraph.types import Command

from app.agents.data_analyst_agent.state import AnalystState


async def should_continue_after_reflection1(state: AnalystState) :
    """根据反思结果决定下一步"""

    reflection = state.get("stat_reflection", {})
    iteration=state.get("stat_iteration_count")

    # 如果迭代次数过多，则直接往下走了

    if iteration == state["max_iteration"]:
        print("达到最大迭代次数，考虑直接结束该操作")
        return "continue"

    # 正常情况下继续根据llm的决定走
    next_action = reflection.get("next_action", "continue")
    is_complete = reflection.get("is_complete", True)

    if next_action == "supplement" or not is_complete:
        return "supplement"
    return "continue"


async def should_continue_after_reflection2(state: AnalystState):
    """根据反思结果决定下一步"""

    reflection = state.get("trend_reflection", {})
    iteration = state.get("trend_iteration_count")

    # 如果迭代次数过多，则直接往下走了

    if iteration == state["max_iteration"]:
        print("达到最大迭代次数，考虑直接结束该操作")
        return "continue"

    # 正常情况下继续根据llm的决定走
    next_action = reflection.get("next_action", "continue")
    is_complete = reflection.get("is_complete", True)

    if next_action == "supplement" or not is_complete:
        return "supplement"
    return "continue"

async def should_continue_after_reflection3(state: AnalystState):
    """根据反思结果决定下一步"""

    reflection = state.get("anomaly_reflection", {})
    iteration = state.get("anomaly_iteration_count")

    # 如果迭代次数过多，则直接往下走了

    if iteration == state["max_iteration"]:
        print("达到最大迭代次数，考虑直接结束该操作")
        return "continue"

    # 正常情况下继续根据llm的决定走
    next_action = reflection.get("next_action", "continue")
    is_complete = reflection.get("is_complete", True)

    if next_action == "supplement" or not is_complete:
        return "supplement"
    return "continue"
