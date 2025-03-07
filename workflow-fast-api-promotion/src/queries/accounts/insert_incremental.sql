INSERT INTO accounts (id, name, created_at, updated_at)
SELECT
    id,
    name,
    created_at,
    updated_at
FROM staging_accounts
WHERE created_at BETWEEN: start_time AND: end_time;
