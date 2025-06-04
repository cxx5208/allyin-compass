import sys
import os

# Add the parent directory of src to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.retrievers import sql_retriever
from src.retrievers import vector_retriever
from src.retrievers import graph_retriever

import datetime

# Basic logging function
def log_tool_usage(tool_name, query, result):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Tool: {tool_name}, Query: '{query}', Result: {result}\n"
    print(log_entry) # For demonstration, print to console
    # In a real application, you might write to a log file
    # with open('tool_usage.log', 'a') as f:
    #     f.write(log_entry)

# Simple agent logic to choose a tool
def run_agent(query):
    """Runs the agent to process a query using available tools."""
    chosen_tool = None
    result = ""

    # Simple keyword-based tool selection
    query_lower = query.lower()

    if any(keyword in query_lower for keyword in ['sql', 'database', 'table']):
        chosen_tool = 'sql_retriever'
        print(f"Agent chose {chosen_tool}")
        # Assuming the query for SQL retriever is the SQL query itself
        sql_query = query.replace('sql:', '').strip() # Simple way to extract query after a prefix
        if not sql_query:
             result = "Please provide a SQL query after 'sql:'."
             log_tool_usage(chosen_tool, query, result)
             return result
        sql_result_df = sql_retriever.get_sql_data(sql_query)
        if sql_result_df is not None:
            result = sql_result_df.to_string()
        else:
            result = "Could not retrieve data using SQL."

    elif any(keyword in query_lower for keyword in ['document', 'text', 'search', 'vector']):
        chosen_tool = 'vector_retriever'
        print(f"Agent chose {chosen_tool}")
        # Assuming the query for vector retriever is the search query itself
        vector_query = query.replace('vector search:', '').strip()
        if not vector_query:
             result = "Please provide a search query after 'vector search:'."
             log_tool_usage(chosen_tool, query, result)
             return result
        vector_results = vector_retriever.get_vector_retriever(vector_query)
        if vector_results:
            # Format vector search results for output
            formatted_output = []
            for res in vector_results:
                formatted_output.append(f"  Distance: {res.get('distance', 'N/A'):.4f}, Filename: {res.get('metadata', {}).get('filename', 'N/A')}, Snippet: {res.get('metadata', {}).get('text_snippet', 'N/A')}")
            result = "Vector Search Results:\n" + "\n".join(formatted_output)
        else:
            result = "No vector search results found."

    elif any(keyword in query_lower for keyword in ['graph', 'relationship', 'node', 'neighbors']):
        chosen_tool = 'graph_retriever'
        print(f"Agent chose {chosen_tool}")
        # Assuming the query for graph retriever is the node name or a command
        graph_query = query.replace('graph:', '').strip()
        if not graph_query:
             result = "Please provide a graph query (e.g., node name) after 'graph:'."
             log_tool_usage(chosen_tool, query, result)
             return result
        # For this simple example, we'll just pass the query string to the graph retriever
        # In a real agent, you might parse the query to call specific graph functions
        sample_graph = graph_retriever.create_sample_graph() # Re-create sample graph for simplicity
        graph_results = graph_retriever.get_graph_data(graph_query, sample_graph)
        result = "\n".join(graph_results)

    else:
        result = "Could not determine the appropriate tool for the query. Please include keywords like 'sql:', 'vector search:', or 'graph:'."
        chosen_tool = 'None'

    # Log tool usage if a tool was chosen
    if chosen_tool and chosen_tool != 'None':
         log_tool_usage(chosen_tool, query, result)

    return result

if __name__ == "__main__":
    print("Simple Multi-Tool Agent (Type 'quit' to exit)")
    while True:
        user_query = input("Enter your query: ")
        if user_query.lower() == 'quit':
            break
        agent_response = run_agent(user_query)
        print("Agent Response:")
        print(agent_response)
        print("\n" + "-"*20 + "\n") 