# XAgent - 多功能AI代理框架

## 项目简介
XAgent是一个结合了LLM、MCP、RAG和MEM能力的多功能AI代理框架，旨在探索如何通过基础能力组合充分释放大语言模型的潜力。

## 核心功能
- **MCP (Multi-Capability Processor)**: 多能力处理器
  - 当前已实现基础数学计算功能
  - 计划扩展更多工具能力
- **RAG (Retrieval-Augmented Generation)**: 检索增强生成
  - 基础检索功能实现
  - 待优化知识库和检索算法
- **MEM (Memory)**: 记忆模块
  - 基础记忆功能实现
  - 待增强长期记忆和上下文管理

## 项目状态
🚧 开发中 (WIP)  
当前版本为早期原型，各模块功能尚待完善：
- MCP仅实现基础数学工具
- RAG和MEM模块较为简陋
- 需要优化系统架构和性能

## 快速开始
```bash
# 安装依赖
pip install -r requirements.txt

# 运行示例
python agent/xagent.py
```

