from typing_extensions import Literal, TypedDict, Dict, List, Union, Optional, Annotated, Sequence
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import asyncio
from uuid import uuid4
from langchain_ollama import ChatOllama  # 修正Ollama导入路径
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages

# 连接类型定义
class StdioConnection(TypedDict):
    command: str
    args: List[str]
    transport: Literal["stdio"]

class SSEConnection(TypedDict):
    url: str
    transport: Literal["sse"]

# 增强版状态类型
class AgentState(TypedDict):
    mcp_config: Optional[Dict[str, Union[StdioConnection, SSEConnection]]]
    messages: Annotated[Sequence[BaseMessage], add_messages]
    chat_history: Annotated[Sequence[BaseMessage], add_messages]
    thread_id: str

# MCP默认配置
DEFAULT_MCP_CONFIG = {
    "math": {
        "command": "python",
        "args": ["-m", "xmcp.server.server"],
        "transport": "stdio",
    }
}

# 初始化记忆模块（修正后的导入路径）
memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=5,
    return_messages=True
)

# 系统提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的数学助手，请用中文回答问题"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

async def chat_node(state: AgentState) -> dict:
    try:
        async with MultiServerMCPClient(state.get("mcp_config", DEFAULT_MCP_CONFIG)) as mcp_client:
            # 加载对话历史
            history = memory.load_memory_variables({})["chat_history"]
            
            # 获取工具集
            mcp_tools = mcp_client.get_tools()
            
            # 初始化模型
            model = ChatOllama(
                model="qwen2.5:1.5b",
                temperature=0,
            ).bind_tools(tools=mcp_tools)
            
            # 创建React智能体
            react_agent = create_react_agent(model, mcp_tools)
            
            # 构建输入数据
            agent_input = {
                "input": state["messages"][-1].content,
                "messages": state["messages"],
                "chat_history": history
            }
            
            # 执行智能体调用
            agent_response = await react_agent.ainvoke(agent_input)
            
            # 更新记忆和状态
            updated_messages = agent_response.get("messages", [])
            if updated_messages:
                memory.save_context(
                    {"input": state["messages"][-1].content},
                    {"output": updated_messages[-1].content}
                )
            
            return {
                "messages": updated_messages,
                "chat_history": memory.load_memory_variables({})["chat_history"]
            }
    except Exception as e:
        print(f"处理过程中发生错误: {str(e)}")
        return {"messages": [AIMessage(content="系统遇到问题，请稍后再试")]}

# 构建状态图
workflow = StateGraph(AgentState)
workflow.add_node("chat", chat_node)
workflow.set_entry_point("chat")
workflow.set_finish_point("chat")

# 编译应用实例（修正后的参数）
app = workflow.compile(
    checkpointer=MemorySaver(),
    # 移除了错误的config参数
)

if __name__ == "__main__":
    # 初始化带会话ID的状态
    initial_state = AgentState(
        mcp_config=DEFAULT_MCP_CONFIG,
        messages=[HumanMessage(content="我之前问你什么问题")],
        chat_history=[],
        thread_id=str(uuid4())
    )

    # 执行对话流程（配置在此处传递）
    async def main():
        async for step in app.astream(
            initial_state,
            config=RunnableConfig(
                configurable={
                    "thread_id": initial_state["thread_id"],
                    "checkpoint_id": str(uuid4())
                }
            )
        ):
            if "__end__" not in step:
                _, result = step.popitem()
                print("\n--- 响应结果 ---")
                print(result["messages"][-1].content)

    asyncio.run(main())
