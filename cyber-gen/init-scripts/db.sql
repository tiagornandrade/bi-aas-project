-- Criando usuário de replicação sem permissões desnecessárias
CREATE ROLE repl_user WITH REPLICATION LOGIN PASSWORD 'strongpassword';
GRANT USAGE ON SCHEMA public TO repl_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO repl_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO repl_user;

-- Configuração da replicação lógica
ALTER SYSTEM SET wal_level = 'logical';
ALTER SYSTEM SET max_replication_slots = 10;
ALTER SYSTEM SET max_wal_senders = 10;
ALTER SYSTEM SET track_commit_timestamp = on;
SELECT pg_reload_conf();

-- Criando o slot de replicação apenas se ele não existir
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_replication_slots WHERE slot_name = 'my_slot') THEN
        PERFORM pg_create_logical_replication_slot('my_slot', 'pgoutput');
    END IF;
END $$;

-- Criando uma publicação para todas as tabelas
CREATE PUBLICATION my_publication FOR ALL TABLES;

-- Validando a configuração da replicação
SELECT * FROM pg_publication;
SELECT * FROM pg_subscription;
SELECT * FROM pg_replication_slots;
SELECT * FROM pg_stat_replication;

-- Criando os schemas do banco
CREATE SCHEMA IF NOT EXISTS public;
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
CREATE SCHEMA IF NOT EXISTS audit_log;

-- Criando a tabela de auditoria para registrar mudanças
CREATE TABLE IF NOT EXISTS audit_log.changes (
    id SERIAL PRIMARY KEY,
    table_name TEXT,
    change_type TEXT,
    record JSONB,
    captured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criando tabelas na camada RAW
CREATE TABLE IF NOT EXISTS raw.accounts (
    id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    event_uuid UUID NOT NULL,
    event_type TEXT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);
CREATE INDEX idx_accounts_event_timestamp ON raw.accounts(event_timestamp);
CREATE INDEX idx_accounts_event_uuid ON raw.accounts(event_uuid);

CREATE TABLE IF NOT EXISTS raw.audits (
    id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    event_uuid UUID NOT NULL,
    event_type TEXT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.claims (
    id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    event_uuid UUID NOT NULL,
    event_type TEXT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.credit_scores (
    id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    event_uuid UUID NOT NULL,
    event_type TEXT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.entities (
    id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    event_uuid UUID NOT NULL,
    event_type TEXT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.insured_entities (
    id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    event_uuid UUID NOT NULL,
    event_type TEXT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.loans (
    id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    event_uuid UUID NOT NULL,
    event_type TEXT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.merchants (
    id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    event_uuid UUID NOT NULL,
    event_type TEXT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.payment_methods (
    id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    event_uuid UUID NOT NULL,
    event_type TEXT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.payments (
    id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    event_uuid UUID NOT NULL,
    event_type TEXT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.policies (
    id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    event_uuid UUID NOT NULL,
    event_type TEXT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.portfolios (
    id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    event_uuid UUID NOT NULL,
    event_type TEXT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.regulations (
    id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    event_uuid UUID NOT NULL,
    event_type TEXT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.risk_assessments (
    id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    event_uuid UUID NOT NULL,
    event_type TEXT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.subaccounts (
    id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    event_uuid UUID NOT NULL,
    event_type TEXT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.transactions (
    id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    event_uuid UUID NOT NULL,
    event_type TEXT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.user_verifications (
    id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    event_uuid UUID NOT NULL,
    event_type TEXT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS raw.users (
    id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    event_uuid UUID NOT NULL,
    event_type TEXT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Tabela para armazenar eventos da Dead Letter Queue (DLQ)
CREATE TABLE IF NOT EXISTS raw.dlq_events (
    id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    event_uuid UUID NOT NULL,
    event_type TEXT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    error_message TEXT
);
