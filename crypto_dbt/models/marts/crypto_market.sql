{{ config(
    materialized='incremental',
    unique_key=['coin_id', 'batch_id']
) }}

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

{% if is_incremental() %}
where batch_id not in (
    select distinct batch_id
    from {{ this }}
)
{% endif %}