"""Create the email table if needed using the automation database owner's credentials."""

import os
from pathlib import Path

from dotenv import load_dotenv
import psycopg


def main():
    load_dotenv(Path(__file__).resolve().parent.parent / ".env", interpolate=False)
    with psycopg.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["AUTOMATION_DB"],
        user=os.environ["AUTOMATION_DB_USER"],
        password=os.environ["AUTOMATION_DB_PASSWORD"],
        connect_timeout=10,
        options="-c statement_timeout=30000",
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS emails (
                    id BIGSERIAL PRIMARY KEY,
                    subject TEXT NOT NULL,
                    sender TEXT NOT NULL,
                    recipient TEXT NOT NULL,
                    body TEXT NOT NULL,
                    direction TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
    print("Email table is ready.")


if __name__ == "__main__":
    main()
