from typing import List, Dict, Optional

import chromadb

from sentence_transformers import SentenceTransformer

from backend.app.research_pipeline.retrieval.reranker import (
    FinancialReranker
)

from backend.app.research_pipeline.retrieval.query_expander import (
    QueryExpander
)


class HybridRetriever:

    def __init__(
        self,
        persist_path: str = "./data/chroma",
        embedding_model: str = "all-MiniLM-L6-v2",
    ):

        self.client = chromadb.PersistentClient(
            path=persist_path
        )

        self.model = SentenceTransformer(
            embedding_model
        )
        self.reranker = FinancialReranker()
        
        self.query_expander = QueryExpander()

    def get_collection(
        self,
        collection_name: str,
    ):

        return self.client.get_collection(
            name=collection_name
        )

    def search(
        self,
        collection_name: str,
        query: str,
        top_k: int = 5,
    ) -> List[Dict]:

        collection = self.get_collection(
            collection_name
        )
        
        expanded_query = (
            self.query_expander.expand(
                query
            )
        )

        query_embedding = self.model.encode(
            expanded_query,
            normalize_embeddings=True,
        ).tolist()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        formatted_results = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for doc, metadata, distance in zip(
            documents,
            metadatas,
            distances,
        ):

            formatted_results.append(
                {
                    "text": doc,
                    "metadata": metadata,
                    "score": 1 - distance,
                }
            )

        reranked_results = self.reranker.rerank(
            formatted_results
        )

        return reranked_results