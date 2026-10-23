import os
from dotenv import load_dotenv
import psycopg
from pathlib import Path

current_folder = Path(__file__).resolve().parent
load_dotenv(Path(__file__).resolve().parent.parent / ".env", interpolate=False)


automation_db_user = os.getenv("AUTOMATION_DB_USER")
automation_db_password = os.getenv("AUTOMATION_DB_PASSWORD")
automation_db = os.getenv("AUTOMATION_DB")
db_host = os.getenv("DB_HOST")


def main():
    with psycopg.connect(
        host=db_host,
        dbname=automation_db,
        user=automation_db_user,
        password=automation_db_password,
        connect_timeout=10,
        options="-c statement_timeout=30000",
    ) as connection:
        while True:
            sql = input("Enter SQL: ")
            with connection.cursor() as cursor:
                cursor.execute(sql)
                rows = cursor.fetchall()

            if not rows:
                print("The emails table is empty.")
            else:
                for row in rows:
                    print(row)


if __name__ == "__main__":
    main()
