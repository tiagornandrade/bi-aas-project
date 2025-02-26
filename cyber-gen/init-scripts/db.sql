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
