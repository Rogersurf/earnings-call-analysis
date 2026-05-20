# ============================================================
# FILE: src/kg/community_labeling.py
# ============================================================
#
# PURPOSE:
# Generate semantic labels for chunk communities
#
# INPUT:
# outputs/chunk_clusters/semantic_chunk_clusters.parquet
#
# OUTPUT:
# outputs/community_labeling/
#   ├── community_labels.csv
#   ├── community_labels.json
#   └── semantic_chunk_clusters_labeled.parquet
#
# ============================================================

import os
import re
import json

import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import (
    CountVectorizer
)

# ============================================================
# CONFIG
# ============================================================

INPUT_FILE = (
    "outputs/chunk_clusters/"
    "semantic_chunk_clusters.parquet"
)

OUTPUT_DIR = (
    "outputs/community_labeling"
)

TOP_KEYWORDS = 15

MIN_COMMUNITY_SIZE = 5

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# ============================================================
# LOAD DATA
# ============================================================

print("\n===================================================")
print("LOADING CLUSTERED CHUNKS")
print("===================================================\n")

df = pd.read_parquet(
    INPUT_FILE
)

print(f"Dataset shape: {df.shape}")

# ============================================================
# VALIDATION
# ============================================================

required_columns = [

    "cluster",
    "chunk_text"

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
# CLEAN TEXT
# ============================================================

def clean_text(text):

    text = str(text)

    text = text.lower()

    text = re.sub(
        r"[^a-zA-Z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()

# ============================================================
# BUILD COMMUNITY DOCUMENTS
# ============================================================

print("\n===================================================")
print("BUILDING COMMUNITY DOCUMENTS")
print("===================================================\n")

community_documents = {}

community_sizes = {}

for cluster_id, group in df.groupby("cluster"):

    # --------------------------------------------------------
    # SKIP NOISE CLUSTER
    # --------------------------------------------------------

    if cluster_id == -1:

        continue

    # --------------------------------------------------------
    # SKIP SMALL COMMUNITIES
    # --------------------------------------------------------

    if len(group) < MIN_COMMUNITY_SIZE:

        continue

    # --------------------------------------------------------
    # EXTRACT TEXTS
    # --------------------------------------------------------

    texts = group[
        "chunk_text"
    ].fillna("").astype(str)

    cleaned_texts = [

        clean_text(t)

        for t in texts
    ]

    combined_text = " ".join(
        cleaned_texts
    )

    community_documents[
        cluster_id
    ] = combined_text

    community_sizes[
        cluster_id
    ] = len(group)

print(
    f"Communities analyzed: "
    f"{len(community_documents)}"
)

# ============================================================
# VECTORIZE COMMUNITIES
# ============================================================

print("\n===================================================")
print("EXTRACTING KEYWORDS")
print("===================================================\n")

vectorizer = CountVectorizer(

    stop_words="english",

    max_features=10000,

    ngram_range=(1, 2)

)

community_ids = list(
    community_documents.keys()
)

community_texts = [

    community_documents[c]

    for c in community_ids
]

X = vectorizer.fit_transform(
    community_texts
)

feature_names = np.array(
    vectorizer.get_feature_names_out()
)

# ============================================================
# GENERATE LABELS
# ============================================================

community_results = []

for idx, cluster_id in enumerate(community_ids):

    row = X[idx].toarray()[0]

    top_indices = row.argsort()[::-1]

    keywords = []

    for i in top_indices:

        if row[i] == 0:

            continue

        keyword = feature_names[i]

        keywords.append(
            keyword
        )

        if len(keywords) >= TOP_KEYWORDS:

            break

    # --------------------------------------------------------
    # GENERATE SEMANTIC LABEL
    # --------------------------------------------------------

    label = " / ".join(
        keywords[:3]
    )

    community_results.append({

        "cluster_id":
            int(cluster_id),

        "community_label":
            label,

        "community_size":
            int(
                community_sizes[cluster_id]
            ),

        "top_keywords":
            ", ".join(keywords)

    })

# ============================================================
# CREATE DATAFRAME
# ============================================================

community_df = pd.DataFrame(
    community_results
)

community_df = community_df.sort_values(

    by="community_size",

    ascending=False
)

# ============================================================
# SAVE CSV
# ============================================================

csv_output = os.path.join(

    OUTPUT_DIR,

    "community_labels.csv"
)

community_df.to_csv(

    csv_output,

    index=False
)

# ============================================================
# SAVE JSON
# ============================================================

json_output = os.path.join(

    OUTPUT_DIR,

    "community_labels.json"
)

with open(

    json_output,

    "w"

) as f:

    json.dump(

        community_results,

        f,

        indent=4
    )

# ============================================================
# MAP LABELS BACK TO DATASET
# ============================================================

print("\n===================================================")
print("MAPPING LABELS TO DATASET")
print("===================================================\n")

label_mapping = {

    row["cluster_id"]:
        row["community_label"]

    for _, row in
    community_df.iterrows()
}

df["community_label"] = df[
    "cluster"
].map(label_mapping)

df["community_label"] = df[
    "community_label"
].fillna("unclassified")

# ============================================================
# SAVE LABELED DATASET
# ============================================================

labeled_output = os.path.join(

    OUTPUT_DIR,

    "semantic_chunk_clusters_labeled.parquet"
)

df.to_parquet(

    labeled_output,

    index=False
)

# ============================================================
# PRINT TOP COMMUNITIES
# ============================================================

print("\n===================================================")
print("TOP COMMUNITIES")
print("===================================================\n")

print(
    community_df.head(20)
)

# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n===================================================")
print("COMMUNITY LABELING COMPLETED")
print("===================================================\n")

print("Saved files:\n")

print(csv_output)
print(json_output)
print(labeled_output)