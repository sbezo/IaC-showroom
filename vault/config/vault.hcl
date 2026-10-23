# Reference configuration; TLS files are intentionally not included.
ui = true
disable_mlock = true
api_addr = "https://vault.example.test:8200"

storage "file" {
  path = "/opt/vault/data"
}

listener "tcp" {
  address = "0.0.0.0:8200"
  tls_cert_file = "/opt/vault/tls/vault-cert.pem"
  tls_key_file = "/opt/vault/tls/vault-key.pem"
}
