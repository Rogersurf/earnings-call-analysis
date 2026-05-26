from fastapi import APIRouter

from backend.app.services.graph_service import (
    get_graph_data
)

router = APIRouter(
    prefix="/graph",
    tags=["graph"]
)

@router.get("/propagation")
async def graph_propagation_route(

    query: str = "AI infrastructure demand"

):

    results = get_graph_data(
        query=query
    )

    return {
        "results": results
    }