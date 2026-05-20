from fastapi import APIRouter
from backend.app.services.retrieval_service import semantic_search

router = APIRouter(
    prefix="/retrieval",
    tags=["retrieval"]
)

@router.get("/search")
async def semantic_search_route(query: str):

    results = semantic_search(query)

    return {
        "query": query,
        "results": results
    }