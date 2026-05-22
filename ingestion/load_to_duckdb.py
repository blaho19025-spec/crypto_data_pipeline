from pathlib import Path
import duckdb


RAW_DATA_DIR = Path("data/raw")
WAREHOUSE_PATH = Path("warehouse/crypto.duckdb")


def get_latest_parquet_file():
    parquet_files = list(RAW_DATA_DIR.glob("crypto_market_*.parquet"))

    if not parquet_files:
        raise FileNotFoundError("No parquet files found in data/raw")

    return max(parquet_files, key=lambda file: file.stat().st_mtime)


def load_latest_file_to_duckdb():
    WAREHOUSE_PATH.parent.mkdir(parents=True, exist_ok=True)

    latest_file = get_latest_parquet_file()

    con = duckdb.connect(str(WAREHOUSE_PATH))

    con.execute("""
        CREATE SCHEMA IF NOT EXISTS raw;
    """)

    con.execute(f"""
        CREATE OR REPLACE TABLE raw.crypto_market AS
        SELECT *
        FROM read_parquet('{latest_file}');
    """)

    row_count = con.execute("""
        SELECT COUNT(*) 
        FROM raw.crypto_market;
    """).fetchone()[0]

    con.close()

    print(f"Loaded file: {latest_file}")
    print(f"Rows loaded into raw.crypto_market: {row_count}")


if __name__ == "__main__":
    load_latest_file_to_duckdb()