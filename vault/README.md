# Secrets service

`../ansible/playbooks/install_vault.yml` illustrates package installation, CA-signed
TLS, configuration distribution, and systemd startup. `config/vault.hcl` shows a
single-node file backend and an HTTPS listener.

Initialization, unseal keys, root tokens, policies, and application authentication
are outside this example. No `.env` is required by this playbook; real Vault
credentials must remain outside Git.
