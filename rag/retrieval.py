"""
向量检索模块
2024-1-16 [电子灰原哀] 添加retrieve方法实现
"""
import numpy as np

class VectorRetriever:
    def __init__(self, vector_store):
        """初始化检索器
        参数:
            vector_store: 向量存储实例
        """
        self.vector_store = vector_store
    
    def retrieve(self, query_embedding, top_k=5):
        """检索最相似的文档
        参数:
            query_embedding: 查询向量
            top_k: 返回最相似的k个结果
        返回:
            相似文档列表
        """
        try:
            # 使用Faiss进行相似度搜索
            distances, indices = self.vector_store.index.search(
                np.array([query_embedding]).astype('float32'), 
                top_k
            )
            # 返回匹配的文档内容
            return [self.vector_store.documents[i] for i in indices[0]]
        except Exception as e:
            print(f"检索失败: {str(e)}")
            raise

    def similarity_search(self, query_vector, k=5):
        """
        自定义向量相似性搜索实现
        参数：
            query_vector: 查询向量
            k: 返回结果数量
        返回：
            results: 相似文档列表
        """
        # 调用vector_store的底层FAISS接口进行搜索
        distances, indices = self.vector_store.index.search(query_vector, k)
        return [self.vector_store.documents[i] for i in indices[0]]