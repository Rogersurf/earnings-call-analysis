# ============================================================
# FILE: backend/app/routes/graph.py
# ============================================================

from fastapi import APIRouter
from pydantic import BaseModel

from backend.app.services.graph_service import (
    get_query_graph
)

# ============================================================
# ROUTER
# ============================================================

router = APIRouter()

# ============================================================
# REQUEST MODEL
# ============================================================

class GraphQueryRequest(BaseModel):

    query: str

    top_k_chunks: int = 5

    neighbors_per_chunk: int = 5

# ============================================================
# GRAPH QUERY ENDPOINT
# ============================================================

@router.post("/query")

def query_graph(

    request: GraphQueryRequest
):

    graph = get_query_graph(

        query=request.query,

        top_k_chunks=
            request.top_k_chunks,

        neighbors_per_chunk=
            request.neighbors_per_chunk
    )

    return graph