# DNS, DHCP, and certificates

`named.conf.local` defines the `example.test` zone; `net.example.test` contains
its records. `dhcpd.conf` demonstrates a subnet, lease range, gateway, and DNS
server. Service units show host-level lifecycle management.

`ca_template.txt` illustrates creating a service key/CSR and signing it with an
existing example CA. No CA, private keys, certificates, or serial files are
included. Paths referenced by Ansible are placeholders for externally managed
TLS material; review ownership and permissions when adapting them.
