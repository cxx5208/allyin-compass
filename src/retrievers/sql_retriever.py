import duckdb
import pandas as pd

def get_sql_data(query, db_path='data/structured/structured_data.duckdb'):
    """Executes a SQL query against the DuckDB database and returns results as a pandas DataFrame."""
    try:
        con = duckdb.connect(database=db_path, read_only=True)
        df = con.execute(query).fetchdf()
        con.close()
        print(f"Successfully executed SQL query: {query}")
        return df
    except Exception as e:
        print(f"Error executing SQL query: {query}\n{e}")
        return None

# Example usage (optional - for testing)
if __name__ == "__main__":
    # Make sure you have run structured_loader.py first to create the database and table
    sample_query = "SELECT * FROM sample_data_1 LIMIT 5;"
    result_df = get_sql_data(sample_query)
    if result_df is not None:
        print("\nSample Query Result:")
        print(result_df) 