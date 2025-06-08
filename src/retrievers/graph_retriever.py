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

def add_node(graph, node_name):
    """Adds a new node to the graph."""
    if node_name not in graph:
        graph.add_node(node_name)
        return f"Node '{node_name}' added to the graph."
    return f"Node '{node_name}' already exists in the graph."

def add_edge(graph, node1, node2, relationship=None):
    """Adds an edge between two nodes, optionally with a relationship."""
    if node1 not in graph:
        graph.add_node(node1)
    if node2 not in graph:
        graph.add_node(node2)

    if relationship:
        graph.add_edge(node1, node2, relationship=relationship)
        return f"Edge added between '{node1}' and '{node2}' with relationship '{relationship}'."
    else:
        graph.add_edge(node1, node2)
        return f"Edge added between '{node1}' and '{node2}'."

def delete_node(graph, node_name):
    """Deletes a node and all its incident edges from the graph."""
    if node_name in graph:
        graph.remove_node(node_name)
        return f"Node '{node_name}' and its associated edges deleted from the graph."
    return f"Node '{node_name}' not found in the graph."

def delete_edge(graph, node1, node2):
    """Deletes an edge between two nodes."""
    if graph.has_edge(node1, node2):
        graph.remove_edge(node1, node2)
        return f"Edge between '{node1}' and '{node2}' deleted from the graph."
    return f"Edge between '{node1}' and '{node2}' not found in the graph."

def find_paths(graph, source, target):
    """Finds all simple paths between a source and target node."""
    if source not in graph:
        return f"Source node '{source}' not found in graph."
    if target not in graph:
        return f"Target node '{target}' not found in graph."

    paths = list(nx.all_simple_paths(graph, source=source, target=target))
    if paths:
        formatted_paths = []
        for path in paths:
            formatted_paths.append(" -> ".join(path))
        return f"Paths from '{source}' to '{target}':\n" + "\n".join(formatted_paths)
    return f"No paths found from '{source}' to '{target}'."

def get_all_nodes(graph):
    """Returns a list of all nodes in the graph."""
    nodes = list(graph.nodes())
    if nodes:
        return f"All nodes in the graph: {nodes}"
    return "The graph contains no nodes."

def get_all_edges(graph):
    """Returns a list of all edges in the graph, with relationships if present."""
    edges = []
    for u, v, data in graph.edges(data=True):
        if 'relationship' in data:
            edges.append(f"('{u}', '{v}', relationship='{data['relationship']}')")
        else:
            edges.append(f"('{u}', '{v}')")
    if edges:
        return f"All edges in the graph: {edges}"
    return "The graph contains no edges."

def get_graph_data(query, graph):
    """Basic graph retrieval function (can be expanded)."""
    results = []
    query_lower = query.lower()

    if query_lower.startswith("neighbors of"):
        node_name = query.replace("neighbors of ", "").strip()
        if node_name in graph:
            neighbors = list(graph.neighbors(node_name))
            results.append(f"Neighbors of {node_name}: {neighbors}")
        else:
            results.append(f"Node '{node_name}' not found in graph.")
    elif query_lower.startswith("add node"):
        node_name = query.replace("add node ", "").strip()
        results.append(add_node(graph, node_name))
    elif query_lower.startswith("add edge"):
        parts = query.replace("add edge ", "").strip().split(" to ")
        if len(parts) == 2:
            node1 = parts[0].strip()
            node2_and_rel = parts[1].strip()
            if "(" in node2_and_rel and ")" in node2_and_rel:
                node2_parts = node2_and_rel.split(" (")
                node2 = node2_parts[0].strip()
                relationship = node2_parts[1].replace(")", "").strip()
                results.append(add_edge(graph, node1, node2, relationship))
            else:
                node2 = node2_and_rel.strip()
                results.append(add_edge(graph, node1, node2))
        else:
            results.append("Invalid 'add edge' query format. Use 'add edge Node1 to Node2 (relationship)' or 'add edge Node1 to Node2'.")
    elif query_lower.startswith("delete node"):
        node_name = query.replace("delete node ", "").strip()
        results.append(delete_node(graph, node_name))
    elif query_lower.startswith("delete edge"):
        parts = query.replace("delete edge ", "").strip().split(" to ")
        if len(parts) == 2:
            node1 = parts[0].strip()
            node2 = parts[1].strip()
            results.append(delete_edge(graph, node1, node2))
        else:
            results.append("Invalid 'delete edge' query format. Use 'delete edge Node1 to Node2'.")
    elif query_lower.startswith("paths from"):
        parts = query.replace("paths from ", "").strip().split(" to ")
        if len(parts) == 2:
            source = parts[0].strip()
            target = parts[1].strip()
            results.append(find_paths(graph, source, target))
        else:
            results.append("Invalid 'paths from' query format. Use 'paths from SourceNode to TargetNode'.")
    elif query_lower == "all nodes":
        results.append(get_all_nodes(graph))
    elif query_lower == "all edges":
        results.append(get_all_edges(graph))
    else:
        results.append(f"Node '{query}' not found in graph. Try 'neighbors of [node name]', 'add node [node name]', 'add edge [node1] to [node2] (relationship)', 'delete node [node name]', 'delete edge [node1] to [node2]', 'paths from [source] to [target]', 'all nodes', or 'all edges'.")
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

    # Test new functionalities
    print("\n--- Testing New Functionalities ---")
    print(get_graph_data("add node City Z", sample_graph))
    print(get_graph_data("add edge Person A to City Z (lives_in)", sample_graph))
    print(get_graph_data("add edge Company X to City Z", sample_graph))
    print(get_graph_data("all nodes", sample_graph))
    print(get_graph_data("all edges", sample_graph))
    print(get_graph_data("paths from Person A to Project Beta", sample_graph))
    print(get_graph_data("delete node Company X", sample_graph))
    print(get_graph_data("all nodes", sample_graph))
    print(get_graph_data("all edges", sample_graph))
    print(get_graph_data("delete edge Person B to Project Beta", sample_graph))
    print(get_graph_data("all edges", sample_graph)) 