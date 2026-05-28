# ============================================================
# FILE:
# backend/app/research_pipeline/retrieval/query_expander.py
# ============================================================

from typing import List


class QueryExpander:

    """
    Expand financial semantic queries
    into business-aware retrieval queries.
    """

    QUERY_EXPANSIONS = {

        "ai": [
            "generative ai",
            "enterprise ai",
            "ai infrastructure",
            "ai workloads",
            "ai demand",
        ],

        "cloud": [
            "cloud infrastructure",
            "cloud capacity",
            "datacenter expansion",
            "cloud capex",
            "cloud compute",
        ],

        "gpu": [
            "gpu servers",
            "accelerator demand",
            "high performance compute",
            "compute clusters",
            "server infrastructure",
        ],

        "server": [
            "enterprise server",
            "server cpu",
            "server deployments",
            "server infrastructure",
        ],

        "datacenter": [
            "data center",
            "datacenter buildout",
            "compute infrastructure",
            "cloud scaling",
        ],

        "foundry": [
            "semiconductor manufacturing",
            "advanced packaging",
            "wafer production",
            "process node",
        ],
    }

    def normalize(
        self,
        query: str,
    ) -> str:

        return str(query).lower()

    def expand(
        self,
        query: str,
    ) -> str:

        normalized_query = (
            self.normalize(query)
        )

        expanded_terms = []

        for keyword, expansions in (
            self.QUERY_EXPANSIONS.items()
        ):

            if keyword in normalized_query:

                expanded_terms.extend(
                    expansions
                )

        expanded_query = (
            query
            + " "
            + " ".join(expanded_terms)
        )

        return expanded_query.strip()