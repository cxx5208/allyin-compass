import json
import os
import datetime

FEEDBACK_LOG_PATH = 'feedback/feedback_log.jsonl'

def log_feedback(query, response, feedback_type):
    """Logs user feedback to a JSONL file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    feedback_entry = {
        'timestamp': timestamp,
        'query': query,
        'response': response,
        'feedback_type': feedback_type # e.g., 'thumbs_up', 'thumbs_down'
    }

    # Ensure the feedback directory exists
    os.makedirs(os.path.dirname(FEEDBACK_LOG_PATH), exist_ok=True)

    try:
        with open(FEEDBACK_LOG_PATH, 'a') as f:
            json.dump(feedback_entry, f)
            f.write('\n')
        print(f"Logged feedback: {feedback_type} for query '{query}'")
    except Exception as e:
        print(f"Error logging feedback: {e}")

# Example usage (optional - for testing)
if __name__ == "__main__":
    log_feedback("Test query", "Test response", "thumbs_up")
    log_feedback("Another query", "Another response", "thumbs_down") 