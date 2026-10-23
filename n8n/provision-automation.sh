#!/bin/sh
# Runs on first initialization and through Ansible for existing installations.
set -eu

if [ "$AUTOMATION_DB" = "$POSTGRES_DB" ] || \
   [ "$AUTOMATION_DB_USER" = "$POSTGRES_USER" ] || \
   [ "$AUTOMATION_DB_USER" = "$N8N_DB_USER" ]; then
    echo "Use a separate automation database and user." >&2
    exit 1
fi

psql --no-psqlrc --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
    --set=ON_ERROR_STOP=1 \
    --set=app_user="$AUTOMATION_DB_USER" \
    --set=app_password="$AUTOMATION_DB_PASSWORD" \
    --set=db_name="$AUTOMATION_DB" <<'SQL'
SELECT format('CREATE USER %I', :'app_user')
WHERE NOT EXISTS (SELECT FROM pg_roles WHERE rolname = :'app_user')
\gexec

-- Synchronize the password with .env on subsequent deployments too.
ALTER ROLE :"app_user" WITH PASSWORD :'app_password';

SELECT format('CREATE DATABASE %I OWNER %I', :'db_name', :'app_user')
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = :'db_name')
\gexec

ALTER DATABASE :"db_name" OWNER TO :"app_user";
REVOKE ALL ON DATABASE :"db_name" FROM PUBLIC;
SQL
