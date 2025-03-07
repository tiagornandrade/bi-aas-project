INSERT INTO bronze.accounts_deleted (
    event_uuid,
    event_timestamp,
    processed_at,
    balance,
    user_uuid,
    currency,
    account_uuid,
    created_at,
    account_type
)
SELECT
    event_uuid::UUID,
    event_timestamp,
    ingested_at AS processed_at,
    (payload ->> 'balance')::NUMERIC AS balance,
    (payload ->> 'user_id')::UUID AS user_uuid,
    payload ->> 'currency' AS currency,
    (payload ->> 'account_id')::UUID AS account_uuid,
    (payload ->> 'created_at')::TIMESTAMP AS created_at,
    payload ->> 'account_type' AS account_type
FROM raw.accounts
WHERE event_type = 'delete'
    AND ingested_at > (SELECT COALESCE(MAX(processed_at::date), '1900-01-01') FROM bronze.accounts_deleted);
