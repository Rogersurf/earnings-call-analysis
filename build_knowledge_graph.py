#!/usr/bin/env python3
"""
build_knowledge_graph.py
Constructs a corporate knowledge graph (NetworkX) from earnings call transcripts stored in Parquet format.
Nodes: Company, Sector, Signal
Edges: mentions, in_sector, propagates_to, mentions_company
"""

import re
import pandas as pd
import networkx as nx
import spacy
from collections import Counter
from pathlib import Path

# ------------------------------
# CONFIGURATION
# ------------------------------
PARQUET_PATH = "data/database/transcripts_clean.parquet"
# If you have the dataset on Hugging Face, uncomment the next lines:
# from datasets import load_dataset
# df = load_dataset("your-username/earnings-calls", split="train").to_pandas()

# Supply chain keywords (customise as needed)
SUPPLY_CHAIN_TERMS = {
    "production", "capacity", "inventory", "supply", "stock",
    "infrastructure", "manufacturing", "orders", "capex",
    "backlog", "supply chain", "logistics", "component shortage",
    "demand", "pricing pressure", "margin pressure", "cloud capacity",
    "server infrastructure", "data center", "semiconductor", "wafer"
}

# Sector mapping (extend based on your tickers)
TICKER_TO_SECTOR = {
    "NVDA": "Semiconductors", "AMD": "Semiconductors", "INTC": "Semiconductors",
    "TSM": "Semiconductors", "MU": "Semiconductors", "QCOM": "Semiconductors",
    "MSFT": "Cloud & Software", "AMZN": "Cloud & E-commerce", "GOOGL": "Cloud & Advertising",
    "META": "Social Media", "DELL": "Hardware", "HPQ": "Hardware", "AAPL": "Consumer Electronics",
    "TSLA": "Automotive", "GM": "Automotive", "F": "Automotive", "UBER": "Mobility"
}
DEFAULT_SECTOR = "Other"

# ------------------------------
# LOAD DATA
# ------------------------------
if not Path(PARQUET_PATH).exists():
    raise FileNotFoundError(f"Parquet file not found at {PARQUET_PATH}")

df = pd.read_parquet(PARQUET_PATH)
print(f"✅ Loaded {len(df)} transcripts from {PARQUET_PATH}")

# Ensure required columns exist
required_cols = {"ticker", "company", "quarter", "earnings_year", "transcript"}
if not required_cols.issubset(df.columns):
    raise ValueError(f"Parquet must contain columns: {required_cols}. Found: {df.columns.tolist()}")

# Fill NaN companies
df["company"] = df["company"].fillna(df["ticker"])

# ------------------------------
# LOAD SPACY MODEL
# ------------------------------
try:
    nlp = spacy.load("en_core_web_lg")
except OSError:
    print("⚠️ Model 'en_core_web_lg' not found. Downloading...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_lg"])
    nlp = spacy.load("en_core_web_lg")

# ------------------------------
# INITIALISE GRAPH
# ------------------------------
G = nx.MultiDiGraph()  # directed multigraph

def add_node(entity, node_type, **attrs):
    if not G.has_node(entity):
        G.add_node(entity, type=node_type, **attrs)

# ------------------------------
# PROCESS EACH TRANSCRIPT
# ------------------------------
for idx, row in df.iterrows():
    ticker = row["ticker"]
    company = row["company"]
    transcript = row["transcript"]
    if not isinstance(transcript, str) or len(transcript.strip()) < 100:
        continue

    # ---- Company node ----
    add_node(company, "Company", ticker=ticker)

    # ---- Sector node ----
    sector = TICKER_TO_SECTOR.get(ticker, DEFAULT_SECTOR)
    add_node(sector, "Sector")
    G.add_edge(company, sector, relation="in_sector")

    # ---- Extract mentioned companies using spaCy (limit to first 500k chars for speed) ----
    doc = nlp(transcript[:500000])
    mentioned_orgs = set()
    for ent in doc.ents:
        if ent.label_ == "ORG" and len(ent.text) > 2:
            # avoid self‑mention and very short names
            if ent.text.lower() not in company.lower() and ent.text not in company:
                mentioned_orgs.add(ent.text)

    for other_org in mentioned_orgs:
        add_node(other_org, "Company", ticker=None)
        G.add_edge(company, other_org, relation="mentions_company")

    # ---- Extract supply chain signals (dictionary + regex) ----
    text_lower = transcript.lower()
    signals_found = set()
    for term in SUPPLY_CHAIN_TERMS:
        # word boundary regex to avoid partial matches
        if re.search(r'\b' + re.escape(term) + r'\b', text_lower):
            signal_name = f"Signal_{term.replace(' ', '_').title()}"
            signals_found.add(signal_name)

    for signal in signals_found:
        add_node(signal, "Signal")
        G.add_edge(company, signal, relation="mentions")
        # Propagate signal to sector (simplistic)
        G.add_edge(signal, sector, relation="propagates_to")

    if idx % 500 == 0:
        print(f"📄 Processed {idx} transcripts...")

print(f"\n🎉 Graph built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges.")

# ------------------------------
# SAVE OUTPUTS
# ------------------------------
output_dir = Path("data")
output_dir.mkdir(exist_ok=True)

nx.write_gpickle(G, output_dir / "knowledge_graph.gpickle")
print(f"💾 Graph saved as {output_dir / 'knowledge_graph.gpickle'}")

# Export nodes and edges as CSV for easy inspection
nodes_df = pd.DataFrame([(n, G.nodes[n].get("type", "Unknown")) for n in G.nodes()],
                        columns=["node", "type"])
nodes_df.to_csv(output_dir / "graph_nodes.csv", index=False)

edges = []
for u, v, data in G.edges(data=True):
    edges.append([u, v, data.get("relation", "unknown")])
edges_df = pd.DataFrame(edges, columns=["source", "target", "relation"])
edges_df.to_csv(output_dir / "graph_edges.csv", index=False)

print(f"📁 Node list: {output_dir / 'graph_nodes.csv'}")
print(f"📁 Edge list: {output_dir / 'graph_edges.csv'}")

# Optional: show node type summary
node_type_counts = Counter(nx.get_node_attributes(G, "type").values())
print("\n📊 Node type distribution:")
for ntype, count in node_type_counts.items():
    print(f"   {ntype}: {count}")