from pathlib import Path

import re
import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ======================================================
# LOAD MODEL
# ======================================================

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# ======================================================
# LOAD DATASET
# ======================================================

DATA_PATH = Path(
    "outputs/chunks/semantic_chunks_embeddings.parquet"
)

df = pd.read_parquet(DATA_PATH)

# ======================================================
# PREPARE EMBEDDINGS
# ======================================================

embeddings_matrix = np.vstack(
    df["embedding"].values
)

# ======================================================
# ENTITY / DOMAIN SYNONYMS
# ======================================================

ENTITY_SYNONYMS = {

    "ai": [
        "artificial intelligence",
        "machine learning",
        "llm",
        "foundation model",
        "generative ai"
    ],

    "datacenter": [
        "data center",
        "cloud",
        "hyperscale",
        "infrastructure",
        "compute"
    ],

    "energy": [
        "utilities",
        "electricity",
        "power",
        "grid"
    ],

    "semiconductor": [
        "gpu",
        "chip",
        "nvidia",
        "amd"
    ],

    "china": [
        "chinese",
        "asia",
        "manufacturing",
        "sourcing"
    ],

    "brazil": [
        "brazilian",
        "latam",
        "latin america"
    ]
}

# ======================================================
# QUERY NORMALIZATION
# ======================================================

def normalize_text(text: str):

    text = text.lower()

    text = re.sub(
        r"[^a-zA-Z0-9\s]",
        "",
        text
    )

    return text

# ======================================================
# KEYWORD EXTRACTION
# ======================================================

def extract_keywords(query: str):

    query = normalize_text(query)

    return query.split()

# ======================================================
# KEYWORD BOOST
# ======================================================

def compute_keyword_boost(

    query_keywords,
    chunk_text,
):

    chunk_text = normalize_text(chunk_text)

    boost = 0.0

    for keyword in query_keywords:

        if keyword in chunk_text:

            boost += 0.05

    return boost

# ======================================================
# ENTITY BOOST
# ======================================================

def compute_entity_boost(

    query_keywords,
    chunk_text,
):

    chunk_text = normalize_text(chunk_text)

    boost = 0.0

    for keyword in query_keywords:

        if keyword not in ENTITY_SYNONYMS:
            continue

        synonyms = ENTITY_SYNONYMS[keyword]

        for synonym in synonyms:

            synonym = normalize_text(synonym)

            if synonym in chunk_text:

                boost += 0.08

    return boost

# ======================================================
# HYBRID SCORE
# ======================================================

def compute_hybrid_score(

    semantic_score,
    keyword_score,
    entity_score,
):

    return (
        semantic_score
        + keyword_score
        + entity_score
    )

# ======================================================
# SEMANTIC SEARCH
# ======================================================

def semantic_search(

    query: str,

    top_k: int = 10
):

    # ==============================================
    # NORMALIZE QUERY
    # ==============================================

    normalized_query = normalize_text(query)

    query_keywords = extract_keywords(
        normalized_query
    )

    # ==============================================
    # QUERY EMBEDDING
    # ==============================================

    query_embedding = model.encode(
        [normalized_query]
    )

    # ==============================================
    # SEMANTIC SIMILARITIES
    # ==============================================

    semantic_scores = cosine_similarity(

        query_embedding,
        embeddings_matrix

    )[0]

    # ==============================================
    # HYBRID SCORING
    # ==============================================

    hybrid_scores = []

    for idx, semantic_score in enumerate(
        semantic_scores
    ):

        row = df.iloc[idx]

        chunk_text = row["chunk_text"]

        # ------------------------------------------
        # KEYWORD BOOST
        # ------------------------------------------

        keyword_score = compute_keyword_boost(

            query_keywords,
            chunk_text
        )

        # ------------------------------------------
        # ENTITY BOOST
        # ------------------------------------------

        entity_score = compute_entity_boost(

            query_keywords,
            chunk_text
        )

        # ------------------------------------------
        # FINAL SCORE
        # ------------------------------------------

        final_score = compute_hybrid_score(

            semantic_score=semantic_score,

            keyword_score=keyword_score,

            entity_score=entity_score,
        )

        hybrid_scores.append(final_score)

    hybrid_scores = np.array(hybrid_scores)

    # ==============================================
    # TOP RESULTS
    # ==============================================

    top_indices = (
        hybrid_scores
        .argsort()[-top_k:]
        [::-1]
    )

    results = []

    for idx in top_indices:

        row = df.iloc[idx]

        results.append({

            "company":
                row["company"],

            "ticker":
                row["ticker"],

            "source_layer":
                row["source_layer"],

            "chunk_text":
                row["chunk_text"],

            "semantic_score":
                float(semantic_scores[idx]),

            "hybrid_score":
                float(hybrid_scores[idx])
        })

    return results

# ======================================================
# GRAPH EXPANSION
# ======================================================

def semantic_graph_expansion(

    query: str,

    top_k: int = 5,

    neighbors_per_chunk: int = 5,
):

    # ==============================================
    # RETRIEVE TOP RESULTS
    # ==============================================

    search_results = semantic_search(

        query=query,

        top_k=top_k
    )

    # ==============================================
    # GRAPH STRUCTURES
    # ==============================================

    nodes = {}

    edges = []

    # ==============================================
    # BUILD GRAPH
    # ==============================================

    for result in search_results:

        # ------------------------------------------
        # FIND MATCHING ROW
        # ------------------------------------------

        matching_rows = df[
            df["chunk_text"]
            ==
            result["chunk_text"]
        ]

        if len(matching_rows) == 0:
            continue

        idx = matching_rows.index[0]

        row = df.loc[idx]

        source_id = str(int(idx))

        # ------------------------------------------
        # SOURCE NODE
        # ------------------------------------------

        nodes[source_id] = {

            "id":
                source_id,

            "type":
                "default",

            "position": {

                "x":
                    int(idx % 5 * 250),

                "y":
                    int(idx // 5 * 200),
            },

            "data": {

                "label":
                    f"{row['company']} ({row['ticker']})",

                "chunk":
                    row["chunk_text"][:120],

                "score":
                    float(result["hybrid_score"])
            }
        }

        # ------------------------------------------
        # SOURCE EMBEDDING
        # ------------------------------------------

        source_embedding = np.array(
            row["embedding"]
        ).reshape(1, -1)

        # ------------------------------------------
        # FIND NEIGHBORS
        # ------------------------------------------

        neighbor_scores = cosine_similarity(

            source_embedding,
            embeddings_matrix

        )[0]

        # ------------------------------------------
        # TOP NEIGHBORS
        # ------------------------------------------

        neighbor_indices = (
            neighbor_scores
            .argsort()[-neighbors_per_chunk-1:]
            [::-1]
        )

        # ------------------------------------------
        # BUILD NEIGHBOR GRAPH
        # ------------------------------------------

        for neighbor_idx in neighbor_indices:

            if neighbor_idx == idx:
                continue

            neighbor_row = df.iloc[neighbor_idx]

            target_id = str(int(neighbor_idx))

            # --------------------------------------
            # TARGET NODE
            # --------------------------------------

            if target_id not in nodes:

                nodes[target_id] = {

                    "id":
                        target_id,

                    "type":
                        "default",

                    "position": {

                        "x":
                            int(neighbor_idx % 5 * 250),

                        "y":
                            int(neighbor_idx // 5 * 200 + 300),
                    },

                    "data": {

                        "label":
                            f"{neighbor_row['company']} ({neighbor_row['ticker']})",

                        "chunk":
                            neighbor_row["chunk_text"][:120],
                    }
                }

            # --------------------------------------
            # EDGE
            # --------------------------------------

            edges.append({

                "id":
                    f"{source_id}-{target_id}",

                "source":
                    source_id,

                "target":
                    target_id,

                "animated":
                    False,

                "similarity":
                    float(neighbor_scores[neighbor_idx])
            })

    # ==============================================
    # RETURN GRAPH
    # ==============================================

    return {

        "nodes":
            list(nodes.values()),

        "edges":
            edges,
    }

# ======================================================
# TEST
# ======================================================

if __name__ == "__main__":

    query = "AI infrastructure demand"

    results = semantic_search(query)

    print("\n" + "=" * 60)
    print(f"QUERY: {query}")
    print("=" * 60)

    for r in results[:5]:

        print("\n")

        print(f"Company: {r['company']}")
        print(f"Ticker: {r['ticker']}")

        print(
            f"Hybrid Score: "
            f"{r['hybrid_score']:.4f}"
        )

        print(
            f"Semantic Score: "
            f"{r['semantic_score']:.4f}"
        )

        print("-" * 60)

        print(r["chunk_text"][:300])