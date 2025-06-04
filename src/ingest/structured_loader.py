import pandas as pd
import duckdb
import glob
import os

def load_structured_data(data_dir='data/structured', db_path='data/structured/structured_data.duckdb'):
    """Loads CSV files from a directory into a DuckDB database."""
    # Create data directory if it doesn't exist
    os.makedirs(data_dir, exist_ok=True)

    # Connect to DuckDB
    con = duckdb.connect(database=db_path, read_only=False)

    # Get list of CSV files
    csv_files = glob.glob(os.path.join(data_dir, '*.csv'))

    if not csv_files:
        print(f"No CSV files found in {data_dir}")
        return

    for csv_file in csv_files:
        table_name = os.path.splitext(os.path.basename(csv_file))[0]
        try:
            # Read CSV into pandas DataFrame
            df = pd.read_csv(csv_file)
            # Load DataFrame into DuckDB table
            con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df")
            print(f"Loaded {csv_file} into table {table_name}")
        except Exception as e:
            print(f"Error loading {csv_file}: {e}")

    # Close connection
    con.close()

if __name__ == "__main__":
    load_structured_data() 