# Identity service

`../ansible/playbooks/install_keycloak.yml` illustrates a systemd-managed
Keycloak service with PostgreSQL, TLS, health checks, and one-time administrator
bootstrap. `.env_example` lists its four credential inputs.

The example assumes an existing CA on the infrastructure host. Adapt the pinned
release, checksum, Java runtime, and database version together before using it.
Bootstrap credentials and TLS material are intentionally omitted. Replace the
temporary administrator with a permanent account in an actual lab.
