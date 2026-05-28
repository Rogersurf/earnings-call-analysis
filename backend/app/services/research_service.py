from typing import Dict

from backend.app.research_pipeline.retrieval.retriever import (
    HybridRetriever
)

from backend.app.research_pipeline.retrieval.graph_expander import (
    SemanticGraphExpander
)


class ResearchService:

    """
    Main orchestration service for
    semantic intelligence research operations.
    """

    def __init__(self):

        self.retriever = (
            HybridRetriever()
        )

        self.graph_expander = (
            SemanticGraphExpander()
        )

    def semantic_search(
        self,
        query: str,
        collection_name: str = (
            "earnings_speaker_turns"
        ),
        top_k: int = 10,
    ) -> Dict:

        results = self.retriever.search(
            collection_name=collection_name,
            query=query,
            top_k=top_k,
        )

        return {
            "query": query,
            "collection": collection_name,
            "results": results,
            "total_results": len(results),
        }

    def graph_search(
        self,
        query: str,
        collection_name: str = (
            "earnings_speaker_turns"
        ),
        top_k: int = 10,
    ) -> Dict:

        graph_result = (
            self.graph_expander.expand_query(
                query=query,
                collection_name=collection_name,
                top_k=top_k,
            )
        )

        return {
            "query": query,

            "nodes": graph_result["nodes"],

            "edges": graph_result["edges"],

            "companies": (
                self.graph_expander.get_connected_companies()
            ),

            "graph_nodes": (
                self.graph_expander.export_node_data()
            ),

            "graph_edges": (
                self.graph_expander.export_edge_data()
            ),
        }