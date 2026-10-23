# VM provisioning

`main.tf` shows four vSphere VM clones from an `ubuntu-template`, using an
example resource pool, datastore, and management network. `variables.tf`
defines the connection inputs; `.env_example` shows their `TF_VAR_*` names.
Terraform does not load dotenv files automatically.

The provider lock file records the inherited provider selection. State, provider
binaries, and real vCenter settings are omitted. Addresses and object names must
be replaced in a separate lab before planning or applying.
