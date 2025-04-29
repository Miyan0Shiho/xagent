"""
向量存储模块
2024-1-16 [电子灰原哀] 修复向量维度不匹配问题
"""
import numpy as np
import faiss

class VectorStore:
    def __init__(self, dim=512):  # Jina模型默认维度为512
        """初始化向量存储
        参数:
            dim: 向量维度，默认为512
        """
        self.index = faiss.IndexFlatL2(dim)
        self.documents = []
        
    def add_documents(self, vectors, documents):
        """添加文档向量到存储
        参数:
            vectors: 向量数组
            documents: 对应文档内容
        """
        try:
            vectors = np.array(vectors).astype('float32')
            assert vectors.shape[1] == self.index.d, f"维度不匹配: 期望{self.index.d}维，实际{vectors.shape[1]}维"
            self.index.add(vectors)
            self.documents.extend(documents)
        except Exception as e:
            print(f"添加文档失败: {str(e)}")
            raise

    def save_index(self, path):
        faiss.write_index(self.index, path)

    def load_index(self, path):
        self.index = faiss.read_index(path)

    def create_index(self, vectors):
        self.index = faiss.IndexFlatL2(len(vectors[0]))
        self.index.add(np.array(vectors).astype('float32'))