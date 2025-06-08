import streamlit as st
import sys
import os
import torch

# Patch PyTorch path handling
torch.classes.__path__ = []

os.environ["STREAMLIT_SERVER_ENABLE_FILE_WATCHER"] = "false" # Disables problematic inspection

# Add necessary directories to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'feedback')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dashboards')))

# Import the agent, feedback logger, and metrics functions
from src.agents.multi_tool_agent import run_agent
from feedback.logger import log_feedback
from dashboards.metrics import load_feedback_data, get_query_count, get_feedback_counts

st.set_page_config(page_title="AllyIn Compass", layout="wide")

# Custom CSS for basic styling (e.g., smaller text for citations)
st.markdown("""
<style>
.small-text {
    font-size: 0.9em;
    color: #666;
}
</style>
""", unsafe_allow_html=True)

st.title("🧭 AllyIn Compass")
st.markdown("A multi-modal enterprise AI agent (Open Source Prototype)")

# Sidebar
st.sidebar.header("Dashboard Metrics")

# Load feedback data and calculate metrics
feedback_df = load_feedback_data()
total_queries = get_query_count(feedback_df)
feedback_counts = get_feedback_counts(feedback_df)

# Display metrics in the sidebar
st.sidebar.write(f"Total Queries: {total_queries}")
st.sidebar.write("Feedback Counts:")
if feedback_counts:
    for feedback_type, count in feedback_counts.items():
        st.sidebar.write(f"- {feedback_type.replace('_', ' ').title()}: {count}")
else:
    st.sidebar.write("No feedback yet.")

st.sidebar.markdown("---")
st.sidebar.header("Filters (Coming Soon)")
# Add filter options here later

# Main content area
st.header("Ask your question:")

# Input fields
query = st.text_input("Enter your query:", "What is the value?") # Example query
domain = st.selectbox("Select Domain (Not implemented yet):", ['Structured Data', 'Unstructured Data', 'Knowledge Graph', 'All'])

# Use Streamlit session state to store the last query and response
if 'last_query' not in st.session_state:
    st.session_state.last_query = None
if 'last_response' not in st.session_state:
    st.session_state.last_response = None
if 'last_citations' not in st.session_state:
    st.session_state.last_citations = []

# Run Agent button
if st.button("Get Answer"):
    if query:
        st.info(f"Running agent for query: '{query}' (Domain: {domain})")

        # Reset feedback status for a new query
        st.session_state.feedback_submitted = False

        # Run the agent with the query
        # NOTE: The current simple agent doesn't use the domain input.
        # Modify the agent logic in src/agents/multi_tool_agent.py to use domain.
        # Also, the current multi_tool_agent doesn't return citations separately.
        # You would need to modify multi_tool_agent to return citations from the RAG tool.
        agent_response = run_agent(query)
        citations = [] # Placeholder - need to get citations from agent response if using RAG

        st.subheader("Agent Response:")
        # Simple attempt at highlighting or color-coding using markdown
        # This would need more sophisticated logic based on agent output structure
        if "Error" in agent_response:
            st.error(agent_response)
        elif "Success" in agent_response or "Loaded" in agent_response or "Neighbors" in agent_response or "search results" in agent_response.lower() or "Agent chose" in agent_response:
             # Check for indicators of successful retrieval/action
             st.success(agent_response)
        else:
            st.write(agent_response)

        # Store the last query, response, and citations in session state
        st.session_state.last_query = query
        st.session_state.last_response = agent_response
        st.session_state.last_citations = citations # Store citations if available

    else:
        st.warning("Please enter a query.")

# Feedback buttons (Day 8 deliverable)
if st.session_state.last_query and st.session_state.last_response:
    st.subheader("Provide Feedback:")
    col1, col2 = st.columns(2)

    # Initialize feedback status in session state
    if 'feedback_submitted' not in st.session_state:
        st.session_state.feedback_submitted = False

    with col1:
        if st.button("👍 Thumbs Up", disabled=st.session_state.feedback_submitted):
            log_feedback(st.session_state.last_query, st.session_state.last_response, 'thumbs_up')
            st.success("Feedback logged: Thumbs Up!")
            st.session_state.feedback_submitted = True # Mark feedback as submitted
            st.rerun() # Rerun to disable the button
    with col2:
        if st.button("👎 Thumbs Down", disabled=st.session_state.feedback_submitted):
            log_feedback(st.session_state.last_query, st.session_state.last_response, 'thumbs_down')
            st.success("Feedback logged: Thumbs Down!")
            st.session_state.feedback_submitted = True # Mark feedback as submitted
            st.rerun() # Rerun to disable the button

# Display citations if available (Day 13 deliverable)
if st.session_state.last_citations:
     st.subheader("Sources:")
     for citation in st.session_state.last_citations:
         st.markdown(f'<p class="small-text">{citation}</p>', unsafe_allow_html=True)


# Add some explanatory text or instructions
st.markdown("""
**How to use:**
Enter your query above. The agent will attempt to use the available data sources (Structured, Unstructured, Graph) to answer.

*   Try queries like: `sql: SELECT * FROM sample_data_1;`, `vector search: tell me about the sample email`
*   For graph queries, try: `graph: neighbors of Person A`, `graph: add node City Z`, `graph: paths from Person A to Project Beta`, `graph: all nodes`, `graph: all edges`
""") 