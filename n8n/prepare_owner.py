#!/usr/bin/env python3
# Run on the deployment host. Never print the password or its hash.
import os
from pathlib import Path

import bcrypt
from dotenv import dotenv_values


directory = Path(__file__).resolve().parent
settings = dotenv_values(directory / ".env", interpolate=False)
required = [
    "N8N_OWNER_EMAIL",
    "N8N_OWNER_FIRST_NAME",
    "N8N_OWNER_LAST_NAME",
    "N8N_OWNER_PASSWORD",
]
for name in required:
    value = settings.get(name)
    if not value or value.startswith("CHANGE_ME"):
        raise SystemExit("Fill the owner account fields in .env before deploying.")

password = settings["N8N_OWNER_PASSWORD"].encode()
if len(password) < 8 or len(password) > 72:
    raise SystemExit("The owner password must contain between 8 and 72 bytes.")

os.umask(0o077)
output = directory / ".owner.env"
if output.exists():
    old_hash = dotenv_values(output, interpolate=False).get("N8N_INSTANCE_OWNER_PASSWORD_HASH")
    if old_hash and bcrypt.checkpw(password, old_hash.encode()):
        output.chmod(0o600)
        print("Owner password hash unchanged.")
        raise SystemExit(0)

password_hash = bcrypt.hashpw(password, bcrypt.gensalt()).decode()
output.write_text("N8N_INSTANCE_OWNER_PASSWORD_HASH=" + password_hash + "\n")
output.chmod(0o600)
print("Owner password hash prepared.")
