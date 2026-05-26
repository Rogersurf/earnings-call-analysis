from fastapi import FastAPI

from fastapi.middleware.cors import (
    CORSMiddleware
)

from backend.app.routes.retrieval import (
    router as retrieval_router
)

from backend.app.routes.graph import (
    router as graph_router
)

from backend.app.routes.agents import (
    router as agents_router
)

# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(

    title=
        "Earnings Call Semantic Intelligence API",

    version="0.1.0"
)

# ============================================================
# CORS
# ============================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

# ============================================================
# ROUTES
# ============================================================

app.include_router(
    retrieval_router
)

app.include_router(

    graph_router,

    prefix="/graph",

    tags=["Graph"]
)

app.include_router(
    agents_router
)

# ============================================================
# ROOT
# ============================================================

@app.get("/")

async def root():

    return {

        "status":
            "online",

        "system":
            "semantic intelligence engine",

        "version":
            "0.1.0"
    }