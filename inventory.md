# Example topology

All addresses and names below are fictional and match the source examples.

| Ansible host | Guest hostname | Address | Role |
| --- | --- | --- | --- |
| `infra-host` | `infra-services.example.test` | `192.0.2.10` | DNS, DHCP, CA, NFS, Vault, Keycloak |
| `runner-host` | `gitlab-runner.example.test` | `192.0.2.19` | CI runner |
| `gitlab-host` | `gitlab.example.test` | `192.0.2.20` | GitLab |
| `app-host` | `apps.example.test` | `192.0.2.21` | NetBox, phpIPAM, n8n, scripts API, Nginx |

The illustrative gateway is `192.0.2.1`. DNS is `192.0.2.10`; DHCP offers
`.128`–`.254`. The example NFS export serves `192.0.2.0/24`.

Nginx terminates HTTPS for `netbox.example.test`, `phpipam.example.test`, and
`n8n.example.test`, forwarding to loopback ports 8080, 8081, and 5678.
`demo-app.example.test` illustrates another upstream on 8082; its application is
intentionally not included. GitLab exposes HTTPS and SSH on port 2222. Vault
uses HTTPS on 8200 and Keycloak on 8443.

The scripts API is available only on the shared `n8n_default` Docker network
at `http://scripts-api:8000`. Its health endpoint checks the API process, not
PostgreSQL or S3. These are configuration relationships, not live status.
