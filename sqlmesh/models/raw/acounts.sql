MODEL (
  name main.raw_accounts,
  kind FULL,
  start '2025-02-20',
  cron '@daily',
  grain (id, created_at)
);


SELECT
    account_id,
    account_type,
    balance,
    currency,
    status,
    user_id,
    created_at
FROM main.accounts;
