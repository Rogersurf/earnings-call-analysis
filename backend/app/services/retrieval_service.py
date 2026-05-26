from pathlib import Path

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
# SEMANTIC SEARCH
# ======================================================

def semantic_search(
    query: str,
    top_k: int = 10
):

    # ==============================================
    # ENCODE QUERY
    # ==============================================

    query_embedding = model.encode([query])

    # ==============================================
    # COSINE SIMILARITY
    # ==============================================

    similarities = cosine_similarity(
        query_embedding,
        embeddings_matrix
    )[0]

    # ==============================================
    # TOP RESULTS
    # ==============================================

    top_indices = similarities.argsort()[-top_k:][::-1]

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

            "similarity":
                float(similarities[idx])

        })

    return results

# ======================================================
# GRAPH EXPANSION
# ======================================================

def semantic_graph_expansion(

    query: str,

    top_k: int = 3,

    neighbors_per_chunk: int = 2,
):

    # ==============================================
    # QUERY EMBEDDING
    # ==============================================

    query_embedding = model.encode([query])

    # ==============================================
    # QUERY SIMILARITIES
    # ==============================================

    similarities = cosine_similarity(
        query_embedding,
        embeddings_matrix
    )[0]

    # ==============================================
    # TOP QUERY MATCHES
    # ==============================================

    top_indices = similarities.argsort()[-top_k:][::-1]

    # ==============================================
    # GRAPH STRUCTURES
    # ==============================================

    nodes = {}
    edges = []

    # ==============================================
    # EXPAND EACH MATCH
    # ==============================================

    for idx in top_indices:

        row = df.iloc[idx]

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

                "x": int(idx % 5 * 250),
                "y": int(idx // 5 * 200),
            },

            "data": {

                "label":
                    f"{row['company']} ({row['ticker']})",

                "chunk":
                    row["chunk_text"][:120],
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