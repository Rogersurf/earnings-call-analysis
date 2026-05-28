from fastapi import APIRouter

from backend.app.services.research_service import (
    ResearchService
)


router = APIRouter(
    prefix="/research",
    tags=["Research"],
)

research_service = (
    ResearchService()
)


@router.get("/query")
def semantic_query(
    query: str,
    top_k: int = 10,
):

    return research_service.semantic_search(
        query=query,
        top_k=top_k,
    )


@router.get("/graph")
def graph_query(
    query: str,
    top_k: int = 10,
):

    return research_service.graph_search(
        query=query,
        top_k=top_k,
    )