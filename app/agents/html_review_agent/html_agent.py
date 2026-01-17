from __future__ import annotations

import asyncio
import os
from typing import Optional

from langchain.agents import create_agent
from langchain.agents.middleware import (
    SummarizationMiddleware,
    ToolRetryMiddleware,
)
from langchain_core.messages import HumanMessage


from app.agents.html_review_agent.format import DataAnalysisInput, DataQueryInput, HTMLReportOutput
from app.agents.html_review_agent.tools.chart_generation_tool import get_mcp_tools
from app.agents.html_review_agent.tools.html_generation_tool import generate_html_tool
from app.agents.html_review_agent.tools.layout_tool import design_layout_tool
from app.agents.html_review_agent.tools.plan_tool import create_execution_plan
from app.models.LLM_MODEL import ModelInstances
from app.prompts.html_review_agent_prompt import (
    HTML_REVIEW_AGENT_SYSTEM_PROMPT, USER_PORMPT,
)

# ──────────────────────────────────────────────
# 5. HTMLReviewAgent 类（Plan and Execute 范式）
# ──────────────────────────────────────────────
class HTMLReviewAgent:
    """
    基于 LangChain Plan and Execute 范式的 HTML 报表生成 Agent。
    
    工作流程：
    1. 规划阶段：分析输入，制定执行计划
    2. 执行阶段：按计划逐步执行（生成图表、设计布局、生成 HTML 等）
    3. 反思阶段：每完成一个步骤，进行反思和评估
    4. 最终输出：整合所有组件，生成完整的 HTML 报表
    """
    
    def __init__(self, thread_id: Optional[str] = None, output_dir: str = "output/reports"):
        """
        :param thread_id: 线程 ID，用于状态管理
        :param output_dir: 输出目录
        """
        self.thread_id = thread_id or "default"
        self.output_dir = output_dir
        
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 工具列表（MCP 工具在运行时动态获取）
        self.base_tools = [
            create_execution_plan,
            generate_html_tool,
            design_layout_tool,
        ]
        
        # MCP 工具将在运行时动态加载
        self.mcp_tools = None
        
        # 构建 Agent（延迟到 run 方法中，以便异步加载 MCP 工具）
        self.agent = None
    
    async def _build_agent(self):
        """构建 Plan and Execute Agent（异步方法，用于加载 MCP 工具）"""
        # 动态加载 MCP 工具
        if self.mcp_tools is None:
            try:
                self.mcp_tools = await get_mcp_tools()
            except Exception as e:
                print(f"警告：加载 MCP 工具失败: {e}，将继续使用基础工具")
                self.mcp_tools = []
        
        # 合并所有工具
        all_tools = self.base_tools + (self.mcp_tools if self.mcp_tools else [])

        print(f"所有工具如下：{all_tools}")
        
        # 使用 create_agent 创建 Agent，支持 Plan and Execute 模式
        agent = create_agent(
            model=ModelInstances.html_llm,
            tools=all_tools,
            system_prompt=HTML_REVIEW_AGENT_SYSTEM_PROMPT,
        )
        return agent
    
    async def run(
        self,
        stat_md_path: str,
        trend_md_path: str,
        anomaly_md_path:str,
        user_query:str,
    ) :
        """
        执行 HTML 报表生成
        
        :param analysis_output: 数据分析结果
        :param query_output: 数据查询结果
        :param user_query: 用户原始查询（可选）
        :return: HTML 报表生成结果
        """
        
        user_input = USER_PORMPT.format(stat_md_file_path=stat_md_path,trend_md_file_path=trend_md_path,anomaly_md_file_path=anomaly_md_path,user_query=user_query,output_dir=self.output_dir)
        # 如果 Agent 还未构建，先构建（异步加载 MCP 工具）
        if self.agent is None:
            self.agent = await self._build_agent()
        
        # 执行 Agent

        # 异步调用
        response = await self.agent.ainvoke(
            {"messages": [HumanMessage(content=user_input)]},
        )
        
        # 从响应中提取结果
        # 注意：实际实现可能需要根据 Agent 的响应格式进行调整
        messages = response.get("messages", [])
        last_message = messages[-1] if messages else None

        # 构建输出
        return last_message


if __name__ == "__main__":
    # 测试示例
    
    # 创建 Agent
    agent = HTMLReviewAgent(thread_id="test_123")
    
    # 执行生成
    result = asyncio.run(agent.run("app/agents/data_analyst_agent/reports/统计分析报告_20260117_151505.md",
                                   "app/agents/data_analyst_agent/reports/趋势预测报告_20260117_151505.md",
                                   "app/agents/data_analyst_agent/reports/异常检测报告_20260117_151359.md",
                                   "生成完整的数据分析报告，HTML文件"))
    
    # 打印结果
    print("\n" + "=" * 50)
    print("HTML 报表生成结果：")
    print("=" * 50)
    print(result.content)
