# ============================================================
# FILE: src/kg/build_semantic_graph.py
# ============================================================
#
# PURPOSE:
# Build a hybrid semantic propagation graph using:
#
# - Semantic similarity
# - Thematic overlap
# - Cross-sector semantic bridges
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

INPUT_PATH = (
    "outputs/chunks/"
    "semantic_chunks_embeddings.parquet"
)

OUTPUT_DIR = "outputs/graph"

TOP_K = 10

MIN_SEMANTIC_SIMILARITY = 0.55

MIN_HYBRID_SCORE = 0.65

MAX_NEIGHBORS_PER_NODE = 8

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# ============================================================
# THEMATIC KEYWORDS
# ============================================================

THEMATIC_KEYWORDS = {

    "ai": [
        "ai",
        "artificial intelligence",
        "machine learning",
        "llm",
        "foundation model",
        "inference"
    ],

    "infrastructure": [
        "datacenter",
        "data center",
        "cloud",
        "compute",
        "gpu",
        "server",
        "infrastructure"
    ],

    "energy": [
        "utilities",
        "electricity",
        "power",
        "grid",
        "energy demand"
    ],

    "semiconductors": [
        "nvidia",
        "amd",
        "chip",
        "chips",
        "gpu",
        "semiconductor"
    ],

    "supply_chain": [
        "china",
        "manufacturing",
        "logistics",
        "exports",
        "sourcing"
    ]
}

# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):

    if pd.isna(text):
        return ""

    return str(text).lower()

# ============================================================
# EXTRACT THEMES
# ============================================================

def extract_themes(text):

    text = normalize_text(text)

    themes_found = set()

    for theme, keywords in THEMATIC_KEYWORDS.items():

        for keyword in keywords:

            if keyword in text:

                themes_found.add(theme)

    return themes_found

# ============================================================
# COMPUTE THEMATIC OVERLAP
# ============================================================

def compute_thematic_overlap(

    source_text,
    target_text
):

    source_themes = extract_themes(
        source_text
    )

    target_themes = extract_themes(
        target_text
    )

    overlap = (
        source_themes
        &
        target_themes
    )

    return len(overlap)

# ============================================================
# COMPUTE HYBRID EDGE SCORE
# ============================================================

def compute_hybrid_edge_score(

    semantic_similarity,
    thematic_overlap,
    cross_sector
):

    score = semantic_similarity

    # ========================================================
    # THEMATIC BOOST
    # ========================================================

    score += thematic_overlap * 0.08

    # ========================================================
    # CROSS-SECTOR BOOST
    # ========================================================

    if cross_sector:

        score += 0.05

    return score

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
# VALIDATE REQUIRED COLUMNS
# ============================================================

required_columns = [
    "embedding",
    "chunk_text"
]

missing_columns = [

    col

    for col in required_columns

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

embeddings = np.vstack(
    df["embedding"].values
)

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

distances, indices = nn.kneighbors(
    embeddings
)

# ============================================================
# CREATE GRAPH
# ============================================================

print("\n===================================================")
print("CREATING HYBRID SEMANTIC GRAPH")
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

        sector=row.get(
            "sector",
            ""
        ),

        source_layer=row.get(
            "source_layer",
            ""
        ),

        chunk_text=row.get(
            "chunk_text",
            ""
        ),

        chunk_size_words=row.get(
            "chunk_size_words",
            0
        )
    )

# ============================================================
# ADD EDGES
# ============================================================

print("\nAdding edges...\n")

edges_data = []

for i in tqdm(range(len(embeddings))):

    source_idx = i

    source_row = df.iloc[source_idx]

    source_sector = source_row.get(
        "sector",
        ""
    )

    source_text = source_row.get(
        "chunk_text",
        ""
    )

    neighbor_idxs = indices[i][1:]

    neighbor_distances = distances[i][1:]

    neighbor_count = 0

    # ========================================================
    # PROCESS NEIGHBORS
    # ========================================================

    for target_idx, dist in zip(

        neighbor_idxs,
        neighbor_distances
    ):

        # ----------------------------------------------------
        # LIMIT MAX NEIGHBORS
        # ----------------------------------------------------

        if neighbor_count >= MAX_NEIGHBORS_PER_NODE:
            break

        # ----------------------------------------------------
        # SEMANTIC SIMILARITY
        # ----------------------------------------------------

        semantic_similarity = 1 - dist

        if (
            semantic_similarity
            <
            MIN_SEMANTIC_SIMILARITY
        ):
            continue

        # ----------------------------------------------------
        # TARGET DATA
        # ----------------------------------------------------

        target_row = df.iloc[target_idx]

        target_sector = target_row.get(
            "sector",
            ""
        )

        target_text = target_row.get(
            "chunk_text",
            ""
        )

        # ----------------------------------------------------
        # CROSS-SECTOR RELATION
        # ----------------------------------------------------

        cross_sector = (
            source_sector != target_sector
        )

        # ----------------------------------------------------
        # THEMATIC OVERLAP
        # ----------------------------------------------------

        thematic_overlap = (
            compute_thematic_overlap(

                source_text,
                target_text
            )
        )

        # ----------------------------------------------------
        # HYBRID SCORE
        # ----------------------------------------------------

        hybrid_score = (
            compute_hybrid_edge_score(

                semantic_similarity=
                    semantic_similarity,

                thematic_overlap=
                    thematic_overlap,

                cross_sector=
                    cross_sector
            )
        )

        # ----------------------------------------------------
        # FINAL FILTER
        # ----------------------------------------------------

        if hybrid_score < MIN_HYBRID_SCORE:
            continue

        # ----------------------------------------------------
        # AVOID DUPLICATE EDGES
        # ----------------------------------------------------

        if G.has_edge(

            source_idx,
            int(target_idx)
        ):
            continue

        # ----------------------------------------------------
        # ADD EDGE
        # ----------------------------------------------------

        G.add_edge(

            source_idx,

            int(target_idx),

            weight=float(hybrid_score),

            semantic_similarity=
                float(semantic_similarity),

            thematic_overlap=
                int(thematic_overlap),

            cross_sector=
                bool(cross_sector)
        )

        # ----------------------------------------------------
        # STORE EDGE DATA
        # ----------------------------------------------------

        edges_data.append({

            "source":
                source_idx,

            "target":
                int(target_idx),

            "semantic_similarity":
                float(semantic_similarity),

            "hybrid_score":
                float(hybrid_score),

            "thematic_overlap":
                int(thematic_overlap),

            "cross_sector":
                bool(cross_sector)
        })

        neighbor_count += 1

# ============================================================
# GRAPH STATISTICS
# ============================================================

print("\n===================================================")
print("GRAPH STATS")
print("===================================================\n")

num_nodes = G.number_of_nodes()

num_edges = G.number_of_edges()

density = nx.density(G)

connected_components = (
    nx.number_connected_components(G)
)

average_degree = np.mean([

    degree

    for _, degree in G.degree()
])

print(f"Nodes: {num_nodes:,}")

print(f"Edges: {num_edges:,}")

print(f"Density: {density:.8f}")

print(
    f"Connected Components: "
    f"{connected_components:,}"
)

print(
    f"Average Degree: "
    f"{average_degree:.2f}"
)

# ============================================================
# CENTRALITY METRICS
# ============================================================

print("\n===================================================")
print("CALCULATING CENTRALITY")
print("===================================================\n")

degree_centrality = (
    nx.degree_centrality(G)
)

betweenness_centrality = (
    nx.betweenness_centrality(

        G,

        k=min(
            1000,
            len(G.nodes)
        ),

        normalized=True,

        seed=42
    )
)

# ============================================================
# CREATE NODES DATAFRAME
# ============================================================

print("\nCreating nodes dataframe...\n")

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

        "sector":
            attrs.get(
                "sector",
                ""
            ),

        "source_layer":
            attrs.get(
                "source_layer",
                ""
            ),

        "chunk_text":
            attrs.get(
                "chunk_text",
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
# CREATE EDGES DATAFRAME
# ============================================================

print("\nCreating edges dataframe...\n")

edges_df = pd.DataFrame(
    edges_data
)

# ============================================================
# SAVE OUTPUT FILES
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

    "nodes":
        num_nodes,

    "edges":
        num_edges,

    "density":
        density,

    "connected_components":
        connected_components,

    "average_degree":
        average_degree
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
            "sector",
            "degree",
            "degree_centrality"
        ]
    ]
)

# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n===================================================")
print("HYBRID SEMANTIC GRAPH COMPLETED")
print("===================================================\n")

print("Saved files:\n")

print(nodes_output)
print(edges_output)
print(gexf_output)
print(stats_output)

print("\nOpen semantic_graph.gexf in Gephi.\n")