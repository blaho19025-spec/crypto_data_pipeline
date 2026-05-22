import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests


API_URL = "https://api.coingecko.com/api/v3/coins/markets"

PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 100,
    "page": 1,
    "sparkline": "false",
}


def fetch_crypto_market_data():
    response = requests.get(API_URL, params=PARAMS, timeout=30)
    response.raise_for_status()
    return response.json()


def save_raw_data(data):
    ingestion_time = datetime.now(timezone.utc)
    batch_id = ingestion_time.strftime("%Y%m%d_%H%M%S")

    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)

    json_path = raw_dir / f"crypto_market_{batch_id}.json"
    parquet_path = raw_dir / f"crypto_market_{batch_id}.parquet"

    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)

    df = pd.DataFrame(data)
    df["ingestion_time_utc"] = ingestion_time.isoformat()
    df["batch_id"] = batch_id

    df.to_parquet(parquet_path, index=False)

    print(f"Saved JSON: {json_path}")
    print(f"Saved Parquet: {parquet_path}")
    print(f"Rows pulled: {len(df)}")


if __name__ == "__main__":
    data = fetch_crypto_market_data()
    save_raw_data(data)
    