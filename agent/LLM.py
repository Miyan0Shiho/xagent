from langchain_ollama import OllamaLLM  # 使用新版本包 [[1]][[7]]
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage

# 初始化模型（新版本API）
llm = OllamaLLM(
    model="deepseek-r1:1.5b",
    temperature=0.7,
    base_url='http://localhost:11434',
    # streaming参数已移动到调用方法 [[4]][[13]]
)

# 系统提示模板
system_prompt = SystemMessage(
    content="你是一个专业的AI助手，需要用清晰简洁的中文回答用户问题。"
)

# 对话模板（调整格式匹配新版本）
prompt = ChatPromptTemplate.from_messages([
    system_prompt,
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}")
])

# 初始化对话链（适配新版本API）
conversation = ConversationChain(
    llm=llm,
    prompt=prompt,
    memory=ConversationBufferMemory(return_messages=True),
    verbose=True
)

# 流式输出调用方式
response_stream = conversation.stream(
    input="请用一句话解释人工智能是什么。"
)

# 处理流式响应（新版本输出格式）
for chunk in response_stream:
    print(chunk["response"], end="", flush=True)
