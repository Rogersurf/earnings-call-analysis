from typing import List, Dict
from collections import defaultdict

import networkx as nx

from backend.app.research_pipeline.retrieval.retriever import (
    HybridRetriever
)


class SemanticGraphExpander:

    """
    Graph-aware semantic retrieval expansion.

    Goal:
    transform retrieval results into
    semantic propagation graphs.
    """

    def __init__(self):

        self.retriever = HybridRetriever()

        self.graph = nx.Graph()

    @staticmethod
    def build_node_id(
        metadata: Dict,
    ) -> str:

        ticker = metadata.get(
            "ticker",
            "UNK",
        )

        quarter = metadata.get(
            "quarter",
            "UNK",
        )

        year = metadata.get(
            "earnings_year",
            "UNK",
        )

        sequence = metadata.get(
            "sequence",
            "0",
        )

        return (
            f"{ticker}_{year}_{quarter}_{sequence}"
        )

    def add_result_node(
        self,
        result: Dict,
    ):

        metadata = result["metadata"]

        node_id = self.build_node_id(
            metadata
        )

        self.graph.add_node(
            node_id,

            text=result["text"],

            score=result.get(
                "reranked_score",
                result.get("score", 0.0),
            ),

            ticker=metadata.get("ticker"),

            company=metadata.get("company"),

            speaker=metadata.get("speaker"),

            speaker_type=metadata.get(
                "speaker_type"
            ),

            section=metadata.get("section"),

            semantic_layer=metadata.get(
                "semantic_layer"
            ),

            quarter=metadata.get(
                "quarter"
            ),

            earnings_year=metadata.get(
                "earnings_year"
            ),
        )

        return node_id

    def connect_results(
        self,
        node_ids: List[str],
    ):

        for i in range(len(node_ids)):

            for j in range(i + 1, len(node_ids)):
                
                if node_ids[i] == node_ids[j]:
                    continue

                self.graph.add_edge(
                    node_ids[i],
                    node_ids[j],
                    relation="semantic_similarity",
                )

    def expand_query(
        self,
        query: str,
        collection_name: str = "earnings_speaker_turns",
        top_k: int = 10,
    ):

        results = self.retriever.search(
            collection_name=collection_name,
            query=query,
            top_k=top_k,
        )

        node_ids = set()

        for result in results:

            node_id = self.add_result_node(
                result
            )

            node_ids.add(node_id)

        self.connect_results(
            list(node_ids)
        )

        return {
            "query": query,
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges(),
            
            "graph": self.graph,
        }

    def get_connected_companies(
        self,
    ) -> List[str]:

        companies = set()

        for _, data in self.graph.nodes(
            data=True
        ):

            company = data.get("company")

            if company:
                companies.add(company)

        return sorted(companies)

    def export_node_data(
        self,
    ) -> List[Dict]:

        exported = []

        for node_id, data in self.graph.nodes(
            data=True
        ):

            exported.append(
                {
                    "node_id": node_id,
                    **data,
                }
            )

        return exported

    def export_edge_data(
        self,
    ) -> List[Dict]:

        exported = []

        for source, target, data in self.graph.edges(
            data=True
        ):

            exported.append(
                {
                    "source": source,
                    "target": target,
                    **data,
                }
            )

        return exported