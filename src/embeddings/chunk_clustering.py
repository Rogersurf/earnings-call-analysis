import os
import ast
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from tqdm import tqdm

from umap import UMAP

import hdbscan

from sklearn.feature_extraction.text import CountVectorizer

# =========================================================
# CONFIG
# =========================================================

INPUT_PATH = "outputs/chunks/semantic_chunks.parquet"

OUTPUT_DIR = "outputs/chunk_clusters"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================================================
# LOAD DATA
# =========================================================

print("\nLoading semantic chunks...\n")

df = pd.read_parquet(INPUT_PATH)

print(df.shape)

# =========================================================
# LOAD EMBEDDINGS
# =========================================================

print("\nLoading embeddings matrix...\n")

embeddings = np.array(df["embedding"].tolist())

print(embeddings.shape)

# =========================================================
# REMOVE INVALID
# =========================================================

valid_mask = ~np.isnan(embeddings).any(axis=1)

df = df[valid_mask].reset_index(drop=True)

embeddings = embeddings[valid_mask]

print("\nAfter cleaning:\n")

print(df.shape)
print(embeddings.shape)

# =========================================================
# UMAP REDUCTION
# =========================================================

print("\nRunning UMAP reduction...\n")

umap_model = UMAP(
    n_neighbors=25,
    n_components=15,
    min_dist=0.0,
    metric="cosine",
    random_state=42
)

reduced_embeddings = umap_model.fit_transform(
    embeddings
)

print(reduced_embeddings.shape)

# =========================================================
# HDBSCAN CLUSTERING
# =========================================================

print("\nRunning HDBSCAN clustering...\n")

clusterer = hdbscan.HDBSCAN(
    min_cluster_size=25,
    min_samples=8,
    metric="euclidean",
    cluster_selection_method="eom",
    prediction_data=True
)

cluster_labels = clusterer.fit_predict(
    reduced_embeddings
)

df["cluster"] = cluster_labels

# =========================================================
# OUTLIER SCORES
# =========================================================

df["outlier_score"] = clusterer.outlier_scores_

# =========================================================
# CLUSTER STATS
# =========================================================

print("\n==============================")
print("CLUSTER STATS")
print("==============================\n")

n_clusters = len(
    set(cluster_labels)
) - (1 if -1 in cluster_labels else 0)

noise_points = np.sum(cluster_labels == -1)

print(f"Total clusters: {n_clusters}")
print(f"Noise points: {noise_points}")

cluster_counts = (
    df["cluster"]
    .value_counts()
    .sort_index()
)

print("\nCluster distribution:\n")

print(cluster_counts.head(30))

# =========================================================
# TOPIC EXTRACTION
# =========================================================

print("\n==============================")
print("EXTRACTING CLUSTER TOPICS")
print("==============================\n")

vectorizer = CountVectorizer(
    stop_words="english",
    max_features=10000,
    ngram_range=(1, 2)
)

vectorizer.fit(df["chunk_text"])

feature_names = np.array(
    vectorizer.get_feature_names_out()
)

cluster_topics = []

for cluster_id in sorted(df["cluster"].unique()):

    if cluster_id == -1:
        continue

    cluster_texts = df[
        df["cluster"] == cluster_id
    ]["chunk_text"]

    if len(cluster_texts) < 5:
        continue

    X = vectorizer.transform(cluster_texts)

    word_counts = np.asarray(
        X.sum(axis=0)
    ).flatten()

    top_indices = word_counts.argsort()[-15:][::-1]

    top_words = feature_names[top_indices]

    cluster_size = len(cluster_texts)

    top_companies = (
        df[df["cluster"] == cluster_id]["company"]
        .value_counts()
        .head(10)
        .index
        .tolist()
    )

    print("\n===================================")
    print(f"CLUSTER {cluster_id}")
    print("===================================\n")

    print(f"SIZE: {cluster_size}")

    print("\nTOP WORDS:\n")

    print(", ".join(top_words))

    print("\nTOP COMPANIES:\n")

    for c in top_companies:
        print(f"- {c}")

    cluster_topics.append({

        "cluster": cluster_id,
        "size": cluster_size,

        "top_words": ", ".join(top_words),

        "top_companies": ", ".join(top_companies)

    })

# =========================================================
# SAVE TOPICS
# =========================================================

topics_df = pd.DataFrame(cluster_topics)

topics_path = os.path.join(
    OUTPUT_DIR,
    "cluster_topics.csv"
)

topics_df.to_csv(
    topics_path,
    index=False
)

# =========================================================
# 2D UMAP FOR VISUALIZATION
# =========================================================

print("\nRunning 2D UMAP projection...\n")

umap_2d = UMAP(
    n_neighbors=25,
    n_components=2,
    min_dist=0.0,
    metric="cosine",
    random_state=42
)

projection_2d = umap_2d.fit_transform(
    embeddings
)

df["x"] = projection_2d[:, 0]
df["y"] = projection_2d[:, 1]

# =========================================================
# SAVE PROJECTION
# =========================================================

projection_path = os.path.join(
    OUTPUT_DIR,
    "chunk_projection.parquet"
)

df.to_parquet(projection_path)

# =========================================================
# PLOT CLUSTERS
# =========================================================

print("\nGenerating plots...\n")

plt.figure(figsize=(14, 10))

scatter = plt.scatter(
    df["x"],
    df["y"],
    c=df["cluster"],
    s=8,
    cmap="tab20",
    alpha=0.7
)

plt.title(
    "Semantic Chunk Clusters",
    fontsize=18
)

plt.xlabel("UMAP Dimension 1")
plt.ylabel("UMAP Dimension 2")

plot_path = os.path.join(
    OUTPUT_DIR,
    "semantic_chunk_clusters.png"
)

plt.savefig(
    plot_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# =========================================================
# OUTLIER HISTOGRAM
# =========================================================

plt.figure(figsize=(12, 6))

plt.hist(
    df["outlier_score"],
    bins=50
)

plt.title(
    "Outlier Score Distribution",
    fontsize=18
)

plt.xlabel("Outlier Score")
plt.ylabel("Frequency")

hist_path = os.path.join(
    OUTPUT_DIR,
    "outlier_distribution.png"
)

plt.savefig(
    hist_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# =========================================================
# CLUSTER SIZE HISTOGRAM
# =========================================================

valid_clusters = df[df["cluster"] != -1]

cluster_sizes = (
    valid_clusters["cluster"]
    .value_counts()
)

plt.figure(figsize=(12, 6))

plt.hist(
    cluster_sizes,
    bins=30
)

plt.title(
    "Cluster Size Distribution",
    fontsize=18
)

plt.xlabel("Cluster Size")
plt.ylabel("Frequency")

cluster_hist_path = os.path.join(
    OUTPUT_DIR,
    "cluster_size_distribution.png"
)

plt.savefig(
    cluster_hist_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# =========================================================
# SAVE FINAL DATASET
# =========================================================

final_path = os.path.join(
    OUTPUT_DIR,
    "semantic_chunk_clusters.parquet"
)

df.to_parquet(final_path)

# =========================================================
# FINAL OUTPUT
# =========================================================

print("\n===================================")
print("CHUNK CLUSTERING COMPLETED")
print("===================================\n")

print(f"Clusters found: {n_clusters}")

print("\nSaved outputs:\n")

print(topics_path)
print(projection_path)
print(final_path)
print(plot_path)

print("\nDone.\n")