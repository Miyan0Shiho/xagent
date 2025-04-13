
from typing_extensions import Literal, TypedDict, Dict, List, Any, Union, Optional
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command
from copilotkit import CopilotKitState
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import os
import asyncio
from langchain_ollama import ChatOllama
class StdioConnection(TypedDict):
    command: str
    args: List[str]
    transport: Literal["stdio"]

class SSEConnection(TypedDict):
    url: str
    transport: Literal["sse"]

# Type for MCP configuration
MCPConfig = Dict[str, Union[StdioConnection, SSEConnection]]

class AgentState(CopilotKitState):
    mcp_config: Optional[MCPConfig]
DEFAULT_MCP_CONFIG: MCPConfig = {
    "math": {
        "command": "python",
        "args": ["-m", "xmcp.server.server"],
        "transport": "stdio",
    },
}
async def chat_node(state: AgentState) -> Command[Literal["__end__"]]:
    mcp_config = state.get("mcp_config", DEFAULT_MCP_CONFIG)
    async with MultiServerMCPClient(mcp_config) as mcp_client:

        mcp_tools = mcp_client.get_tools()
        model = ChatOllama(
            model="qwen2.5:1.5b",
            temperature=0,
        ).bind_tools(tools=mcp_tools)
        react_agent = create_react_agent(model, mcp_tools)
        agent_input = {
            "messages": state["messages"]
        }
        agent_response = await react_agent.ainvoke(agent_input)
        # Update the state with the new messages
        updated_messages = agent_response.get("messages", [])
        print(updated_messages[-1].content)
        

if __name__ == "__main__":
    state = AgentState(
        mcp_config=DEFAULT_MCP_CONFIG,
        messages=[
            {"role": "user", "content": "计算1+1等于几"},
        ]
    )
    asyncio.run(chat_node(state))