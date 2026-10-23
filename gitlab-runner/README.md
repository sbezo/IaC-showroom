# CI runner

`../ansible/playbooks/install_gitlab-runner.yml` illustrates package installation
and trusting a private CA. The referenced `ca.example.test.crt` is not included.
Runner registration, executor selection, and the registration token are supplied
separately in an adapted lab. No runner credentials are stored here.
