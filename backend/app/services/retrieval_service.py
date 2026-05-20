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