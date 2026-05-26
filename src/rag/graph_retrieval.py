# ============================================================
# FILE: src/rag/graph_retrieval.py
# ============================================================

from pathlib import Path

import re
import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ============================================================
# LOAD MODEL
# ============================================================

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# ============================================================
# LOAD DATA
# ============================================================

DATA_PATH = Path(
    "outputs/chunks/semantic_chunks_embeddings.parquet"
)

df = pd.read_parquet(DATA_PATH)

# ============================================================
# PREPARE EMBEDDINGS
# ============================================================

embeddings_matrix = np.vstack(
    df["embedding"].values
)

# ============================================================
# THEMATIC KEYWORDS
# ============================================================

THEMATIC_KEYWORDS = {

    "ai": [
        "ai",
        "artificial intelligence",
        "machine learning",
        "llm",
        "foundation model",
        "inference"
    ],

    "infrastructure": [
        "datacenter",
        "data center",
        "cloud",
        "compute",
        "gpu",
        "server",
        "infrastructure"
    ],

    "energy": [
        "utilities",
        "electricity",
        "power",
        "grid",
        "energy demand"
    ],

    "semiconductors": [
        "nvidia",
        "amd",
        "chip",
        "chips",
        "gpu",
        "semiconductor"
    ],

    "supply_chain": [
        "china",
        "manufacturing",
        "logistics",
        "exports",
        "sourcing"
    ]
}

# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):

    if pd.isna(text):
        return ""

    text = str(text).lower()

    text = re.sub(
        r"[^a-zA-Z0-9\s]",
        "",
        text
    )

    return text

# ============================================================
# EXTRACT THEMES
# ============================================================

def extract_themes(text):

    text = normalize_text(text)

    themes_found = set()

    for theme, keywords in THEMATIC_KEYWORDS.items():

        for keyword in keywords:

            if keyword in text:

                themes_found.add(theme)

    return themes_found

# ============================================================
# COMPUTE THEMATIC OVERLAP
# ============================================================

def compute_thematic_overlap(

    source_text,
    target_text
):

    source_themes = extract_themes(
        source_text
    )

    target_themes = extract_themes(
        target_text
    )

    overlap = (
        source_themes
        &
        target_themes
    )

    return len(overlap)

# ============================================================
# SEMANTIC SEARCH
# ============================================================

def semantic_search(

    query: str,

    top_k: int = 10
):

    query_embedding = model.encode([query])

    similarities = cosine_similarity(

        query_embedding,
        embeddings_matrix

    )[0]

    top_indices = (
        similarities
        .argsort()[-top_k:]
        [::-1]
    )

    results = []

    for idx in top_indices:

        row = df.iloc[idx]

        results.append({

            "index":
                int(idx),

            "company":
                row.get("company", ""),

            "ticker":
                row.get("ticker", ""),

            "sector":
                row.get("sector", ""),

            "source_layer":
                row.get("source_layer", ""),

            "chunk_text":
                row.get("chunk_text", ""),

            "similarity":
                float(similarities[idx])
        })

    return results

# ============================================================
# RETRIEVE GRAPH CONTEXT
# ============================================================

def retrieve_graph_context(

    query: str,

    top_k_chunks: int = 5,

    neighbors_per_chunk: int = 5,

    min_similarity: float = 0.55
):

    # ========================================================
    # INITIAL RETRIEVAL
    # ========================================================

    retrieved_chunks = semantic_search(

        query=query,

        top_k=top_k_chunks
    )

    # ========================================================
    # GRAPH STRUCTURES
    # ========================================================

    nodes = {}

    edges = []

    edge_ids = set()

    # ========================================================
    # PROCESS RETRIEVED CHUNKS
    # ========================================================

    for chunk in retrieved_chunks:

        source_idx = chunk["index"]

        source_row = df.iloc[source_idx]

        source_embedding = np.array(
            source_row["embedding"]
        ).reshape(1, -1)

        source_text = source_row.get(
            "chunk_text",
            ""
        )

        source_sector = source_row.get(
            "sector",
            ""
        )

        source_company = source_row.get(
            "company",
            ""
        )

        source_ticker = source_row.get(
            "ticker",
            ""
        )

        source_id = str(source_idx)

        # ====================================================
        # SOURCE NODE
        # ====================================================

        if source_id not in nodes:

            nodes[source_id] = {

                "id":
                    source_id,

                "type":
                    "source",

                "position": {

                    "x":
                        int(len(nodes) * 250),

                    "y":
                        100,
                },

                "data": {

                    "company":
                        source_company,

                    "ticker":
                        source_ticker,

                    "sector":
                        source_sector,

                    "label":
                        f"{source_company} ({source_ticker})",

                    "chunk":
                        source_text[:300],

                    "themes":
                        list(
                            extract_themes(
                                source_text
                            )
                        ),

                    "similarity":
                        float(chunk["similarity"])
                }
            }

        # ====================================================
        # FIRST-ORDER NEIGHBORS
        # ====================================================

        similarities = cosine_similarity(

            source_embedding,
            embeddings_matrix

        )[0]

        neighbor_indices = (

            similarities
            .argsort()[-neighbors_per_chunk - 1:]
            [::-1]
        )

        for neighbor_idx in neighbor_indices:

            if neighbor_idx == source_idx:
                continue

            semantic_similarity = (
                similarities[neighbor_idx]
            )

            if semantic_similarity < min_similarity:
                continue

            neighbor_row = df.iloc[neighbor_idx]

            target_text = neighbor_row.get(
                "chunk_text",
                ""
            )

            target_sector = neighbor_row.get(
                "sector",
                ""
            )

            target_company = neighbor_row.get(
                "company",
                ""
            )

            target_ticker = neighbor_row.get(
                "ticker",
                ""
            )

            thematic_overlap = (
                compute_thematic_overlap(

                    source_text,
                    target_text
                )
            )

            cross_sector = (
                source_sector != target_sector
            )

            hybrid_score = (
                semantic_similarity
                +
                (thematic_overlap * 0.08)
                +
                (
                    0.05
                    if cross_sector
                    else 0
                )
            )

            if hybrid_score < 0.65:
                continue

            target_id = str(neighbor_idx)

            # =================================================
            # TARGET NODE
            # =================================================

            if target_id not in nodes:

                nodes[target_id] = {

                    "id":
                        target_id,

                    "type":
                        "neighbor",

                    "position": {

                        "x":
                            int(len(nodes) * 220),

                        "y":
                            400,
                    },

                    "data": {

                        "company":
                            target_company,

                        "ticker":
                            target_ticker,

                        "sector":
                            target_sector,

                        "label":
                            (
                                f"{target_company} "
                                f"({target_ticker})"
                            ),

                        "chunk":
                            target_text[:300],

                        "themes":
                            list(
                                extract_themes(
                                    target_text
                                )
                            ),

                        "similarity":
                            float(
                                semantic_similarity
                            )
                    }
                }

            # =================================================
            # EDGE
            # =================================================

            edge_id = (
                f"{source_id}-{target_id}"
            )

            reverse_edge_id = (
                f"{target_id}-{source_id}"
            )

            if (
                edge_id in edge_ids
                or
                reverse_edge_id in edge_ids
            ):
                continue

            edge_ids.add(edge_id)

            edges.append({

                "id":
                    edge_id,

                "source":
                    source_id,

                "target":
                    target_id,

                "animated":
                    False,

                "data": {

                    "semantic_similarity":
                        float(
                            semantic_similarity
                        ),

                    "hybrid_score":
                        float(
                            hybrid_score
                        ),

                    "thematic_overlap":
                        int(
                            thematic_overlap
                        ),

                    "cross_sector":
                        bool(
                            cross_sector
                        ),

                    "edge_type":
                        "first_order"
                }
            })

            # =================================================
            # SECOND-ORDER EXPANSION
            # =================================================

            neighbor_embedding = np.array(

                neighbor_row["embedding"]

            ).reshape(1, -1)

            neighbor_similarities = cosine_similarity(

                neighbor_embedding,
                embeddings_matrix

            )[0]

            second_order_indices = (

                neighbor_similarities
                .argsort()[-4:]
                [::-1]
            )

            for second_idx in second_order_indices:

                if second_idx in [

                    source_idx,
                    neighbor_idx
                ]:
                    continue

                second_similarity = (
                    neighbor_similarities[
                        second_idx
                    ]
                )

                if second_similarity < 0.60:
                    continue

                second_row = df.iloc[
                    second_idx
                ]

                second_id = str(second_idx)

                # =============================================
                # SECOND-ORDER NODE
                # =============================================

                if second_id not in nodes:

                    nodes[second_id] = {

                        "id":
                            second_id,

                        "type":
                            "second_order",

                        "position": {

                            "x":
                                int(
                                    len(nodes) * 180
                                ),

                            "y":
                                700,
                        },

                        "data": {

                            "company":
                                second_row.get(
                                    "company",
                                    ""
                                ),

                            "ticker":
                                second_row.get(
                                    "ticker",
                                    ""
                                ),

                            "sector":
                                second_row.get(
                                    "sector",
                                    ""
                                ),

                            "label":
                                (
                                    f"{second_row.get('company', '')} "
                                    f"({second_row.get('ticker', '')})"
                                ),

                            "chunk":
                                second_row.get(
                                    "chunk_text",
                                    ""
                                )[:300],

                            "themes":
                                list(

                                    extract_themes(

                                        second_row.get(
                                            "chunk_text",
                                            ""
                                        )
                                    )
                                ),

                            "similarity":
                                float(
                                    second_similarity
                                )
                        }
                    }

                # =============================================
                # SECOND-ORDER EDGE
                # =============================================

                second_edge_id = (
                    f"{target_id}-{second_id}"
                )

                reverse_second_edge_id = (
                    f"{second_id}-{target_id}"
                )

                if (

                    second_edge_id in edge_ids

                    or

                    reverse_second_edge_id in edge_ids
                ):
                    continue

                edge_ids.add(
                    second_edge_id
                )

                edges.append({

                    "id":
                        second_edge_id,

                    "source":
                        target_id,

                    "target":
                        second_id,

                    "animated":
                        False,

                    "data": {

                        "semantic_similarity":
                            float(
                                second_similarity
                            ),

                        "edge_type":
                            "second_order"
                    }
                })

    # ========================================================
    # GLOBAL THEMES
    # ========================================================

    all_themes = []

    for node in nodes.values():

        node_themes = (
            node["data"]
            .get("themes", [])
        )

        all_themes.extend(node_themes)

    unique_themes = sorted(
        list(set(all_themes))
    )

    # ========================================================
    # RETURN GRAPH
    # ========================================================

    return {

        "query":
            query,

        "themes":
            unique_themes,

        "num_nodes":
            len(nodes),

        "num_edges":
            len(edges),

        "nodes":
            list(nodes.values()),

        "edges":
            edges
    }

# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    query = "AI infrastructure demand"

    graph = retrieve_graph_context(

        query=query,

        top_k_chunks=5,

        neighbors_per_chunk=5
    )

    print("\n===================================================")
    print("DYNAMIC GRAPH RETRIEVAL")
    print("===================================================\n")

    print(f"Query: {query}")

    print(f"Nodes: {graph['num_nodes']}")

    print(f"Edges: {graph['num_edges']}")

    print(f"Themes: {graph['themes']}")

    print("\n===================================================\n")

    print("Sample Nodes:\n")

    for node in graph["nodes"][:5]:

        print(node["data"]["label"])

    print("\n===================================================\n")

    print("Sample Edges:\n")

    for edge in graph["edges"][:5]:

        print(

            edge["source"],
            "->",
            edge["target"]
        )