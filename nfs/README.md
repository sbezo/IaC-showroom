# Shared storage

`exports.j2` renders exports from `nfs_exports` in
`../ansible/inventories/host_vars/infra-host.yml`. The playbook creates export
directories, installs the server, and applies the template. The example grants
`192.0.2.0/24` access to `/srv/nfs/shared` with `root_squash`. Adapt the client
range and permissions to an isolated lab.
