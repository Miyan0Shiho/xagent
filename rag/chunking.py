class ChunkingStrategy:
    def __init__(self, chunk_size=512, overlap=64):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split_text(self, text):
        """
        自定义文本分块实现
        参数：
            text: 输入文本字符串
        返回：
            chunks: 分块后的文本列表
        """
        chunks = []
        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])
            start = end - self.overlap
        return chunks