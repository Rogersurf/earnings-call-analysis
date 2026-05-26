# ============================================================
# FILE: backend/app/routes/agents.py
# ============================================================

from fastapi import APIRouter

from pydantic import BaseModel

from backend.app.services.graph_service import (
    get_query_graph
)

from backend.app.services.agent_service import (
    generate_agent_insights
)

# ============================================================
# ROUTER
# ============================================================

router = APIRouter(

    prefix="/agents",

    tags=["agents"]
)

# ============================================================
# REQUEST MODEL
# ============================================================

class AgentQueryRequest(BaseModel):

    query: str

# ============================================================
# AGENT QUERY
# ============================================================

@router.post("/query")

async def query_agents(

    request: AgentQueryRequest
):

    # ========================================================
    # GRAPH CONTEXT
    # ========================================================

    graph_data = get_query_graph(

        query=request.query
    )

    # ========================================================
    # AGENT INSIGHTS
    # ========================================================

    insights = generate_agent_insights(

    query=request.query,

    graph_data=graph_data
    )

    # ========================================================
    # RESPONSE
    # ========================================================

    return {

        "query":
            request.query,

        "agents":
            insights["agents"]
    }