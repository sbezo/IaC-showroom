from pathlib import Path
from email import policy
from email.parser import BytesParser
import subprocess
from dotenv import load_dotenv
import psycopg
import os
import json


current_folder = Path(__file__).resolve().parent
load_dotenv(Path(__file__).resolve().parent.parent / ".env", interpolate=False)

automation_db_user = os.getenv("AUTOMATION_DB_USER")
automation_db_password = os.getenv("AUTOMATION_DB_PASSWORD")
automation_db = os.getenv("AUTOMATION_DB")
db_host = os.getenv("DB_HOST")
bucket = os.getenv("S3_BUCKET")
data_folder = Path(os.getenv("EMAIL_DATA_DIR", str(current_folder)))
email_folder = data_folder / "raw_emails"
history = data_folder / "processed.txt"


def main():
    email_folder.mkdir(parents=True, exist_ok=True)
    # Sync the S3 bucket to the local folder.
    subprocess.run(
        ["aws", "s3", "sync", f"s3://{bucket}", str(email_folder), "--quiet"],
        check=True,
        timeout=240,
    )

    # Keep track of processed files to avoid reprocessing.
    processed = set()
    if history.exists():
        processed = set(history.read_text().splitlines())

    # Process each email file in the folder.
    saved = 0
    for path in email_folder.iterdir():
        if not path.is_file() or path.name in processed:
            continue

        # process the email file
        process_email(path)

        # Remember the file only after successful processing.
        with history.open("a") as file:
            file.write(path.name + "\n")
        saved += 1

    return {"status": "ok", "processed": saved}

def process_email(path):
    with path.open("rb") as file:
        message = BytesParser(policy=policy.default).parse(file)

    subject = str(message.get("Subject", ""))
    sender = str(message.get("From", ""))
    recipient = ", ".join(str(value) for value in message.get_all("To", []))
    body_part = message.get_body(preferencelist=("plain", "html"))
    body = body_part.get_content() if body_part is not None else ""

    with psycopg.connect(
        host=db_host,
        dbname=automation_db,
        user=automation_db_user,
        password=automation_db_password,
        connect_timeout=10,
        options="-c statement_timeout=30000",
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO emails
                    (subject, sender, recipient, body, direction, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (subject, sender, recipient, body, "incoming", "unprocessed"),
            )

if __name__ == "__main__":
    print(json.dumps(main()))
