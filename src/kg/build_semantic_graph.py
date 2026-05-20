# ============================================================
# FILE: src/kg/build_semantic_graph.py
# ============================================================
#
# PURPOSE:
# Build a semantic similarity graph from chunk embeddings
#
# INPUT:
# outputs/chunks/semantic_chunks_embeddings.parquet
#
# OUTPUT:
# outputs/graph/
#   ├── semantic_nodes.parquet
#   ├── semantic_edges.parquet
#   ├── semantic_graph.gexf
#   └── graph_stats.csv
#
# ============================================================

import os
import numpy as np
import pandas as pd
import networkx as nx

from tqdm import tqdm
from sklearn.neighbors import NearestNeighbors

# ============================================================
# CONFIG
# ============================================================

INPUT_PATH = "outputs/chunks/semantic_chunks_embeddings.parquet"

OUTPUT_DIR = "outputs/graph"

TOP_K = 15
SIMILARITY_THRESHOLD = 0.65

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# LOAD DATA
# ============================================================

print("\n===================================================")
print("LOADING EMBEDDINGS")
print("===================================================\n")

df = pd.read_parquet(INPUT_PATH)

print("Dataset shape:")
print(df.shape)

# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "embedding",
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
# EXTRACT EMBEDDINGS
# ============================================================

print("\nExtracting embeddings...\n")

embeddings = np.vstack(df["embedding"].values)

print("Embeddings shape:")
print(embeddings.shape)

# ============================================================
# BUILD KNN INDEX
# ============================================================

print("\n===================================================")
print("BUILDING KNN INDEX")
print("===================================================\n")

nn = NearestNeighbors(
    n_neighbors=TOP_K + 1,
    metric="cosine",
    algorithm="brute"
)

nn.fit(embeddings)

distances, indices = nn.kneighbors(embeddings)

# ============================================================
# CREATE GRAPH
# ============================================================

print("\n===================================================")
print("CREATING SEMANTIC GRAPH")
print("===================================================\n")

G = nx.Graph()

# ============================================================
# ADD NODES
# ============================================================

print("Adding nodes...\n")

for idx, row in tqdm(df.iterrows(), total=len(df)):

    G.add_node(
        idx,

        company=row.get("company", ""),
        ticker=row.get("ticker", ""),
        sector=row.get("sector", ""),
        source_layer=row.get("source_layer", ""),

        chunk=row.get("chunk", ""),
        chunk_size_words=row.get("chunk_size_words", 0)
    )

# ============================================================
# ADD EDGES
# ============================================================

print("\nAdding edges...\n")

edges_data = []

for i in tqdm(range(len(embeddings))):

    source_idx = i

    neighbor_idxs = indices[i][1:]
    neighbor_distances = distances[i][1:]

    for target_idx, dist in zip(
        neighbor_idxs,
        neighbor_distances
    ):

        similarity = 1 - dist

        if similarity >= SIMILARITY_THRESHOLD:

            G.add_edge(
                source_idx,
                int(target_idx),
                weight=float(similarity)
            )

            edges_data.append({

                "source": source_idx,
                "target": int(target_idx),

                "similarity": float(similarity)
            })

# ============================================================
# GRAPH STATS
# ============================================================

print("\n===================================================")
print("GRAPH STATS")
print("===================================================\n")

num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()

density = nx.density(G)

connected_components = nx.number_connected_components(G)

print(f"Nodes: {num_nodes:,}")
print(f"Edges: {num_edges:,}")
print(f"Density: {density:.8f}")
print(f"Connected Components: {connected_components:,}")

# ============================================================
# CENTRALITY METRICS
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
# CREATE NODES DATAFRAME
# ============================================================

print("\nCreating nodes dataframe...\n")

nodes_data = []

for node in tqdm(G.nodes()):

    attrs = G.nodes[node]

    nodes_data.append({

        "node_id": node,

        "company": attrs.get("company", ""),
        "ticker": attrs.get("ticker", ""),
        "sector": attrs.get("sector", ""),
        "source_layer": attrs.get("source_layer", ""),

        "chunk": attrs.get("chunk", ""),

        "degree": G.degree(node),

        "degree_centrality":
            degree_centrality.get(node, 0),

        "betweenness_centrality":
            betweenness_centrality.get(node, 0)
    })

nodes_df = pd.DataFrame(nodes_data)

# ============================================================
# CREATE EDGES DATAFRAME
# ============================================================

print("\nCreating edges dataframe...\n")

edges_df = pd.DataFrame(edges_data)

# ============================================================
# SAVE DATAFRAMES
# ============================================================

print("\n===================================================")
print("SAVING FILES")
print("===================================================\n")

nodes_output = os.path.join(
    OUTPUT_DIR,
    "semantic_nodes.parquet"
)

edges_output = os.path.join(
    OUTPUT_DIR,
    "semantic_edges.parquet"
)

gexf_output = os.path.join(
    OUTPUT_DIR,
    "semantic_graph.gexf"
)

stats_output = os.path.join(
    OUTPUT_DIR,
    "graph_stats.csv"
)

nodes_df.to_parquet(
    nodes_output,
    index=False
)

edges_df.to_parquet(
    edges_output,
    index=False
)

# ============================================================
# SAVE GEXF GRAPH
# ============================================================

print("Saving GEXF graph...\n")

nx.write_gexf(
    G,
    gexf_output
)

# ============================================================
# SAVE GRAPH STATS
# ============================================================

stats_df = pd.DataFrame([{

    "nodes": num_nodes,
    "edges": num_edges,

    "density": density,

    "connected_components":
        connected_components
}])

stats_df.to_csv(
    stats_output,
    index=False
)

# ============================================================
# TOP CENTRAL NODES
# ============================================================

print("\n===================================================")
print("TOP CENTRAL NODES")
print("===================================================\n")

top_nodes = nodes_df.sort_values(
    "degree_centrality",
    ascending=False
).head(20)

print(
    top_nodes[
        [
            "company",
            "ticker",
            "degree",
            "degree_centrality"
        ]
    ]
)

# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n===================================================")
print("SEMANTIC GRAPH COMPLETED")
print("===================================================\n")

print("Saved files:\n")

print(nodes_output)
print(edges_output)
print(gexf_output)
print(stats_output)

print("\nNow open the .gexf file in Gephi.\n")