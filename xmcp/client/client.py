# client.py
from mcp import ClientSession
from mcp.client.stdio import stdio_client
from mcp import StdioServerParameters
import asyncio

async def main():
    # 配置服务端连接参数
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # 初始化连接
            await session.initialize()
            
            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools:
                print(f"- {tool.name}: {tool.description}")
            

if __name__ == "__main__":
    asyncio.run(main())
