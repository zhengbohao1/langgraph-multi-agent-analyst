from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool

from app.models.LLM_MODEL import ModelInstances
from app.prompts.html_review_agent_prompt import HTML_REVIEW_AGENT_SYSTEM_PROMPT, PLANNING_PROMPT


# ──────────────────────────────────────────────
# 3. 规划工具（Plan Tool）
# ──────────────────────────────────────────────
@tool
async def create_execution_plan(
        stat_md_content: str,
        trend_md_content: str,
        anomaly_md_content:str,
) -> str:
    """
    创建具体的任务执行计划，任务为 HTML 报表的生成。
    
    参数说明：
    - stat_md_content: 统计分析md文档读取结果（字符串类型），包含统计分析报告的Markdown内容，包括描述性统计、分组统计、相关性、洞察和可视化建议
    - trend_md_content：趋势预测md文档读取结果（字符串类型），包含趋势预测报告的Markdown内容，包括时间序列分析、预测值、增长率、洞察和可视化建议
    - anomaly_md_content：异常检测md文档结果（字符串类型），包含异常检测报告的Markdown内容，包括离群值、异常模式、数据质量、洞察和可视化建议
    
    返回：执行计划的文本描述（字符串格式）
    """
    try:
        print(f"进入规划工具")
        
        # 直接使用字符串，不需要复杂的 JSON 解析
        # 准备规划提示词（直接使用文本描述）
        prompt = PLANNING_PROMPT.format(
            # query_output=query_output[:2000] if len(query_output) > 2000 else query_output,  # 限制长度
            stat_md_content=stat_md_content,
            trend_md_content=trend_md_content,
            anomaly_md_content=anomaly_md_content
        )

        # 调用 LLM 生成计划
        messages = [
            SystemMessage(content=HTML_REVIEW_AGENT_SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]

        llm = ModelInstances.html_llm
        response = await llm.ainvoke(messages)

        plan = response.content.strip()
        print(f"规划工具设计的plan如下：\n{plan[:500]}...")  # 只打印前500字符

        # 直接返回计划字符串，而不是包装在字典中
        return plan
    except Exception as e:
        error_msg = f"规划工具执行失败: {str(e)}"
        print(error_msg)
        return error_msg