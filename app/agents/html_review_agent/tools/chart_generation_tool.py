from langchain_mcp_adapters.client import MultiServerMCPClient

mcp_server_chart ={
    "transport": "sse",
    "url": "https://mcp.api-inference.modelscope.net/2a9b3733645243/sse"
}

mcp_client = MultiServerMCPClient({
    "chart": mcp_server_chart,
})

async def get_mcp_tools():
    """获取专门用于各种精美图表生成的 MCP工具"""
    try:
        chart_tools = await mcp_client.get_tools(server_name="chart")
        print(f"成功加载 {len(chart_tools)} 个 图表生成MCP 工具")
        return chart_tools

    except Exception as e:
        print(f"加载 chart MCP 工具失败: {e}")