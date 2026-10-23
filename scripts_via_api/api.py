import hmac
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
from dotenv import load_dotenv
from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse

load_dotenv(Path(__file__).resolve().parent / ".env", interpolate=False)
scripts_api_token = os.environ["SCRIPTS_API_TOKEN"]

app = FastAPI(title="Scripts via API")
if not scripts_api_token:
    raise ValueError("SCRIPTS_API_TOKEN must not be empty")

email_script = Path(__file__).parent / "email" / "process_emails.py"
email_lock = threading.Lock()


@app.get("/health")
def health():
    # FastAPI converts dictionaries to JSON automatically.
    return {"status": "ok"}


@app.post("/email/process")
def process_email(authorization: str = Header(default="")):
    # Use ordinary def: subprocess.run blocks. FastAPI runs this in a thread.
    expected = scripts_api_token.encode("utf-8")
    supplied = authorization.encode("utf-8")
    if not hmac.compare_digest(supplied, expected):
        return JSONResponse({"error": "Unauthorized"}, status_code=401)

    if not email_lock.acquire(blocking=False):
        return JSONResponse({"error": "Email processing is already running"}, status_code=409)

    try:
        result = subprocess.run(
            [sys.executable, str(email_script)],
            check=True,
            capture_output=True,
            text=True,
            timeout=300,
        )
        return json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        return JSONResponse({"error": "Email processing exceeded 300 seconds"}, status_code=504)
    except (subprocess.CalledProcessError, OSError, ValueError):
        return JSONResponse(
            {"error": "Email processing failed; check S3 and database configuration"},
            status_code=500,
        )
    finally:
        email_lock.release()
