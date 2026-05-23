select
    id as coin_id,
    symbol,
    name as coin_name,
    current_price,
    market_cap,
    total_volume,
    price_change_percentage_24h,
    ingestion_time_utc,
    batch_id
from {{ source('raw', 'crypto_market') }}