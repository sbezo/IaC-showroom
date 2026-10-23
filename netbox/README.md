# NetBox and IPAM API examples

Compose illustrates NetBox with PostgreSQL, Redis, and persistent volumes behind
Nginx. `.env_example` documents database and bootstrap settings; the database
password fields must agree. This is a simplified stack, not a full NetBox release
configuration.

`NetBox-API/` contains small Python examples for creating a site/VLAN/prefix,
importing synthetic CSV addresses, reserving an address, and releasing one.
They require `pynetbox`, `python-dotenv`, and their own `.env` based on
`NetBox-API/.env_example`. Run initial setup before the other examples. API writes
change the configured server; use only a disposable lab after adapting them.
