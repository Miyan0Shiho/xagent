# client.py
from mcp import ClientSession
from mcp.client.stdio import stdio_client
from mcp import StdioServerParameters
import asyncio

async def main():
    # 配置服务端连接参数
    server_params = StdioServerParameters(
        command="python",
        args=["xmcp/server/server.py"]
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # 初始化连接
            await session.initialize()
            
            tools = await session.list_tools()
            return tools
            
def get_tools():
    tools = asyncio.run(main())
    available_tools = [{
        "name": tool.name,
        "description": tool.description,
        "input_schema": tool.inputSchema
    } for tool in tools.tools]
    return available_tools

