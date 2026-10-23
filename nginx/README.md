# Reverse proxy

`reverse-proxy.conf` maps example hostnames to local application ports and
illustrates HTTPS termination. The demo-app upstream is a placeholder; no app
implementation is included. Certificates and private keys referenced under
`/etc/nginx/ssl` must be supplied separately. n8n has its own proxy configuration
in `../n8n/nginx.conf`.
