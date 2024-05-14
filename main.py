import igraph as ig
import pandas as pd
import numpy as np
import networkx as nx
import pickle  # Import pickle to save the graph object

# Load the dataset
df = pd.read_csv('cs_simplified_linkedin_profiles.csv', converters={"education": eval, "experiences": eval})

# Create a new graph
g = ig.Graph(directed=False)

# Add vertices
g.add_vertices(df['public_identifier'].tolist())
g.vs['label'] = df['first_name'].tolist()

def add_edges_based_on_shared_attributes(df, attribute, subfield):
    df_exploded = df.explode(attribute)
    df_exploded.dropna(subset=[attribute], inplace=True)

    df_exploded['key'] = df_exploded[attribute].apply(lambda x: x.get(subfield) if isinstance(x, dict) else None)
    df_exploded = df_exploded.dropna(subset=['key'])

    for item, group in df_exploded.groupby('key'):
        ids = group['public_identifier'].tolist()
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                g.add_edges([(ids[i], ids[j])])
        print(f"Processed group '{item}' with {len(ids)} members based on {attribute}.")

# Community Detection - Louvain Method
louvain = g.community_multilevel()
g.vs['community'] = louvain.membership

# # Convert igraph to networkx
# G_nx = nx.Graph()
# G_nx.add_nodes_from((node.index, {"label": node["label"], "community": node["community"]}) for node in g.vs)
# G_nx.add_edges_from((edge.source, edge.target) for edge in g.es)
#
# # Save the networkx graph
# with open('network_graph.pkl', 'wb') as f:
#     pickle.dump(G_nx, f)
print("Number of Nodes:", g.vcount())
print("Number of Edges:", g.ecount())
print("Diameter:", g.diameter() if g.ecount() > 0 else "Not applicable - No edges")
print("Number of Connected Components:", len(g.connected_components()))

# Clustering Coefficients
clusteringCoefficients = g.transitivity_local_undirected()
high_clustering = np.argsort(clusteringCoefficients)[-5:]
print("5 nodes with the highest clustering coefficients:", high_clustering)

# Vertex Betweenness
vertexBetweenness = g.betweenness()
high_betweenness = np.argsort(vertexBetweenness)[-5:]
print("5 nodes with the highest vertex betweenness:", high_betweenness)

# Community Detection - Louvain Method
louvain = g.community_multilevel()
print("Number of communities (Louvain):", len(louvain))
print("Modularity (Louvain):", louvain.modularity)
ig.plot(louvain, "Louvain.png", mark_groups=True)

# Community Detection - Girvan-Newman
girvan_newman = g.community_edge_betweenness().as_clustering()
print("Number of communities (Girvan-Newman):", len(girvan_newman))
print("Modularity (Girvan-Newman):", girvan_newman.modularity)
ig.plot(girvan_newman, "Girvan_Newman.png", mark_groups=True)

# Community Detection - Random Walk
random_walk = g.community_walktrap().as_clustering()
print("Number of communities (Random Walk):", len(random_walk))
print("Modularity (Random Walk):", random_walk.modularity)
ig.plot(random_walk, "Random_Walk.png", mark_groups=True)

# Set visual styles for plots
visual_style = {
    "vertex_size": 50,
    "vertex_label": g.vs["name"],
    "bbox": (900, 900),
    "margin": 50
}

# Update plots with visual styles
ig.plot(louvain, "Louvain_with_style.png", **visual_style)
ig.plot(girvan_newman, "Girvan_Newman_with_style.png", **visual_style)
ig.plot(random_walk, "Random_Walk_with_style.png", **visual_style)
