# ============================================================
# FILE: backend/app/services/graph_service.py
# ============================================================

from src.rag.graph_retrieval import (
    retrieve_graph_context
)

# ============================================================
# GRAPH QUERY SERVICE
# ============================================================

def get_query_graph(

    query: str,

    top_k_chunks: int = 5,

    neighbors_per_chunk: int = 5
):

    graph_data = retrieve_graph_context(

        query=query,

        top_k_chunks=top_k_chunks,

        neighbors_per_chunk=neighbors_per_chunk
    )

    return {

        "success": True,

        "query": graph_data["query"],

        "themes": graph_data["themes"],

        "num_nodes": graph_data["num_nodes"],

        "num_edges": graph_data["num_edges"],

        "nodes": graph_data["nodes"],

        "edges": graph_data["edges"]
    }