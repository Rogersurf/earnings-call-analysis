import pickle
import networkx as nx

with open("data/knowledge_graph.gpickle", "rb") as f:
    G = pickle.load(f)

print(G)

print("\nNodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())

print("\nSample nodes:")
for i, node in enumerate(G.nodes(data=True)):
    print(node)

    if i >= 10:
        break

print("\nSample edges:")
for i, edge in enumerate(G.edges(data=True)):
    print(edge)

    if i >= 10:
        break