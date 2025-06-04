import json
import pandas as pd
import os

FEEDBACK_LOG_PATH = 'feedback/feedback_log.jsonl'

def load_feedback_data(log_path=FEEDBACK_LOG_PATH):
    """Loads feedback data from the JSONL log file into a pandas DataFrame."""
    data = []
    if not os.path.exists(log_path):
        print(f"Feedback log file not found at {log_path}")
        return pd.DataFrame(data)
    
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON line in {log_path}: {line.strip()} - {e}")
    except Exception as e:
        print(f"Error reading feedback log file {log_path}: {e}")
        return pd.DataFrame([]) # Return empty DataFrame on read error

    df = pd.DataFrame(data)
    return df

def get_query_count(df):
    """Returns the total number of logged queries."""
    return len(df) if df is not None else 0

def get_feedback_counts(df):
    """Returns the counts for each type of feedback."""
    if df is None or df.empty:
        return {}
    # Ensure 'feedback_type' column exists before trying to value_counts
    if 'feedback_type' in df.columns:
        return df['feedback_type'].value_counts().to_dict()
    else:
        return {}

# Example usage (optional - for testing)
if __name__ == "__main__":
    feedback_df = load_feedback_data()
    
    total_queries = get_query_count(feedback_df)
    print(f"\nTotal Queries Logged: {total_queries}")
    
    feedback_counts = get_feedback_counts(feedback_df)
    print(f"Feedback Counts: {feedback_counts}") 