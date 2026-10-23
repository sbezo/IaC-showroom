#!/bin/sh
# PostgreSQL runs this script only when initializing an empty data volume.
set -eu

psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
    --set=ON_ERROR_STOP=1 \
    --set=app_user="$N8N_DB_USER" \
    --set=app_password="$N8N_DB_PASSWORD" \
    --set=db_name="$POSTGRES_DB" <<'SQL'
CREATE USER :"app_user" WITH PASSWORD :'app_password';
GRANT ALL PRIVILEGES ON DATABASE :"db_name" TO :"app_user";
GRANT ALL ON SCHEMA public TO :"app_user";
SQL

# Create the automation database before initializing its email table.
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
sh "$script_dir/provision-automation.sh"

psql --no-psqlrc --username "$POSTGRES_USER" --dbname "$AUTOMATION_DB" \
    --set=ON_ERROR_STOP=1 \
    --set=app_user="$AUTOMATION_DB_USER" <<'SQL'
BEGIN;
SET ROLE :"app_user";

CREATE TABLE IF NOT EXISTS public.emails (
    id BIGSERIAL PRIMARY KEY,
    subject TEXT NOT NULL,
    sender TEXT NOT NULL,
    recipient TEXT NOT NULL,
    body TEXT NOT NULL,
    direction TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMIT;
SQL

echo "The automation emails table is ready."
