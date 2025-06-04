import networkx as nx

def create_sample_graph():
    """Creates a simple sample graph using NetworkX."""
    G = nx.Graph()
    G.add_edges_from([
        ('Person A', 'Company X'),
        ('Person A', 'Project Alpha'),
        ('Company X', 'Project Alpha'),
        ('Person B', 'Company Y'),
        ('Person B', 'Project Beta'),
        ('Company Y', 'Project Beta'),
        ('Project Alpha', 'Project Beta', {'relationship': 'related'})
    ])
    return G

def get_graph_data(query, graph):
    """Basic graph retrieval function (can be expanded)."""
    results = []
    # This is a very basic example. Real graph queries would be more complex.
    # For demonstration, let's find neighbors of a queried node.
    if query in graph:
        neighbors = list(graph.neighbors(query))
        results.append(f"Neighbors of {query}: {neighbors}")
    else:
        results.append(f"Node '{query}' not found in graph.")
    return results

# Example usage (optional - for testing)
if __name__ == "__main__":
    sample_graph = create_sample_graph()

    # Example queries
    query1 = "Person A"
    query2 = "Company Y"
    query3 = "Project Gamma"

    print(f"\nGraph Retrieval Results for '{query1}':")
    print(get_graph_data(query1, sample_graph))

    print(f"\nGraph Retrieval Results for '{query2}':")
    print(get_graph_data(query2, sample_graph))

    print(f"\nGraph Retrieval Results for '{query3}':")
    print(get_graph_data(query3, sample_graph)) 