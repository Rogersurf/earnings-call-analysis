# ============================================================
# SEMANTIC SIMILARITY ANALYSIS
# Financial Semantic Intelligence Platform
# ============================================================

import os
import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances

import matplotlib.pyplot as plt

# ============================================================
# CONFIG
# ============================================================

EMBEDDINGS_DIR = "outputs/embeddings"

OUTPUT_DIR = "outputs/semantic_similarity"

TOP_N = 20

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# FILES
# ============================================================

FILES = [

    {
        "name": "summary",
        "embedding_file":
            f"{EMBEDDINGS_DIR}/summary_embeddings.npy",

        "metadata_file":
            f"{EMBEDDINGS_DIR}/summary_metadata.csv"
    },

    {
        "name": "takeaways",
        "embedding_file":
            f"{EMBEDDINGS_DIR}/takeaways_embeddings.npy",

        "metadata_file":
            f"{EMBEDDINGS_DIR}/takeaways_metadata.csv"
    }
]

# ============================================================
# ANALYSIS LOOP
# ============================================================

for item in FILES:

    name = item["name"]

    print("\n===================================================")
    print(f"ANALYZING: {name}")
    print("===================================================\n")

    # ------------------------------------------------
    # LOAD
    # ------------------------------------------------

    embeddings = np.load(
        item["embedding_file"]
    )

    metadata = pd.read_csv(
        item["metadata_file"]
    )

    print(f"Embeddings shape: {embeddings.shape}")

    # ------------------------------------------------
    # COSINE SIMILARITY
    # ------------------------------------------------

    print("\nCalculating cosine similarity...")

    cosine_matrix = cosine_similarity(
        embeddings
    )

    # ------------------------------------------------
    # EUCLIDEAN DISTANCE
    # ------------------------------------------------

    print("\nCalculating euclidean distance...")

    distance_matrix = euclidean_distances(
        embeddings
    )

    # ------------------------------------------------
    # TOP SIMILARITIES
    # ------------------------------------------------

    similarity_results = []

    num_docs = len(metadata)

    for i in range(num_docs):

        # --------------------------------------------
        # SORT NEIGHBORS
        # --------------------------------------------

        similar_idx = np.argsort(
            cosine_matrix[i]
        )[::-1]

        # remove self

        similar_idx = similar_idx[1:TOP_N+1]

        # --------------------------------------------
        # STORE RESULTS
        # --------------------------------------------

        for j in similar_idx:

            similarity_results.append({

                "source_company":
                    metadata.iloc[i]["company"],

                "source_ticker":
                    metadata.iloc[i]["ticker"],

                "target_company":
                    metadata.iloc[j]["company"],

                "target_ticker":
                    metadata.iloc[j]["ticker"],

                "cosine_similarity":
                    round(
                        cosine_matrix[i][j],
                        4
                    ),

                "euclidean_distance":
                    round(
                        distance_matrix[i][j],
                        4
                    )
            })

    # ------------------------------------------------
    # DATAFRAME
    # ------------------------------------------------

    similarity_df = pd.DataFrame(
        similarity_results
    )

    # ------------------------------------------------
    # SORT
    # ------------------------------------------------

    similarity_df = similarity_df.sort_values(

        by="cosine_similarity",

        ascending=False
    )

    # ------------------------------------------------
    # SAVE CSV
    # ------------------------------------------------

    similarity_df.to_csv(

        f"{OUTPUT_DIR}/{name}_similarities.csv",

        index=False
    )

    # ------------------------------------------------
    # TOP RESULTS
    # ------------------------------------------------

    print("\n==============================")
    print(f"TOP SIMILARITIES -> {name}")
    print("==============================\n")

    print(similarity_df.head(20))

    # ------------------------------------------------
    # COSINE DISTRIBUTION
    # ------------------------------------------------

    plt.figure(figsize=(12, 6))

    plt.hist(
        similarity_df["cosine_similarity"],
        bins=50
    )

    plt.title(
        f"Cosine Similarity Distribution - {name}"
    )

    plt.xlabel("Cosine Similarity")

    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/{name}_cosine_distribution.png"
    )

    plt.close()

    # ------------------------------------------------
    # DISTANCE DISTRIBUTION
    # ------------------------------------------------

    plt.figure(figsize=(12, 6))

    plt.hist(
        similarity_df["euclidean_distance"],
        bins=50
    )

    plt.title(
        f"Euclidean Distance Distribution - {name}"
    )

    plt.xlabel("Euclidean Distance")

    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/{name}_distance_distribution.png"
    )

    plt.close()

# ============================================================
# DONE
# ============================================================

print("\n===================================================")
print("SEMANTIC SIMILARITY COMPLETED")
print("===================================================")

print(f"\nOutputs saved to: {OUTPUT_DIR}")