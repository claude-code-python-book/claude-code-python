-- setup_db.sql: a small shop database for Chapter 4.
-- Run it as a database superuser:  createdb shop && psql -d shop -f setup_db.sql
-- Change the mcp_reader password before using this anywhere but your laptop.

CREATE TABLE customers (
    id         serial PRIMARY KEY,
    name       text NOT NULL,
    email      text NOT NULL UNIQUE,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE orders (
    id          serial PRIMARY KEY,
    customer_id integer NOT NULL REFERENCES customers (id),
    total       numeric(10, 2) NOT NULL CHECK (total >= 0),
    status      text NOT NULL DEFAULT 'paid',
    created_at  timestamptz NOT NULL DEFAULT now()
);

INSERT INTO customers (name, email) VALUES
    ('Asha Rao', 'asha@example.com'),
    ('Ben Okafor', 'ben@example.com'),
    ('Chen Li', 'chen@example.com');

INSERT INTO orders (customer_id, total, status) VALUES
    (1, 120.50, 'paid'), (1, 89.99, 'paid'), (2, 15.00, 'refunded'),
    (2, 240.00, 'paid'), (3, 42.10, 'paid');

-- Least privilege: the MCP server logs in as a role that can only read.
CREATE ROLE mcp_reader LOGIN PASSWORD 'change-me';
GRANT CONNECT ON DATABASE shop TO mcp_reader;
GRANT USAGE ON SCHEMA public TO mcp_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO mcp_reader;
ALTER ROLE mcp_reader SET default_transaction_read_only = on;
ALTER ROLE mcp_reader SET statement_timeout = '5s';
