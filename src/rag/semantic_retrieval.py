# ============================================================
# FILE: src/rag/semantic_retrieval.py
# ============================================================
#
# PURPOSE:
# Semantic retrieval engine for
# Financial Semantic Intelligence Platform
#
# INPUT:
# outputs/community_labeling/
#   semantic_chunk_clusters_labeled.parquet
#
# FEATURES:
# - semantic search
# - chunk retrieval
# - community retrieval
# - company retrieval
# - similarity scoring
#
# ============================================================

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

INPUT_FILE = (
    "outputs/community_labeling/"
    "semantic_chunk_clusters_labeled.parquet"
)

MODEL_NAME = (
    "sentence-transformers/all-MiniLM-L6-v2"
)

TOP_K = 10

# ============================================================
# LOAD DATA
# ============================================================

print("\n===================================================")
print("LOADING SEMANTIC DATASET")
print("===================================================\n")

df = pd.read_parquet(
    INPUT_FILE
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

    col for col in required_columns

    if col not in df.columns
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

print(f"Embeddings shape: {embeddings.shape}")

# ============================================================
# LOAD MODEL
# ============================================================

print("\n===================================================")
print("LOADING SBERT MODEL")
print("===================================================\n")

model = SentenceTransformer(
    MODEL_NAME
)

# ============================================================
# SEMANTIC SEARCH FUNCTION
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

        similarity_score = similarities[idx]

        result = {

            "rank":
                rank + 1,

            "similarity":
                float(similarity_score),

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
                    ""
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
# DISPLAY RESULTS
# ============================================================

def display_results(results):

    print("\n===================================================")
    print("TOP RETRIEVAL RESULTS")
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

        print("\n" + "=" * 60)

# ============================================================
# INTERACTIVE LOOP
# ============================================================

if __name__ == "__main__":

    print("\n===================================================")
    print("FINANCIAL SEMANTIC RETRIEVAL")
    print("===================================================\n")

    while True:

        query = input(
            "\nEnter query "
            "(or 'exit'): "
        )

        if query.lower() == "exit":

            print("\nExiting...\n")

            break
        
        if not query.strip():

            print("Empty query.")

            continue

        results = semantic_search(
            query=query,
            top_k=TOP_K
        )

        display_results(results)