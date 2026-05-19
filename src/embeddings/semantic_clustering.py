# ============================================================
# SEMANTIC CLUSTERING
# Financial Semantic Intelligence Platform
# ============================================================

import os

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import hdbscan

from collections import Counter

# ============================================================
# CONFIG
# ============================================================

EMBEDDINGS_DIR = "outputs/embeddings"

PROJECTION_DIR = "outputs/semantic_projection"

OUTPUT_DIR = "outputs/semantic_clustering"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# FILES
# ============================================================

FILES = [

    {
        "name": "summary",

        "embedding_file":
            f"{EMBEDDINGS_DIR}/summary_embeddings.npy",

        "projection_file":
            f"{PROJECTION_DIR}/summary_projection.csv"
    },

    {
        "name": "takeaways",

        "embedding_file":
            f"{EMBEDDINGS_DIR}/takeaways_embeddings.npy",

        "projection_file":
            f"{PROJECTION_DIR}/takeaways_projection.csv"
    }
]

# ============================================================
# LOOP
# ============================================================

for item in FILES:

    name = item["name"]

    print("\n===================================================")
    print(f"CLUSTERING: {name}")
    print("===================================================\n")

    # ------------------------------------------------
    # LOAD
    # ------------------------------------------------

    embeddings = np.load(
        item["embedding_file"]
    )

    projection_df = pd.read_csv(
        item["projection_file"]
    )

    print(f"Embeddings shape: {embeddings.shape}")

    # ------------------------------------------------
    # HDBSCAN
    # ------------------------------------------------

    print("\nRunning HDBSCAN clustering...\n")

    clusterer = hdbscan.HDBSCAN(

        min_cluster_size=8,

        min_samples=4,

        metric='euclidean',

        cluster_selection_method='eom',

        prediction_data=True
    )

    cluster_labels = clusterer.fit_predict(
        embeddings
    )

    # ------------------------------------------------
    # STORE LABELS
    # ------------------------------------------------

    projection_df["cluster"] = cluster_labels

    projection_df["outlier_score"] = (
        clusterer.outlier_scores_
    )

    # ------------------------------------------------
    # BASIC STATS
    # ------------------------------------------------

    total_clusters = len(

        set(cluster_labels)
    )

    noise_points = np.sum(
        cluster_labels == -1
    )

    print(f"Total clusters: {total_clusters}")

    print(f"Noise points: {noise_points}")

    # ------------------------------------------------
    # CLUSTER COUNTS
    # ------------------------------------------------

    cluster_counts = Counter(
        cluster_labels
    )

    cluster_df = pd.DataFrame({

        "cluster":
            list(cluster_counts.keys()),

        "count":
            list(cluster_counts.values())
    })

    cluster_df = cluster_df.sort_values(

        by="count",

        ascending=False
    )

    # ------------------------------------------------
    # SAVE CLUSTER CSV
    # ------------------------------------------------

    projection_df.to_csv(

        f"{OUTPUT_DIR}/{name}_clusters.csv",

        index=False
    )

    cluster_df.to_csv(

        f"{OUTPUT_DIR}/{name}_cluster_sizes.csv",

        index=False
    )

    # ------------------------------------------------
    # PRINT TOP CLUSTERS
    # ------------------------------------------------

    print("\n==============================")
    print("TOP CLUSTERS")
    print("==============================\n")

    print(cluster_df.head(20))

    # ------------------------------------------------
    # TOP COMPANIES PER CLUSTER
    # ------------------------------------------------

    print("\n==============================")
    print("TOP COMPANIES PER CLUSTER")
    print("==============================\n")

    top_clusters = cluster_df[
        cluster_df["cluster"] != -1
    ].head(10)

    cluster_examples = []

    for cluster_id in top_clusters["cluster"]:

        cluster_subset = projection_df[

            projection_df["cluster"]
            == cluster_id

        ]

        sample_companies = cluster_subset[
            "company"
        ].head(10).tolist()

        cluster_examples.append({

            "cluster":
                cluster_id,

            "size":
                len(cluster_subset),

            "companies":
                sample_companies
        })

        print(f"\nCLUSTER {cluster_id}")

        print(f"SIZE: {len(cluster_subset)}")

        print("COMPANIES:")

        for company in sample_companies:

            print(f" - {company}")

    # ------------------------------------------------
    # CLUSTER PLOT
    # ------------------------------------------------

    plt.figure(figsize=(16, 12))

    scatter = plt.scatter(

        projection_df["x"],

        projection_df["y"],

        c=projection_df["cluster"],

        s=8,

        alpha=0.7
    )

    plt.title(
        f"Semantic Clusters - {name}"
    )

    plt.xlabel("UMAP Dimension 1")

    plt.ylabel("UMAP Dimension 2")

    plt.tight_layout()

    plt.savefig(

        f"{OUTPUT_DIR}/{name}_semantic_clusters.png",

        dpi=300
    )

    plt.close()

    # ------------------------------------------------
    # CLUSTER SIZE HISTOGRAM
    # ------------------------------------------------

    plt.figure(figsize=(12, 6))

    plt.hist(

        cluster_df[
            cluster_df["cluster"] != -1
        ]["count"],

        bins=30
    )

    plt.title(
        f"Cluster Size Distribution - {name}"
    )

    plt.xlabel("Cluster Size")

    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(

        f"{OUTPUT_DIR}/{name}_cluster_size_distribution.png",

        dpi=300
    )

    plt.close()

    # ------------------------------------------------
    # OUTLIER PLOT
    # ------------------------------------------------

    plt.figure(figsize=(12, 6))

    plt.hist(

        projection_df["outlier_score"],

        bins=50
    )

    plt.title(
        f"Outlier Score Distribution - {name}"
    )

    plt.xlabel("Outlier Score")

    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(

        f"{OUTPUT_DIR}/{name}_outlier_distribution.png",

        dpi=300
    )

    plt.close()

# ============================================================
# DONE
# ============================================================

print("\n===================================================")
print("SEMANTIC CLUSTERING COMPLETED")
print("===================================================")

print(f"\nOutputs saved to: {OUTPUT_DIR}")