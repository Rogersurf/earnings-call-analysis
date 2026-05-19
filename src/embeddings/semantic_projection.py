# ============================================================
# SEMANTIC PROJECTION
# Financial Semantic Intelligence Platform
# ============================================================

import os

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import umap

# ============================================================
# CONFIG
# ============================================================

EMBEDDINGS_DIR = "outputs/embeddings"

OUTPUT_DIR = "outputs/semantic_projection"

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
# LOOP
# ============================================================

for item in FILES:

    name = item["name"]

    print("\n===================================================")
    print(f"PROJECTING: {name}")
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
    # UMAP
    # ------------------------------------------------

    print("\nRunning UMAP projection...\n")

    reducer = umap.UMAP(

        n_neighbors=15,

        min_dist=0.1,

        n_components=2,

        metric="cosine",

        random_state=42
    )

    projection = reducer.fit_transform(
        embeddings
    )

    # ------------------------------------------------
    # DATAFRAME
    # ------------------------------------------------

    projection_df = metadata.copy()

    projection_df["x"] = projection[:, 0]

    projection_df["y"] = projection[:, 1]

    # ------------------------------------------------
    # SAVE CSV
    # ------------------------------------------------

    projection_df.to_csv(

        f"{OUTPUT_DIR}/{name}_projection.csv",

        index=False
    )

    # ------------------------------------------------
    # PLOT
    # ------------------------------------------------

    plt.figure(figsize=(14, 10))

    plt.scatter(

        projection_df["x"],

        projection_df["y"],

        s=8,

        alpha=0.6
    )

    plt.title(
        f"Semantic Projection - {name}"
    )

    plt.xlabel("UMAP Dimension 1")

    plt.ylabel("UMAP Dimension 2")

    plt.tight_layout()

    plt.savefig(

        f"{OUTPUT_DIR}/{name}_semantic_map.png",

        dpi=300
    )

    plt.close()

    # ------------------------------------------------
    # TOP COMPANIES
    # ------------------------------------------------

    print("\nTop projected companies:\n")

    print(

        projection_df[[

            "company",
            "ticker",
            "x",
            "y"

        ]].head(10)

    )

# ============================================================
# DONE
# ============================================================

print("\n===================================================")
print("SEMANTIC PROJECTION COMPLETED")
print("===================================================")

print(f"\nOutputs saved to: {OUTPUT_DIR}")