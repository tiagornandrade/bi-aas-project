MODEL (
    name bronze.accounts_inserted,
    kind INCREMENTAL_BY_TIME_RANGE(
        time_column event_timestamp
    ),
    partitioned_by (event_timestamp)
);


WITH extracted_data AS (
    SELECT
        event_uuid,
        event_type,
        event_timestamp,
        ingested_at,
        table_name,
        CAST(payload::jsonb->>'id' AS TEXT) AS account_id,
        CAST(payload::jsonb->>'status' AS TEXT) AS status,
        CAST(
            regexp_replace(payload::jsonb->>'balance', '[^0-9.]', '', 'g')
            AS NUMERIC
        ) AS balance,
        CAST(payload::jsonb->>'currency' AS TEXT) AS currency,
        CAST(payload::jsonb->>'user_id' AS TEXT) AS user_id,
        CAST(payload::jsonb->>'created_at' AS TIMESTAMP) AS created_at,
        CAST(payload::jsonb->>'account_type' AS TEXT) AS account_type
    FROM raw.accounts
    WHERE event_type = 'INSERT'
)

SELECT * FROM extracted_data;
