from fastapi import APIRouter

from backend.app.services.graph_service import (
    get_graph_data
)

router = APIRouter(
    prefix="/graph",
    tags=["graph"]
)

@router.get("/propagation")
async def graph_propagation_route():

    results = get_graph_data()

    return {
        "results": results
    }