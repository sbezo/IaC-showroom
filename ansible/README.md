# Host configuration

`inventories/hosts.yml` groups four fictional hosts. `group_vars/all.yml`
contains shared SSH/become settings; `host_vars/infra-host.yml` defines NFS exports.
`playbooks/` illustrates package installation, file distribution, and service
management. Collections are listed in `requirements.yml`.

Every playbook has a deliberate failing pre-task and disables automatic fact
gathering. This prevents the public example from contacting hosts. After adapting
it, remove the guard and restore fact gathering where needed (notably Keycloak
and Vault). Supply SSH access and sudo credentials separately; no vault password
or encrypted credentials are included.

Service `.env` files and TLS files referenced by copy tasks are intentionally
absent. Their `.env_example` files document the required inputs. The GitLab
playbook includes guest disk expansion assumptions that must match the target OS.
