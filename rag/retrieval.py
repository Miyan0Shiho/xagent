class VectorRetriever:
    def __init__(self, vector_store):
        self.vector_store = vector_store

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