CREATE SCHEMA IF NOT EXISTS api;

-- To enable uuid_generate_v4 function from UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create the clans table in the api schema
CREATE TABLE IF NOT EXISTS api.clans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    region VARCHAR(4),
    created_at TIMESTAMPTZ DEFAULT NOW()
);