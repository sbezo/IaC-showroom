# Workflow automation

Compose illustrates n8n, PostgreSQL, and an external task runner. Nginx terminates
TLS; the scripts API joins the resulting `n8n_default` network.

`.env_example` lists the database roles, owner account, encryption key, and runner
token. `prepare_owner.py` (bcrypt and python-dotenv) creates the ignored
`.owner.env` password hash; Compose reads that file in raw mode. The Ansible
playbook demonstrates this preparation before systemd starts the stack.

`init-db.sh` handles an empty PostgreSQL volume; `provision-automation.sh` also
shows provisioning a separate automation database on an existing instance.
See [database relationships](../postgre_inventory.md). TLS files, owner hashes,
workflow data, and credentials are intentionally absent.
