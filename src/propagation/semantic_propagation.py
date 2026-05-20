# ============================================================
# FILE: src/propagation/semantic_propagation.py
# ============================================================
#
# PURPOSE:
# Analyze semantic propagation across communities
#
# INPUT:
# outputs/community_labeling/
#   semantic_chunk_clusters_labeled.parquet
#
# OUTPUT:
# outputs/propagation/
#   ├── propagation_edges.parquet
#   ├── propagation_nodes.parquet
#   ├── propagation_graph.gexf
#   ├── propagation_stats.csv
#   └── top_propagation_bridges.csv
#
# ============================================================

import os
import numpy as np
import pandas as pd
import networkx as nx

from tqdm import tqdm
from collections import Counter

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

OUTPUT_DIR = (
    "outputs/propagation"
)

SIMILARITY_THRESHOLD = 0.80

TOP_K = 10

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# ============================================================
# LOAD DATA
# ============================================================

print("\n===================================================")
print("LOADING LABELED COMMUNITIES")
print("===================================================\n")

df = pd.read_parquet(
    INPUT_FILE
)

print("Dataset shape:")
print(df.shape)

# ============================================================
# VALIDATION
# ============================================================

required_columns = [

    "embedding",
    "community_label",
    "company",
    "ticker"

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
# EXTRACT EMBEDDINGS
# ============================================================

print("\n===================================================")
print("EXTRACTING EMBEDDINGS")
print("===================================================\n")

embeddings = np.vstack(
    df["embedding"].values
)

print("Embeddings shape:")
print(embeddings.shape)

# ============================================================
# BUILD PROPAGATION GRAPH
# ============================================================

print("\n===================================================")
print("BUILDING PROPAGATION GRAPH")
print("===================================================\n")

G = nx.Graph()

# ============================================================
# ADD NODES
# ============================================================

print("Adding nodes...\n")

for idx, row in tqdm(
    df.iterrows(),
    total=len(df)
):

    G.add_node(

        idx,

        company=row.get(
            "company",
            ""
        ),

        ticker=row.get(
            "ticker",
            ""
        ),

        community=row.get(
            "community_label",
            ""
        ),

        source_layer=row.get(
            "source_layer",
            ""
        ),

        cluster=row.get(
            "cluster",
            -1
        )
    )

# ============================================================
# CALCULATE COSINE MATRIX
# ============================================================

print("\n===================================================")
print("CALCULATING SIMILARITY MATRIX")
print("===================================================\n")

cosine_matrix = cosine_similarity(
    embeddings
)

# ============================================================
# CREATE PROPAGATION EDGES
# ============================================================

print("\n===================================================")
print("DETECTING PROPAGATION")
print("===================================================\n")

edges_data = []

num_docs = len(df)

for i in tqdm(range(num_docs)):

    similarities = cosine_matrix[i]

    top_neighbors = np.argsort(
        similarities
    )[::-1][1:TOP_K+1]

    source_community = df.iloc[i][
        "community_label"
    ]

    source_company = df.iloc[i][
        "company"
    ]

    for j in top_neighbors:

        similarity = similarities[j]

        if similarity < SIMILARITY_THRESHOLD:

            continue

        target_community = df.iloc[j][
            "community_label"
        ]

        target_company = df.iloc[j][
            "company"
        ]

        # ----------------------------------------------------
        # SKIP SAME COMMUNITY
        # ----------------------------------------------------

        if source_community == target_community:

            continue

        # ----------------------------------------------------
        # CREATE EDGE
        # ----------------------------------------------------

        G.add_edge(

            i,
            j,

            weight=float(similarity)
        )

        edges_data.append({

            "source_idx":
                i,

            "target_idx":
                int(j),

            "source_company":
                source_company,

            "target_company":
                target_company,

            "source_community":
                source_community,

            "target_community":
                target_community,

            "similarity":
                float(similarity)
        })

# ============================================================
# CREATE EDGES DATAFRAME
# ============================================================

print("\nCreating propagation dataframe...\n")

edges_df = pd.DataFrame(
    edges_data
)

# ============================================================
# PROPAGATION COUNTS
# ============================================================

print("\n===================================================")
print("ANALYZING PROPAGATION FLOWS")
print("===================================================\n")

community_pairs = []

for _, row in edges_df.iterrows():

    pair = (

        row["source_community"],
        row["target_community"]
    )

    community_pairs.append(pair)

pair_counter = Counter(
    community_pairs
)

propagation_summary = []

for pair, count in pair_counter.items():

    propagation_summary.append({

        "source_community":
            pair[0],

        "target_community":
            pair[1],

        "connection_count":
            count
    })

propagation_df = pd.DataFrame(
    propagation_summary
)

propagation_df = propagation_df.sort_values(

    by="connection_count",

    ascending=False
)

# ============================================================
# CENTRALITY ANALYSIS
# ============================================================

print("\n===================================================")
print("CALCULATING CENTRALITY")
print("===================================================\n")

degree_centrality = nx.degree_centrality(G)

betweenness_centrality = nx.betweenness_centrality(

    G,

    k=min(1000, len(G.nodes)),

    normalized=True,

    seed=42
)

# ============================================================
# CREATE NODE METRICS
# ============================================================

nodes_data = []

for node in tqdm(G.nodes()):

    attrs = G.nodes[node]

    nodes_data.append({

        "node_id":
            node,

        "company":
            attrs.get(
                "company",
                ""
            ),

        "ticker":
            attrs.get(
                "ticker",
                ""
            ),

        "community":
            attrs.get(
                "community",
                ""
            ),

        "degree":
            G.degree(node),

        "degree_centrality":
            degree_centrality.get(
                node,
                0
            ),

        "betweenness_centrality":
            betweenness_centrality.get(
                node,
                0
            )
    })

nodes_df = pd.DataFrame(
    nodes_data
)

# ============================================================
# GRAPH STATS
# ============================================================

print("\n===================================================")
print("GRAPH STATS")
print("===================================================\n")

num_nodes = G.number_of_nodes()

num_edges = G.number_of_edges()

density = nx.density(G)

connected_components = nx.number_connected_components(
    G
)

print(f"Nodes: {num_nodes:,}")

print(f"Edges: {num_edges:,}")

print(f"Density: {density:.8f}")

print(
    f"Connected Components: "
    f"{connected_components:,}"
)

# ============================================================
# SAVE FILES
# ============================================================

print("\n===================================================")
print("SAVING FILES")
print("===================================================\n")

edges_output = os.path.join(

    OUTPUT_DIR,

    "propagation_edges.parquet"
)

nodes_output = os.path.join(

    OUTPUT_DIR,

    "propagation_nodes.parquet"
)

summary_output = os.path.join(

    OUTPUT_DIR,

    "top_propagation_bridges.csv"
)

gexf_output = os.path.join(

    OUTPUT_DIR,

    "propagation_graph.gexf"
)

stats_output = os.path.join(

    OUTPUT_DIR,

    "propagation_stats.csv"
)

edges_df.to_parquet(
    edges_output,
    index=False
)

nodes_df.to_parquet(
    nodes_output,
    index=False
)

propagation_df.to_csv(
    summary_output,
    index=False
)

nx.write_gexf(
    G,
    gexf_output
)

stats_df = pd.DataFrame([{

    "nodes":
        num_nodes,

    "edges":
        num_edges,

    "density":
        density,

    "connected_components":
        connected_components
}])

stats_df.to_csv(
    stats_output,
    index=False
)

# ============================================================
# PRINT TOP PROPAGATION FLOWS
# ============================================================

print("\n===================================================")
print("TOP PROPAGATION FLOWS")
print("===================================================\n")

print(
    propagation_df.head(20)
)

# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n===================================================")
print("SEMANTIC PROPAGATION COMPLETED")
print("===================================================\n")

print("Saved files:\n")

print(edges_output)
print(nodes_output)
print(summary_output)
print(gexf_output)
print(stats_output)

print(
    "\nOpen propagation_graph.gexf "
    "inside Gephi.\n"
)