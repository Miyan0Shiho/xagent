"""
这个文件负责定义RAG功能的模块集成和主程序的运行。
负责一个RAG长期搜索新闻和知识以构建知识向量库的功能。
负责提供一个api接口以供替他模块进行知识检索
提供一个api 接口供LLM利用RAG和向量库进记忆检索
"""
from .chunking import ChunkingStrategy
from .retrieval import VectorRetriever
from .vector_store import VectorStore

class RAGSystem:
    def __init__(self):
        self.chunker = ChunkingStrategy()
        self.vector_store = VectorStore()
        self.retriever = VectorRetriever(self.vector_store)
        self.documents = []

    def add_documents(self, texts):
        """
        添加文档到知识库
        参数：
            texts: 文本列表
        """
        chunks = []
        for text in texts:
            chunks.extend(self.chunker.split_text(text))
        # 这里需要后续添加文本向量化实现
        self.vector_store.add_documents([], chunks)

    def query(self, question, k=3):
        """
        提供外部调用的查询接口
        参数：
            question: 查询文本
            k: 返回结果数量
        返回：
            相关文档片段列表
        """
        # 这里需要后续添加查询向量化实现
        return self.retriever.similarity_search([], k)

    def get_memory_context(self, query):
        """
        为记忆模块提供的专用接口
        参数：
            query: 记忆查询内容
        返回：
            相关记忆片段列表
        """
        return self.query(query, k=5)