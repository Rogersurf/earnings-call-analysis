from datasets import load_dataset
import networkx as nx

ds = load_dataset(
    "Rogersurf/earnings-call-transcripts",
    split="train[:200]"
)

G = nx.Graph()

for row in ds:
    company = row["company"]
    ticker = row["ticker"]

    if company and ticker:
        G.add_node(company)

for i in range(len(ds) - 1):
    c1 = ds[i]["company"]
    c2 = ds[i + 1]["company"]

    if c1 != c2:
        G.add_edge(c1, c2)

print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())