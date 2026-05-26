from backend.app.services.retrieval_service import (
    semantic_graph_expansion
)

# ======================================================
# GRAPH SERVICE
# ======================================================

def get_graph_data(

    query="AI infrastructure demand"

):

    graph = semantic_graph_expansion(
        query=query
    )

    return graph