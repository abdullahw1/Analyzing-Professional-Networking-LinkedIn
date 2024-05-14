import igraph as ig
import pandas as pd

# Load the dataset
df = pd.read_csv('cs_simplified_linkedin_profiles.csv', converters={"education": eval, "experiences": eval})

# Create a new graph
g = ig.Graph(directed=False)

# Add vertices
g.add_vertices(df['public_identifier'].tolist())
g.vs['label'] = df['first_name'].tolist()

# Function to add edges based on shared attributes
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

# Example usage of the function
add_edges_based_on_shared_attributes(df, 'education', 'school')
add_edges_based_on_shared_attributes(df, 'experiences', 'company')

# Degree Centrality
degree = g.degree()
print("Degree Centrality:", degree)

# Betweenness Centrality
betweenness = g.betweenness()
print("Betweenness Centrality:", betweenness)

# Closeness Centrality
closeness = g.closeness()
print("Closeness Centrality:", closeness)

# Eigenvector Centrality
eigenvector = g.eigenvector_centrality()
print("Eigenvector Centrality:", eigenvector)

# Print top 5 nodes for each centrality measure
print("Top 5 nodes by Degree Centrality:", sorted(zip(g.vs['label'], degree), key=lambda x: x[1], reverse=True)[:5])
print("Top 5 nodes by Betweenness Centrality:", sorted(zip(g.vs['label'], betweenness), key=lambda x: x[1], reverse=True)[:5])
print("Top 5 nodes by Closeness Centrality:", sorted(zip(g.vs['label'], closeness), key=lambda x: x[1], reverse=True)[:5])
print("Top 5 nodes by Eigenvector Centrality:", sorted(zip(g.vs['label'], eigenvector), key=lambda x: x[1], reverse=True)[:5])

#
#
#
# import pandas as pd
# import networkx as nx
# import matplotlib.pyplot as plt
# import seaborn as sns
#
# # Load the dataset
# df = pd.read_csv('cs_simplified_linkedin_profiles.csv', converters={"education": eval, "experiences": eval})
#
# # Create a new graph
# G = nx.Graph()
#
# # Add vertices and edges based on shared attributes
# for index, row in df.iterrows():
#     G.add_node(row['first_name'], label=row['first_name'])
#     if 'education' in row:
#         for edu in row['education']:
#             for other_index, other_row in df.iterrows():
#                 if other_index != index and 'education' in other_row:
#                     for other_edu in other_row['education']:
#                         if edu['school'] == other_edu['school']:
#                             G.add_edge(row['first_name'], other_row['first_name'])
#     if 'experiences' in row:
#         for exp in row['experiences']:
#             for other_index, other_row in df.iterrows():
#                 if other_index != index and 'experiences' in other_row:
#                     for other_exp in other_row['experiences']:
#                         if exp['company'] == other_exp['company']:
#                             G.add_edge(row['first_name'], other_row['first_name'])
#
# # Calculating centrality measures
# degree_centrality = nx.degree_centrality(G)
# betweenness_centrality = nx.betweenness_centrality(G)
# closeness_centrality = nx.closeness_centrality(G)
# eigenvector_centrality = nx.eigenvector_centrality(G)
#
# # Convert centrality measures to DataFrame for easier plotting
# centrality_df = pd.DataFrame({
#     'Node': list(degree_centrality.keys()),
#     'Degree': list(degree_centrality.values()),
#     'Betweenness': list(betweenness_centrality.values()),
#     'Closeness': list(closeness_centrality.values()),
#     'Eigenvector': list(eigenvector_centrality.values())
# })
#
# # Plotting
# plt.figure(figsize=(12, 10))
# plt.subplot(221)
# sns.barplot(x='Node', y='Degree', data=centrality_df.sort_values(by='Degree', ascending=False).head(10))
# plt.title('Top 10 Nodes by Degree Centrality')
# plt.xticks(rotation=45)
#
# plt.subplot(222)
# sns.barplot(x='Node', y='Betweenness', data=centrality_df.sort_values(by='Betweenness', ascending=False).head(10))
# plt.title('Top 10 Nodes by Betweenness Centrality')
# plt.xticks(rotation=45)
#
# plt.subplot(223)
# sns.barplot(x='Node', y='Closeness', data=centrality_df.sort_values(by='Closeness', ascending=False).head(10))
# plt.title('Top 10 Nodes by Closeness Centrality')
# plt.xticks(rotation=45)
#
# plt.subplot(224)
# sns.barplot(x='Node', y='Eigenvector', data=centrality_df.sort_values(by='Eigenvector', ascending=False).head(10))
# plt.title('Top 10 Nodes by Eigenvector Centrality')
# plt.xticks(rotation=45)
#
# plt.tight_layout()
# plt.show()
