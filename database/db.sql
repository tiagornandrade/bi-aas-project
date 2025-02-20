
-- Provide privilege to slave user from slave database
-- Should be executed from master database since it has super admin user (postgres)
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO repl_user;
ALTER USER repl_user WITH SUPERUSER;

CREATE PUBLICATION airbyte_publication FOR ALL TABLES;

SHOW wal_level;
SHOW max_replication_slots;
SHOW max_wal_senders;
SELECT * FROM pg_replication_slots;


CREATE USER airbyte PASSWORD 'airbyte';

CREATE SCHEMA raw;
CREATE SCHEMA bronze;
CREATE SCHEMA silver;
CREATE SCHEMA gold;


GRANT USAGE ON SCHEMA public TO airbyte;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO airbyte;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO airbyte;


CREATE SCHEMA IF NOT EXISTS audit_log;

CREATE TABLE audit_log.changes (
    id SERIAL PRIMARY KEY,
    table_name TEXT,
    change_type TEXT,
    record JSONB,
    captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
