from __future__ import annotations

from typing import Optional

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool

from app.models.LLM_MODEL import ModelInstances
from app.prompts.html_review_agent_prompt import LAYOUT_DESIGN_PROMPT

USER_PORMPT = """
我将提供给你以下四块数据，分别为三个数据分析报告内容，和一个图表链接汇总，请你为我设计页面布局。

统计分析报告内容：
{stat_md_content}

趋势预测报告内容：
{trend_md_content}

异常检测报告内容：
{anomaly_md_content}

图表链接：
{charts_html}
"""

@tool
def design_layout_tool(
    stat_md_content: str,
    trend_md_content: str,
    anomaly_md_content:str,
    charts_html:str
) -> str:
    """
    根据数据分析报告结果，和图表链接，设计页面排版风格方案。

    参数说明：
    - charts_html: 所有图表的 HTML 链接或代码（字符串类型）
    - stat_md_content: 统计分析结果（字符串类型），包含统计分析报告的Markdown内容，包括描述性统计、分组统计、相关性、洞察和可视化建议
    - trend_md_content：趋势预测结果（字符串类型），包含趋势预测报告的Markdown内容，包括时间序列分析、预测值、增长率、洞察和可视化建议
    - anomaly_md_content：异常检测结果（字符串类型），包含异常检测报告的Markdown内容，包括离群值、异常模式、数据质量、洞察和可视化建议
    :return: 页面布局设计方案（字符串格式），包含详细的布局、配色、排版等说明
    """
    print("进入排版工具，规划排版")
    try:
        # 准备提示词
        prompt = USER_PORMPT.format(
            stat_md_content=stat_md_content,
            trend_md_content=trend_md_content,
            anomaly_md_content=anomaly_md_content,
            charts_html=charts_html
        )
        
        # 调用 LLM 生成布局设计方案
        messages = [
            SystemMessage(content=LAYOUT_DESIGN_PROMPT),
            HumanMessage(content=prompt),
        ]
        
        llm = ModelInstances.html_llm
        response = llm.invoke(messages)
        
        # 提取布局设计方案（纯文本）
        layout_design = response.content.strip()
        
        # 清理可能的 markdown 标记
        import re
        layout_design = re.sub(r'```[a-z]*\s*', '', layout_design)
        layout_design = layout_design.strip()

        print(f"布局规划如下：{layout_design}")
        return layout_design
    except Exception as e:
        # 如果生成失败，返回一个基础的布局设计方案
        return f"""
页面布局设计方案：

整体布局：采用现代化的卡片式布局，使用响应式网格系统。

配色方案：
- 主色调：#1890ff（蓝色，代表专业和可信）
- 辅助色：#52c41a（绿色，代表增长和积极）
- 背景色：#f0f2f5（浅灰色，提供舒适的阅读体验）
- 文字颜色：#262626（深灰色，确保良好的可读性）

字体和排版：
- 字体族：PingFang SC, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif
- 主标题：2.5em，加粗
- 章节标题：1.8em，加粗
- 正文：1em，行高 1.6

章节布局：
1. 页面头部：包含报告标题和摘要，使用渐变背景
2. 统计分析章节：使用卡片式布局，每个统计指标一个卡片
3. 趋势预测章节：图表居中显示，下方展示预测数据表格
4. 异常检测章节：使用列表式布局，突出显示异常项

图表展示：
- 图表使用响应式容器，最大宽度 100%
- 图表之间使用适当的间距（20px）
- 图表标题位于图表上方，使用中等大小的字体

响应式设计：
- 桌面端（>768px）：多列布局，充分利用屏幕空间
- 移动端（≤768px）：单列布局，确保内容清晰可读

错误信息：{str(e)}
"""


__all__ = ["design_layout_tool"]
