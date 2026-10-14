import os
from typing import List, Dict, Any
import chromadb
from chromadb.utils import embedding_functions

CHROMA_PATH = os.path.join("kb", "chroma_data")
COLLECTION_NAME = "owasp_security_rules"

class KnowledgeBaseRetriever:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=CHROMA_PATH)
        self.ef = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=self.ef
        )

    def retrieve(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )

        formatted_results = []
        if results and results["documents"]:
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            dists = results["distances"][0] if "distances" in results and results["distances"] else [0.0] * len(docs)

            for i in range(len(docs)):
                formatted_results.append({
                    "content": docs[i],
                    "source": metas[i].get("source", "unknown"),
                    "topic": metas[i].get("topic", "general"),
                    "distance": dists[i]
                })
        return formatted_results

def retrieve(query: str, k: int = 3) -> List[Dict[str, Any]]:
    retriever = KnowledgeBaseRetriever()
    return retriever.retrieve(query, k=k)