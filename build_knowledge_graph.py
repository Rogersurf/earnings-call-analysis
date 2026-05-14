#!/usr/bin/env python3
"""
build_knowledge_graph.py

Builds a corporate knowledge graph from earnings call transcripts.

Data Source:
- Hugging Face dataset

Nodes:
- Company
- Sector
- Signal

Edges:
- in_sector
- mentions_company
- mentions
- propagates_to
"""

import pickle
import re
from collections import Counter

import networkx as nx
import pandas as pd
import spacy
from datasets import load_dataset

# =========================================================
# CONFIG
# =========================================================

HF_DATASET = "Rogersurf/earnings-call-transcripts"

# TEST MODE
# later change to:
# split="train"
MAX_ROWS = 250

OUTPUT_GRAPH = "data/knowledge_graph.gpickle"
OUTPUT_GEXF = "data/knowledge_graph.gexf"
OUTPUT_NODES = "data/graph_nodes.csv"
OUTPUT_EDGES = "data/graph_edges.csv"

SUPPLY_CHAIN_TERMS = {
    "production",
    "capacity",
    "inventory",
    "supply",
    "stock",
    "infrastructure",
    "manufacturing",
    "orders",
    "capex",
    "backlog",
    "supply chain",
    "logistics",
    "component shortage",
    "demand",
    "pricing pressure",
    "margin pressure",
    "cloud capacity",
    "server infrastructure",
    "data center",
    "semiconductor",
    "wafer",
}

BAD_TERMS = {
    "cfo",
    "ceo",
    "cto",
    "q&a",
    "arr",
    "gpv",
    "eps",
    "fy",
    "ai",
    "sec",
}

TICKER_TO_SECTOR = {
    "NVDA": "Semiconductors",
    "AMD": "Semiconductors",
    "INTC": "Semiconductors",
    "TSM": "Semiconductors",
    "MU": "Semiconductors",
    "QCOM": "Semiconductors",
    "MSFT": "Cloud & Software",
    "AMZN": "Cloud & E-commerce",
    "GOOGL": "Cloud & Advertising",
    "META": "Social Media",
    "DELL": "Hardware",
    "HPQ": "Hardware",
    "AAPL": "Consumer Electronics",
    "TSLA": "Automotive",
    "GM": "Automotive",
    "F": "Automotive",
    "UBER": "Mobility",
}

DEFAULT_SECTOR = "Other"

# =========================================================
# LOAD DATASET
# =========================================================

print("📥 Loading dataset from Hugging Face...")

ds = load_dataset(
    HF_DATASET,
    split=f"train[:{MAX_ROWS}]"
)

df = ds.to_pandas()

print(f"✅ Loaded {len(df)} transcripts")

required_cols = {
    "ticker",
    "company",
    "quarter",
    "earnings_year",
    "transcript",
}

missing = required_cols - set(df.columns)

if missing:
    raise ValueError(f"Missing required columns: {missing}")

df["company"] = df["company"].fillna(df["ticker"])

# =========================================================
# LOAD SPACY
# =========================================================

try:
    nlp = spacy.load("en_core_web_sm")

except OSError:

    print("📦 Downloading spaCy model...")

    import subprocess

    subprocess.run(
        ["python", "-m", "spacy", "download", "en_core_web_sm"],
        check=True
    )

    nlp = spacy.load("en_core_web_sm")

# =========================================================
# INITIALISE GRAPH
# =========================================================

G = nx.DiGraph()


def add_node(entity, node_type, **attrs):

    if not G.has_node(entity):

        G.add_node(
            entity,
            type=node_type,
            **attrs
        )

# =========================================================
# PROCESS TRANSCRIPTS
# =========================================================

print("🚀 Building knowledge graph...")

for idx, row in df.iterrows():

    ticker = row["ticker"]
    company = row["company"]
    transcript = row["transcript"]

    if not isinstance(transcript, str):
        continue

    transcript = transcript.strip()

    if len(transcript) < 100:
        continue

    # -----------------------------------------------------
    # COMPANY NODE
    # -----------------------------------------------------

    add_node(
        company,
        "Company",
        ticker=ticker
    )

    # -----------------------------------------------------
    # SECTOR NODE
    # -----------------------------------------------------

    sector = TICKER_TO_SECTOR.get(
        ticker,
        DEFAULT_SECTOR
    )

    add_node(
        sector,
        "Sector"
    )

    G.add_edge(
        company,
        sector,
        relation="in_sector"
    )

    # -----------------------------------------------------
    # NLP ENTITY EXTRACTION
    # -----------------------------------------------------

    try:

        # ---------------------------------------------
        # PRE-CLEAN TRANSCRIPT
        # ---------------------------------------------

        transcript = transcript.replace(
            "The Motley Fool",
            ""
        )

        transcript = re.sub(
            r"http\S+",
            "",
            transcript
        )

        transcript = re.sub(
            r"\s+",
            " ",
            transcript
        )

        # ---------------------------------------------
        # NLP
        # ---------------------------------------------

        doc = nlp(transcript[:10000])

        mentioned_orgs = set()

        for ent in doc.ents:

            # ONLY ORGANIZATIONS
            if ent.label_ != "ORG":
                continue

            org = ent.text.strip()

            # ---------------------------------------------
            # NORMALIZATION
            # ---------------------------------------------

            org = org.replace("the ", "")
            org = org.replace("The ", "")
            org = org.strip()

            org_clean = org.lower().strip()

            # ---------------------------------------------
            # ENTITY CLEANING
            # ---------------------------------------------

            if org_clean in BAD_TERMS:
                continue

            if len(org) < 4:
                continue

            if len(org) > 80:
                continue

            # remove short acronyms
            if org.isupper() and len(org) <= 5:
                continue

            # remove numbers
            if any(char.isdigit() for char in org):
                continue

            # remove garbage/html/json
            if any(x in org for x in [
                "{",
                "}",
                "@",
                ".com",
                "http",
                "www",
                '["'
            ]):
                continue

            # avoid self mentions
            if org.lower() in company.lower():
                continue

            # avoid duplicates
            if org == company:
                continue

            mentioned_orgs.add(org)

        # ---------------------------------------------
        # ADD COMPANY RELATIONS
        # ---------------------------------------------

        for org in mentioned_orgs:

            add_node(
                org,
                "Company",
                ticker=""
            )

            G.add_edge(
                company,
                org,
                relation="mentions_company"
            )

    except Exception as e:

        print(f"⚠️ spaCy failed at row {idx}: {e}")

    # -----------------------------------------------------
    # SUPPLY CHAIN SIGNALS
    # -----------------------------------------------------

    text_lower = transcript.lower()

    signals_found = set()

    for term in SUPPLY_CHAIN_TERMS:

        pattern = r"\b" + re.escape(term) + r"\b"

        if re.search(pattern, text_lower):

            signal_name = (
                f"Signal_{term.replace(' ', '_').title()}"
            )

            signals_found.add(signal_name)

    for signal in signals_found:

        add_node(
            signal,
            "Signal"
        )

        G.add_edge(
            company,
            signal,
            relation="mentions"
        )

        G.add_edge(
            signal,
            sector,
            relation="propagates_to"
        )

    # -----------------------------------------------------
    # LOGGING
    # -----------------------------------------------------

    if idx % 25 == 0:

        print(
            f"📄 Processed {idx}/{len(df)} transcripts | "
            f"Nodes={G.number_of_nodes()} | "
            f"Edges={G.number_of_edges()}"
        )

# =========================================================
# SUMMARY
# =========================================================

print("\n🎉 GRAPH COMPLETE")

print(f"🔹 Nodes: {G.number_of_nodes()}")
print(f"🔹 Edges: {G.number_of_edges()}")

# =========================================================
# SAVE GRAPH
# =========================================================

print("\n💾 Saving graph...")

with open(OUTPUT_GRAPH, "wb") as f:
    pickle.dump(G, f)

nx.write_gexf(
    G,
    OUTPUT_GEXF
)

# =========================================================
# EXPORT NODES
# =========================================================

nodes_df = pd.DataFrame(
    [
        (
            n,
            G.nodes[n].get("type", "Unknown")
        )
        for n in G.nodes()
    ],
    columns=[
        "node",
        "type"
    ],
)

nodes_df.to_csv(
    OUTPUT_NODES,
    index=False
)

# =========================================================
# EXPORT EDGES
# =========================================================

edges = []

for u, v, data in G.edges(data=True):

    edges.append(
        [
            u,
            v,
            data.get("relation", "unknown"),
        ]
    )

edges_df = pd.DataFrame(
    edges,
    columns=[
        "source",
        "target",
        "relation",
    ],
)

edges_df.to_csv(
    OUTPUT_EDGES,
    index=False
)

# =========================================================
# NODE TYPE DISTRIBUTION
# =========================================================

node_type_counts = Counter(
    nx.get_node_attributes(G, "type").values()
)

print("\n📊 Node type distribution:")

for ntype, count in node_type_counts.items():

    print(f"   {ntype}: {count}")

# =========================================================
# OUTPUT FILES
# =========================================================

print("\n✅ Files generated:")

print(f"   {OUTPUT_GRAPH}")
print(f"   {OUTPUT_GEXF}")
print(f"   {OUTPUT_NODES}")
print(f"   {OUTPUT_EDGES}")