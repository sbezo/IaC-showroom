# Scripts via API

A small FastAPI service lets n8n trigger a fixed email-processing script.

| Endpoint | Behavior |
| --- | --- |
| `GET /health` | Process health only; no database or S3 check |
| `POST /email/process` | Requires the exact API token in the `Authorization` header |

The POST handler uses a subprocess timeout and a process-local lock. Keep one
Uvicorn worker for that lock to serialize requests. Concurrent calls receive 409;
authentication failures receive 401. There is no arbitrary command endpoint.

`email/process_emails.py` syncs messages from S3, parses MIME, and inserts rows
into PostgreSQL. Downloaded files and `processed.txt` persist in a Docker volume.
A crash between insertion and history update can duplicate an email; the example
does not provide exactly-once processing. `email/init_db.py` creates the table.
`email/check_db.py` is an interactive SQL helper for a disposable lab.

`.env_example` documents API, database, and AWS inputs. The API mounts `.env`
read-only and loads it without interpolation; Compose uses `--env-file /dev/null`
in the systemd unit. The build excludes secrets and downloaded messages.
AWS credentials loaded by Python are inherited by the AWS CLI subprocess.

The service joins `n8n_default` at `http://scripts-api:8000`, with no published
host port. n8n and its database must be adapted first. The source retains runnable
application concepts, but no credentials, message data, or working deployment
are supplied.
