# ============================================================
# FILE: src/rag/graph_retrieval.py
# ============================================================
#
# PURPOSE:
# Graph-aware semantic retrieval engine
#
# Combines:
# - semantic similarity
# - graph topology
# - community relationships
# - propagation candidates
#
# INPUTS:
#
# outputs/community_labeling/
#   semantic_chunk_clusters_labeled.parquet
#
# outputs/graph/
#   semantic_graph.gexf
#
# ============================================================

import networkx as nx
import numpy as np
import pandas as pd

from sentence_transformers import (
    SentenceTransformer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)

# ============================================================
# CONFIG
# ============================================================

PARQUET_FILE = (
    "outputs/community_labeling/"
    "semantic_chunk_clusters_labeled.parquet"
)

GRAPH_FILE = (
    "outputs/graph/"
    "semantic_graph.gexf"
)

MODEL_NAME = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

TOP_K = 5

GRAPH_NEIGHBORS = 5

# ============================================================
# LOAD DATA
# ============================================================

print("\n===================================================")
print("LOADING DATA")
print("===================================================\n")

df = pd.read_parquet(
    PARQUET_FILE
)

print(f"Dataset shape: {df.shape}")

# ============================================================
# VALIDATION
# ============================================================

required_columns = [

    "chunk_text",
    "embedding",
    "company",
    "ticker",
    "community_label"

]

missing_columns = [

    c for c in required_columns

    if c not in df.columns
]

if missing_columns:

    raise ValueError(
        f"Missing columns: {missing_columns}"
    )

# ============================================================
# LOAD EMBEDDINGS
# ============================================================

print("\n===================================================")
print("LOADING EMBEDDINGS")
print("===================================================\n")

embeddings = np.vstack(
    df["embedding"].values
)

print(
    f"Embeddings shape: "
    f"{embeddings.shape}"
)

# ============================================================
# LOAD MODEL
# ============================================================

print("\n===================================================")
print("LOADING SBERT")
print("===================================================\n")

model = SentenceTransformer(
    MODEL_NAME
)

# ============================================================
# LOAD GRAPH
# ============================================================

print("\n===================================================")
print("LOADING GRAPH")
print("===================================================\n")

G = nx.read_gexf(
    GRAPH_FILE
)

print(
    f"Graph nodes: "
    f"{G.number_of_nodes():,}"
)

print(
    f"Graph edges: "
    f"{G.number_of_edges():,}"
)

# ============================================================
# SEMANTIC RETRIEVAL
# ============================================================

def semantic_search(
    query,
    top_k=TOP_K
):

    print("\n===================================================")
    print("SEMANTIC SEARCH")
    print("===================================================\n")

    print(f"Query: {query}")

    # --------------------------------------------------------
    # EMBED QUERY
    # --------------------------------------------------------

    query_embedding = model.encode(
        [query]
    )

    # --------------------------------------------------------
    # COSINE SIMILARITY
    # --------------------------------------------------------

    similarities = cosine_similarity(

        query_embedding,
        embeddings

    )[0]

    # --------------------------------------------------------
    # TOP RESULTS
    # --------------------------------------------------------

    top_indices = similarities.argsort(
    )[::-1][:top_k]

    results = []

    for rank, idx in enumerate(top_indices):

        row = df.iloc[idx]

        result = {

            "node_id":
                str(idx),

            "rank":
                rank + 1,

            "similarity":
                float(
                    similarities[idx]
                ),

            "company":
                row.get(
                    "company",
                    ""
                ),

            "ticker":
                row.get(
                    "ticker",
                    ""
                ),

            "community":
                row.get(
                    "community_label",
                    "unclassified"
                ),

            "chunk":
                row.get(
                    "chunk_text",
                    ""
                )[:1000]
        }

        results.append(result)

    return results

# ============================================================
# GRAPH NEIGHBORS
# ============================================================

def get_graph_neighbors(
    node_id,
    max_neighbors=GRAPH_NEIGHBORS
):

    neighbors = []

    if node_id not in G:

        return neighbors

    for neighbor in G.neighbors(node_id):

        edge_data = G.get_edge_data(
            node_id,
            neighbor
        )

        weight = edge_data.get(
            "weight",
            0
        )

        neighbors.append({

            "neighbor_id":
                neighbor,

            "weight":
                float(weight)
        })

    neighbors = sorted(

        neighbors,

        key=lambda x: x["weight"],

        reverse=True
    )

    return neighbors[:max_neighbors]

# ============================================================
# DISPLAY RESULTS
# ============================================================

def display_results(results):

    print("\n===================================================")
    print("TOP SEMANTIC RESULTS")
    print("===================================================\n")

    for r in results:

        print(
            f"\nRANK: {r['rank']}"
        )

        print(
            f"SIMILARITY: "
            f"{r['similarity']:.4f}"
        )

        print(
            f"COMPANY: "
            f"{r['company']}"
        )

        print(
            f"TICKER: "
            f"{r['ticker']}"
        )

        print(
            f"COMMUNITY: "
            f"{r['community']}"
        )

        print("\nCHUNK:\n")

        print(r["chunk"])

        # ----------------------------------------------------
        # GRAPH NEIGHBORS
        # ----------------------------------------------------

        neighbors = get_graph_neighbors(
            r["node_id"]
        )

        print("\nGRAPH NEIGHBORS:\n")

        if not neighbors:

            print("No graph neighbors found.")

        for n in neighbors:

            try:

                neighbor_row = df.iloc[
                    int(n["neighbor_id"])
                ]

                print(
                    f"- "
                    f"{neighbor_row['company']} "
                    f"({neighbor_row['ticker']}) "
                    f"| weight="
                    f"{n['weight']:.4f}"
                )

            except:

                continue

        print("\n" + "=" * 70)

# ============================================================
# INTERACTIVE LOOP
# ============================================================

if __name__ == "__main__":

    print("\n===================================================")
    print("GRAPH-AWARE SEMANTIC RETRIEVAL")
    print("===================================================\n")

    while True:

        query = input(
            "\nEnter query "
            "(or 'exit'): "
        )

        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        if query.lower() == "exit":

            print("\nExiting...\n")

            break

        # ----------------------------------------------------
        # EMPTY QUERY
        # ----------------------------------------------------

        if not query.strip():

            print("\nEmpty query.\n")

            continue

        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        results = semantic_search(
            query=query,
            top_k=TOP_K
        )

        display_results(results)