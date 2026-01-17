from __future__ import annotations

import asyncio
from typing import Any, List, Optional

from langchain.agents import  create_agent
from langchain.agents.middleware import SummarizationMiddleware, HumanInTheLoopMiddleware, ToolCallLimitMiddleware, \
    ToolRetryMiddleware

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from app.agents.data_query_agent.tools.file_tools import _read_table_file
from app.agents.data_query_agent.tools.api_tools import _api_reader_tool
from app.agents.data_query_agent.tools.db_tools import _query_database
from app.models.LLM_MODEL import ModelInstances
from app.prompts.data_query_agent_prompt import DATA_QUERY_AGENT_SYSTEM_PROMPT
from langgraph.checkpoint.memory import InMemorySaver 


class json_response_format(BaseModel):
    """结构化输出为对应内容"""
    source: str= Field(description="文件类型，如csv")
    path: str=Field(description="文件举例路径，如data/sales.csv")
    columns: list =Field(description="文件中的列表属性，如age,year,name等表格文件的首行属性")
    row_count: int = Field(description="文件的行数，如128")
    all_rows: list =Field(description="展示所有行的内容，列表中也是json格式")



class DataQueryAgent:
    """
    使用 LangChain ReAct 模式封装的数据获取 Agent。

    - 内部通过一组 Tool 实现对不同数据源的访问（本地文件 / 数据库 / HTTP API）。
    - 
    """
    # 限制特定工具

    def __init__(self,thread_id,userinput):
        self.thread_id=thread_id,
        self.user_input=userinput
        self.tools=[_query_database,_api_reader_tool,_read_table_file]
        self.api_search_limiter = ToolCallLimitMiddleware(          #限制api 访问工具的调用次数，避免过多次重复调用。
            tool_name="_api_reader_tool",
            thread_limit=5,
            run_limit=3,
        )
        self.agent = create_agent(
            model=ModelInstances.query_llm,
            tools=self.tools,
            system_prompt=DATA_QUERY_AGENT_SYSTEM_PROMPT,
            checkpointer=InMemorySaver(),
            response_format=json_response_format,
            middleware=[
                SummarizationMiddleware(
                    model=ModelInstances.query_llm,
                    trigger=("tokens", 4000),
                    keep=("messages", 20),
                ),
                self.api_search_limiter,  #限制api 访问工具的调用次数，避免过多次重复调用。

                ToolRetryMiddleware(#工具重试，特别适用于api获取信息和sql操作。
                    max_retries=3,  # 最多重试 3 次
                    backoff_factor=2.0,  # 指数回退乘数
                    initial_delay=1.0,  # 从 1 秒延迟开始
                    max_delay=60.0,  # 将延迟上限设置为 60 秒
                    jitter=True,  # 添加随机抖动以避免“惊群”问题
                ),
            ],
        )

    async def run(self) -> json_response_format:
        response= await self.agent.ainvoke(
            {"messages": [HumanMessage(content=self.user_input)]},
        {"configurable": {"thread_id": f"{self.thread_id}"}}
                                    )
        return response["structured_response"]

@tool
async def query_agent_chat(query:str,thread_id:int)->json_response_format:
    """
    获取数据的工具，具备数据的获取能力。

    Args:
        query: 用户的原需求
        thread_id：当前用户的线程id

    Returns:
        获取数据的结果
    """
    query_agent = DataQueryAgent(thread_id=thread_id, userinput=query)
    response = await query_agent.run()
    print(f"信息获取agent反馈如下：{response}")
    return response

async def test():
    query_agent = DataQueryAgent(thread_id=123, userinput="请帮我分析员工的部门组成，各部门各自有多少人")
    response = await query_agent.run()
    print(response)


if __name__ == "__main__":
    #这里要改为async的
    asyncio.run(test())


