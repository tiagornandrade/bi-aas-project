INSERT INTO accounts (id, name, created_at, updated_at)
SELECT
    id,
    name,
    created_at,
    updated_at
FROM staging_accounts
WHERE updated_at BETWEEN: start_time AND: end_time
ON CONFLICT (id) DO UPDATE
SET name = excluded.name,
updated_at = excluded.updated_at;
