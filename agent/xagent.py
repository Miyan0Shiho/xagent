from langchain_ollama import OllamaLLM
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import os
import sys

# 获取当前工作目录并添加到模块路径
current_dir = os.getcwd()
sys.path.insert(0, current_dir)
from xmcp.client.client import get_tools
import subprocess
# 启动Ollama服务（后台运行）
subprocess.Popen(["ollama", "serve"])

# 初始化模型（新版本API）
llm = OllamaLLM(
    model="deepseek-r1:1.5b",
    temperature=0.7,
    base_url='http://localhost:11434',
    # streaming参数已移动到调用方法 [[4]][[13]]
)
print(get_tools())

react_agent = create_react_agent(llm, tools=get_tools())
agent_input = {
            "messages": '什么是人工智能？',
        }
        
        # Run the react agent subgraph with our input
agent_response = react_agent.ainvoke(agent_input)
print(agent_response)