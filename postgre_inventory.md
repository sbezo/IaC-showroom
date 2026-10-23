# PostgreSQL relationships

| Instance | Database / role | Consumer |
| --- | --- | --- |
| n8n Compose `postgres` | `n8n` / `n8n_app` | n8n workflows and application state |
| Same instance | `automation` / `automation_app` | Scripts API email ingestion |
| NetBox Compose `postgres` | `netbox` / `netbox` | NetBox |
| Keycloak host PostgreSQL | `keycloak` / `keycloak` | Identity service |

The n8n stack uses a separate bootstrap administrator (`postgres`).
`init-db.sh` creates the n8n role and the automation schema on an empty volume;
`provision-automation.sh` demonstrates creating or updating the automation role
and database. The API's `email/init_db.py` also creates the email table if absent.

`public.emails` stores subject, sender, recipient, body, direction, status, and a
creation timestamp. Downloaded messages and the processed-file log are runtime
data and are excluded from Git.

The `AUTOMATION_DB`, `AUTOMATION_DB_USER`, and `AUTOMATION_DB_PASSWORD` values in
[n8n/.env_example](n8n/.env_example) and
[scripts_via_api/.env_example](scripts_via_api/.env_example) must agree when adapted.
The API connects to `DB_HOST=postgres` through `n8n_default`. No database dump,
live metrics, backup schedule, or restore implementation is included.
