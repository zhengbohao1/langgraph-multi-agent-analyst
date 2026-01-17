from __future__ import annotations

import os
import re
from typing import Any, Dict, Optional

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool

from app.models.LLM_MODEL import ModelInstances


HTML_GENERATION_PROMPT = """
你是一个专业的 HTML 代码生成专家。请根据以下信息生成完整的、精美的 HTML 报表代码。

页面设计要求：
{layout_design}

图表 HTML 链接列表：
{charts_html}

原始数据统计分析报告：
{stat_md}

原始数据趋势预测报告：
{trend_md}

原始数据异常检测报告：
{anomaly_md}


请生成一个完整的 HTML 文件，要求：
1. 包含完整的 <!DOCTYPE html> 声明和 HTML 结构
2. 使用现代化的 CSS 样式（可以内联或使用 CDN，推荐使用 Tailwind CSS CDN）
3. 确保响应式设计，在不同设备上都能良好显示
4. 整合所有提供的图表 HTML 代码
5. 展示数据分析结果和洞察
6. 添加适当的交互组件（如导航菜单、标签页、折叠面板等）
7. 确保代码美观、语义化、可访问性良好
8. 使用现代化的配色方案和字体
9. 添加适当的动画效果和过渡效果（可选）

请直接输出完整的 HTML 代码，不要包含任何 markdown 代码块标记（如 ```html 等），只输出纯 HTML 代码。
"""


@tool
def generate_html_tool(
    layout_design: str,
    stat_md_content: str,
    trend_md_content: str,
    anomaly_md_content: str,
    charts_html: str,
    output_file_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    使用 LLM 生成完整的 HTML 报表代码并保存到本地文件。

    参数说明：
    - layout_design: 布局设计方案的文本描述
    - charts_html: 所有图表的 HTML 链接或代码
    - stat_md_content: 统计分析结果（字符串类型），包含统计分析报告的Markdown内容，包括描述性统计、分组统计、相关性、洞察和可视化建议
    - trend_md_content：趋势预测结果（字符串类型），包含趋势预测报告的Markdown内容，包括时间序列分析、预测值、增长率、洞察和可视化建议
    - anomaly_md_content：异常检测结果（字符串类型），包含异常检测报告的Markdown内容，包括离群值、异常模式、数据质量、洞察和可视化建议
    - output_file_path: 输出文件路径（可选，如果不提供则自动生成）
    :return: 生成结果，包含 html_file_path 和 html_content
    """
    print("进入HTML页面生成工具")
    try:
        # 准备提示词
        prompt = HTML_GENERATION_PROMPT.format(
            layout_design=layout_design,
            charts_html=charts_html,
            stat_md_content=stat_md_content,
            trend_md_content=trend_md_content,
            anomaly_md_content=anomaly_md_content
        )
        
        # 调用 LLM 生成 HTML
        messages = [
            SystemMessage(content="你是一个专业的 HTML 代码生成专家，擅长生成现代化的、响应式的 HTML 报表页面。"),
            HumanMessage(content=prompt),
        ]
        
        llm = ModelInstances.html_llm
        response = llm.invoke(messages)
        
        # 提取 HTML 代码
        html_content = response.content
        
        # 清理可能的 markdown 代码块标记
        # 移除 ```html 和 ``` 标记
        html_content = re.sub(r'```html\s*', '', html_content)
        html_content = re.sub(r'```\s*$', '', html_content, flags=re.MULTILINE)
        html_content = html_content.strip()
        
        # 确保以 <!DOCTYPE 或 <html 开头
        if not (html_content.startswith('<!DOCTYPE') or html_content.startswith('<html')):
            # 如果没有完整的 HTML 结构，尝试提取 HTML 部分
            html_match = re.search(r'(<!DOCTYPE.*?</html>)', html_content, re.DOTALL | re.IGNORECASE)
            if html_match:
                html_content = html_match.group(1)
            else:
                # 如果还是没有，添加基本的 HTML 结构
                html_content = f"""<!DOCTYPE html>
                <html lang="zh-CN">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>数据分析报告</title>
                </head>
                <body>
                {html_content}
                </body>
                </html>"""
        
        # 确定输出文件路径
        if not output_file_path:
            # 如果没有提供路径，使用默认路径
            output_dir = "output/reports"
            os.makedirs(output_dir, exist_ok=True)
            import time
            timestamp = int(time.time())
            output_file_path = os.path.join(output_dir, f"report_{timestamp}.html")
        else:
            # 确保目录存在
            output_dir = os.path.dirname(output_file_path)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
        
        # 保存 HTML 文件
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("HTML报告生成成功")
        
        # 获取文件的绝对路径
        abs_path = os.path.abspath(output_file_path)
        
        return {
            "success": True,
            "html_file_path": abs_path,
            "html_content": html_content[:500] + "..." if len(html_content) > 500 else html_content,  # 只返回前500字符预览
            "file_size": len(html_content),
            "message": f"HTML 报表已成功生成并保存到: {abs_path}",
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "html_file_path": None,
        }


__all__ = ["generate_html_tool"]
