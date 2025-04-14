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
from langchain.memory import ConversationBufferWindowMemory  # +++ 新增记忆模块
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder  # +++ 新增提示模板组件
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage  # +++ 消息类型

class StdioConnection(TypedDict):
    command: str
    args: List[str]
    transport: Literal["stdio"]

class SSEConnection(TypedDict):
    url: str
    transport: Literal["sse"]

# Type for MCP configuration
MCPConfig = Dict[str, Union[StdioConnection, SSEConnection]]

# ========== 新增记忆模块初始化 ==========
memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=5,  # 保留最近5轮对话
    return_messages=True
)

# ========== 修改提示模板 ==========
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个数学助手"), 
    MessagesPlaceholder(variable_name="chat_history"),  # 历史消息占位符
    ("human", "{input}")
])

# ========== 修改状态定义 ==========
class AgentState(CopilotKitState):
    mcp_config: Optional[MCPConfig]
    messages: List[Union[HumanMessage, AIMessage]]  # +++ 明确消息类型
    input: str  # +++ 新增输入字段

# ========== 连接定义保持不变 ==========
class StdioConnection(TypedDict):
    command: str
    args: List[str]
    transport: Literal["stdio"]

class SSEConnection(TypedDict):
    url: str
    transport: Literal["sse"]

MCPConfig = Dict[str, Union[StdioConnection, SSEConnection]]

DEFAULT_MCP_CONFIG: MCPConfig = {
    "math": {
        "command": "python",
        "args": ["-m", "xmcp.server.server"],
        "transport": "stdio",
    },
}

# ========== 修改聊天节点 ==========
async def chat_node(state: AgentState) -> Command[Literal["__end__"]]:
    # 加载历史上下文
    history = memory.load_memory_variables({})["chat_history"]
    
    # 构建包含上下文的输入
    agent_input = {
        "input": state["input"],
        "chat_history": history,
        "messages": state["messages"]
    }

    mcp_config = state.get("mcp_config", DEFAULT_MCP_CONFIG)
    async with MultiServerMCPClient(mcp_config) as mcp_client:
        mcp_tools = mcp_client.get_tools()
        
        model = ChatOllama(
            model="qwen2.5:1.5b",
            temperature=0,
        ).bind_tools(tools=mcp_tools).bind(prompt=prompt)  # +++ 绑定提示模板
        
        react_agent = create_react_agent(
            model,
            tools=mcp_tools,
        )
        
        agent_response = await react_agent.ainvoke(agent_input)
        
        # 保存上下文到记忆
        memory.save_context(
            {"input": state["input"]},
            {"output": agent_response["messages"][-1].content}
        )
        
        # 更新状态
        updated_messages = agent_response.get("messages", [])
        print('当前上下文:', [msg.content for msg in history[-5:]])
        return {"messages": updated_messages}

# ========== 初始化工作流 ==========
workflow = StateGraph(AgentState)
workflow.add_node("chat", chat_node)
workflow.set_entry_point("chat")
workflow.add_edge("chat", END)

# 使用内存检查点保存对话状态
memory_saver = MemorySaver()
app = workflow.compile(checkpointer=memory_saver)

# ========== 主程序调用示例 ==========
if __name__ == "__main__":
    # 初始化对话线程（不同thread_id隔离对话历史）
    config = {"configurable": {"thread_id": "math_session_1"}}
    
    # 模拟连续对话
    async def test_conversation():
        # 第一轮对话
        state = AgentState(
            mcp_config=DEFAULT_MCP_CONFIG,
            messages=[],
            input="1+1等于几"
        )
        response1 = await app.ainvoke(state, config=config)
        print("回答1:", response1["messages"][-1].content)
        
        # 第二轮对话（依赖上下文）
        state.input = "再乘以3是多少？"
        state.messages = response1["messages"]
        response2 = await app.ainvoke(state, config=config)
        print("回答2:", response2["messages"][-1].content)
        
        # 显示当前记忆
        print("\n当前记忆:")
        print(memory.load_memory_variables({})["chat_history"])

    asyncio.run(test_conversation())
