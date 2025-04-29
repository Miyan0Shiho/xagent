"""
这个文件负责定义RAG功能的模块集成和主程序的运行。
负责一个RAG长期搜索新闻和知识以构建知识向量库的功能。
负责提供一个api接口以供替他模块进行知识检索
提供一个api 接口供LLM利用RAG和向量库进记忆检索
2024-1-16 [电子灰原哀] 补全了add_document方法和文档处理逻辑
"""
from chunking import ChunkingStrategy
from retrieval import VectorRetriever
from vector_store import VectorStore
from transformers import AutoTokenizer, AutoModel
from torch import embedding
import numpy as np

class RAGSystem:
    def __init__(self):
        """2024-1-16 [电子灰原哀] 修复VectorStore初始化问题"""
        self.documents = []
        # 初始化模型和分词器
        self.tokenizer = AutoTokenizer.from_pretrained("jinaai/jina-embeddings-v2-small-en", trust_remote_code=True)
        self.model = AutoModel.from_pretrained("jinaai/jina-embeddings-v2-small-en", trust_remote_code=True)
        
        # 初始化向量存储（不再传入dim参数）
        self.chunking_strategy = ChunkingStrategy()
        self.vector_store = VectorStore()  # 修改为无参数初始化
        self.vector_retriever = VectorRetriever(self.vector_store)
        
        # 测试向量维度
        try:
            test_embedding = self._get_embeddings(["test"])[0]
            self.embedding_dim = len(test_embedding)
        except Exception as e:
            logger.error(f"获取向量维度失败: {str(e)}")
            raise

    def add_document(self, text):
        """
        添加单个文档到向量库
        参数：
            text: 要添加的文本内容
        """
        try:
            # 对文本进行分块
            chunks = self.chunking_strategy.split_text(text)
            # 获取每个块的嵌入向量
            embeddings = self._get_embeddings(chunks)
            # 将块和向量添加到向量库
            self.vector_store.add_documents(embeddings, chunks)
            self.documents.append(text)
        except Exception as e:
            print(f"添加文档失败: {str(e)}")
            raise

    def _get_embeddings(self, texts):
        """获取文本的嵌入向量"""
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).detach().numpy()
    
    def retrieve(self, query, top_k=5):
        """检索与查询最相关的文档"""
        query_embedding = self._get_embeddings([query])[0]
        return self.vector_retriever.retrieve(query_embedding, top_k)

    def run(self):
        """运行RAG系统"""
        # 示例文档
        documents = [
            "This is the first document.",
            "This is the second document.",
            "This is the third document.",
            "This is the fourth document.",
        ]
        for doc in documents:
            self.add_document(doc)
        # 查询示例
        query = "This is a query."
        results = self.retrieve(query)
        print("Query:", query)
        print("Results:", results)
    
    def searchTopKresults(self,query,top_k=5):
        results = self.retrieve(query, top_k)
        print(results)