# ============================================================
# FILE: backend/app/services/agent_service.py
# ============================================================

from backend.app.services.llm_service import (
    generate_llm_synthesis
)

# ============================================================
# RETRIEVAL ANALYST
# ============================================================

def retrieval_analyst(

    query: str,

    retrieved_chunks: list,

    themes: list,

    graph_stats: dict
):

    prompt = f"""

You are the Retrieval Analyst.

Your role:
- identify dominant semantic narratives
- summarize retrieved evidence
- explain recurring themes
- remain grounded in evidence

DO:
- discuss semantic narratives
- summarize retrieved information
- explain recurring concepts

DO NOT:
- predict markets
- claim causality
- hallucinate information

Focus:
- dominant narratives
- retrieved semantic evidence
"""

    response = generate_llm_synthesis(

        query=query,

        retrieved_chunks=retrieved_chunks,

        themes=themes,

        graph_stats=graph_stats,

        custom_prompt=prompt
    )

    return {

        "agent":
            "Retrieval Analyst",

        "analysis":
            response
    }

# ============================================================
# PROPAGATION ANALYST
# ============================================================

def propagation_analyst(

    query: str,

    retrieved_chunks: list,

    themes: list,

    graph_stats: dict
):

    prompt = f"""

You are the Propagation Analyst.

Your role:
- analyze semantic propagation
- identify cross-sector relationships
- discuss graph neighborhood expansion
- explain thematic diffusion

DO:
- discuss possible propagation
- explain semantic relationships
- identify thematic overlap

DO NOT:
- claim economic causality
- claim prediction capability
- overstate relationships

Focus:
- graph expansion
- sector relationships
- semantic diffusion
- propagation pathways
"""

    response = generate_llm_synthesis(

        query=query,

        retrieved_chunks=retrieved_chunks,

        themes=themes,

        graph_stats=graph_stats,

        custom_prompt=prompt
    )

    return {

        "agent":
            "Propagation Analyst",

        "analysis":
            response
    }

# ============================================================
# RISK ANALYST
# ============================================================

def risk_analyst(

    query: str,

    retrieved_chunks: list,

    themes: list,

    graph_stats: dict
):

    prompt = f"""

You are the Risk Analyst.

Your role:
- explain uncertainty
- explain system limitations
- discuss semantic ambiguity
- explain retrieval limitations

DO:
- discuss uncertainty
- discuss limitations
- discuss ambiguity
- explain semantic risks

DO NOT:
- make predictions
- overclaim certainty
- exaggerate findings

IMPORTANT:
Semantic similarity does not necessarily
represent economic causality.
"""

    response = generate_llm_synthesis(

        query=query,

        retrieved_chunks=retrieved_chunks,

        themes=themes,

        graph_stats=graph_stats,

        custom_prompt=prompt
    )

    return {

        "agent":
            "Risk Analyst",

        "analysis":
            response
    }

# ============================================================
# EXTRACT RETRIEVED CHUNKS
# ============================================================

def extract_retrieved_chunks(

    nodes
):

    chunks = []

    for node in nodes:

        data = node.get(
            "data",
            {}
        )

        chunk = data.get(
            "text",
            ""
        )

        if chunk:

            chunks.append(chunk)

    return chunks

# ============================================================
# GENERATE AGENT INSIGHTS
# ============================================================

def generate_agent_insights(

    query: str,

    graph_data: dict
):

    # ========================================================
    # GRAPH DATA
    # ========================================================

    nodes = graph_data.get(
        "nodes",
        []
    )

    edges = graph_data.get(
        "edges",
        []
    )

    themes = graph_data.get(
        "themes",
        []
    )

    # ========================================================
    # RETRIEVED CHUNKS
    # ========================================================

    retrieved_chunks = extract_retrieved_chunks(
        nodes
    )

    # ========================================================
    # GRAPH STATS
    # ========================================================

    graph_stats = {

        "nodes":
            len(nodes),

        "edges":
            len(edges),

        "themes":
            themes
    }

    # ========================================================
    # RETRIEVAL AGENT
    # ========================================================

    retrieval_agent = retrieval_analyst(

        query=query,

        retrieved_chunks=retrieved_chunks,

        themes=themes,

        graph_stats=graph_stats
    )

    # ========================================================
    # PROPAGATION AGENT
    # ========================================================

    propagation_agent = propagation_analyst(

        query=query,

        retrieved_chunks=retrieved_chunks,

        themes=themes,

        graph_stats=graph_stats
    )

    # ========================================================
    # RISK AGENT
    # ========================================================

    risk_agent = risk_analyst(

        query=query,

        retrieved_chunks=retrieved_chunks,

        themes=themes,

        graph_stats=graph_stats
    )

    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    return {

        "agents": [

            retrieval_agent,

            propagation_agent,

            risk_agent
        ]
    }

# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    mock_graph_data = {

        "themes": [

            "ai",
            "infrastructure",
            "energy"
        ],

        "nodes": [

            {

                "data": {

                    "text":
"""
NVIDIA reported increasing
AI datacenter demand and
higher infrastructure spending.
"""
                }
            },

            {

                "data": {

                    "text":
"""
Utilities discussed higher
energy requirements associated
with cloud infrastructure.
"""
                }
            },

            {

                "data": {

                    "text":
"""
Cloud providers continue
expanding GPU infrastructure
to support AI workloads.
"""
                }
            }
        ],

        "edges": [

            {}, {}, {}
        ]
    }

    insights = generate_agent_insights(

        query=
            "AI infrastructure demand",

        graph_data=
            mock_graph_data
    )

    print("\n===================================================")
    print("MULTI-AGENT RAG ANALYSIS")
    print("===================================================\n")

    for agent in insights["agents"]:

        print(
            f"\n{agent['agent']}"
        )

        print("-" * 60)

        print(
            agent["analysis"]
        )

        print()