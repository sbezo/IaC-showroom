# GitLab

Compose illustrates persistent configuration, logs, and application data under
`GITLAB_HOME`, with HTTPS and SSH on port 2222. The Ansible playbook configures
the external URL and reads `GITLAB_ROOT_PASSWORD` from a local `.env` file.
See `.env_example` for placeholders.

TLS material under `certs/` and SSH keys under `ssh_deploy_keys/` are intentionally
absent. The deployment-user playbook demonstrates installing a public key;
Docker group membership grants broad control of the host.
