import faiss
import numpy as np

class VectorStore:
    def __init__(self, dimension=768):
        self.index = faiss.IndexFlatL2(dimension)
        self.documents = []

    def add_documents(self, vectors, texts):
        """
        添加文档到向量库
        参数：
            vectors: 文本向量列表
            texts: 对应文本内容列表
        """
        self.index.add(np.array(vectors).astype('float32'))
        self.documents.extend(texts)

    def save_index(self, path):
        faiss.write_index(self.index, path)

    def load_index(self, path):
        self.index = faiss.read_index(path)

    def create_index(self, vectors):
        self.index = faiss.IndexFlatL2(len(vectors[0]))
        self.index.add(np.array(vectors).astype('float32'))