CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount NUMERIC(10,2) NOT NULL CHECK (total_amount >= 0),
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER orders_updated_at_trigger
BEFORE UPDATE ON orders
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER customers_updated_at_trigger
BEFORE UPDATE ON customers
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();


# Configuração de replicação

ALTER USER biaas WITH REPLICATION;
CREATE PUBLICATION postgres_publication FOR ALL TABLES;
SELECT PG_CREATE_LOGICAL_REPLICATION_SLOT('postgres_replication', 'pgoutput');

CREATE USER replication_user WITH PASSWORD 'SenhaSegura123';
GRANT SELECT ON ALL TABLES IN SCHEMA public TO replication_user;

## Configurações extras

GRANT cloudsqlreplica TO replication_user;
GRANT cloudsqlreplica TO biaas;

GRANT USAGE ON SCHEMA public TO replication_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT ON TABLES TO replication_user;

ALTER SYSTEM SET wal_level = logical;
SELECT pg_reload_conf();

SELECT pg_create_physical_replication_slot('postgres_replication');



-- Inserção de dados na tabela 'customers'
INSERT INTO customers (first_name, last_name, email, phone_number, created_at, updated_at)
VALUES
('John', 'Doe', 'john.doe@example.com', '123-456-7890', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Jane', 'Smith', 'jane.smith@example.com', '234-567-8901', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Alice', 'Johnson', 'alice.johnson@example.com', '345-678-9012', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Bob', 'Brown', 'bob.brown@example.com', '456-789-0123', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Inserção de dados na tabela 'orders'
INSERT INTO orders (customer_id, order_date, total_amount, status, created_at, updated_at)
VALUES
(1, CURRENT_TIMESTAMP, 100.50, 'completed', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(1, CURRENT_TIMESTAMP, 200.75, 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(2, CURRENT_TIMESTAMP, 150.00, 'shipped', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(3, CURRENT_TIMESTAMP, 50.25, 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(4, CURRENT_TIMESTAMP, 75.10, 'completed', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Inserção de mais dados na tabela 'customers'
INSERT INTO customers (first_name, last_name, email, phone_number, created_at, updated_at)
VALUES
('Charlie', 'Davis', 'charlie.davis@example.com', '567-890-1234', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('David', 'Martinez', 'david.martinez@example.com', '678-901-2345', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Eva', 'Garcia', 'eva.garcia@example.com', '789-012-3456', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Frank', 'Wilson', 'frank.wilson@example.com', '890-123-4567', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Inserção de mais dados na tabela 'orders'
INSERT INTO orders (customer_id, order_date, total_amount, status, created_at, updated_at)
VALUES
(5, CURRENT_TIMESTAMP, 130.80, 'completed', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(6, CURRENT_TIMESTAMP, 90.50, 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(7, CURRENT_TIMESTAMP, 250.00, 'shipped', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(8, CURRENT_TIMESTAMP, 185.75, 'completed', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(5, CURRENT_TIMESTAMP, 99.99, 'pending', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(6, CURRENT_TIMESTAMP, 420.00, 'shipped', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);




SELECT 
    id, 
    audit_id, 
    entity_id, 
    status, 
    findings, 
    date, 
    created_at,
    datastream_metadata.uuid AS uuid,
    TIMESTAMP_SECONDS(CAST(CAST(datastream_metadata.source_timestamp AS INT64) / 1000 AS INT64)) AS source_timestamp,
    datastream_metadata.change_sequence_number AS change_sequence_number,
    datastream_metadata.change_type AS change_type
FROM `yams-lab-nonprod.cdc_postgres_cybergen.public_audits`
WHERE datastream_metadata.change_type = 'DELETE';