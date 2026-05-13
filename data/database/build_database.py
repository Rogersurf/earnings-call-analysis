# build_database.py

import json
import sqlite3
from pathlib import Path

from rich import print


JSON_DIR = Path("data/processed/json")
DB_PATH = Path("data/database/transcripts.db")


DB_PATH.parent.mkdir(parents=True, exist_ok=True)


conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS transcripts (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        ticker TEXT,
        company TEXT,

        quarter TEXT,
        earnings_year INTEGER,

        call_date TEXT,

        title TEXT,

        transcript TEXT,

        source_url TEXT UNIQUE,

        scraped_at TEXT
    )
    """
)


json_files = list(JSON_DIR.glob("*.json"))

print(
    f"\n[bold green]FOUND {len(json_files)} JSON FILES[/bold green]"
)


inserted = 0
skipped = 0
errors = 0


for idx, file_path in enumerate(json_files, start=1):

    try:

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        cursor.execute(
            """
            INSERT OR IGNORE INTO transcripts (
                ticker,
                company,
                quarter,
                earnings_year,
                call_date,
                title,
                transcript,
                source_url,
                scraped_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data.get("ticker"),
                data.get("company"),
                data.get("quarter"),
                data.get("earnings_year"),
                data.get("date"),
                data.get("title"),
                data.get("transcript"),
                data.get("source_url"),
                data.get("scraped_at"),
            ),
        )

        if cursor.rowcount == 1:
            inserted += 1
        else:
            skipped += 1

        if idx % 100 == 0:

            conn.commit()

            print(
                f"[cyan]Processed {idx}/{len(json_files)}[/cyan]"
            )

    except Exception as e:

        errors += 1

        print(
            f"[red]ERROR:[/red] {file_path.name} -> {e}"
        )


conn.commit()


cursor.execute(
    "SELECT COUNT(*) FROM transcripts"
)


total_rows = cursor.fetchone()[0]


print(
    f"\n[bold green]DATABASE COMPLETE[/bold green]"
)

print(f"Inserted: {inserted}")
print(f"Skipped: {skipped}")
print(f"Errors: {errors}")
print(f"Total rows in DB: {total_rows}")
print(f"Database path: {DB_PATH}")


conn.close()