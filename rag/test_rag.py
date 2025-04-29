from torch import embedding
from rag import RAGSystem

if __name__ == "__main__":
    rag_system = RAGSystem()
    rag_system.searchTopKresults('query', 3)