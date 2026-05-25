{{ config(materialized='table') }}

select
    coin_id,
    symbol,
    coin_name,
    current_price,
    market_cap,
    total_volume,
    price_change_percentage_24h,
    ingestion_time_utc,
    batch_id
from {{ ref('stg_crypto_market') }}