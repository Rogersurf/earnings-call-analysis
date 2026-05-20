from fastapi import APIRouter
from backend.app.services.agent_service import generate_agent_response

router = APIRouter(
    prefix="/agents",
    tags=["agents"]
)

@router.get("/explain")
async def explain_agent_route(query: str):

    response = generate_agent_response(query)

    return {
        "query": query,
        "analysis": response
    }