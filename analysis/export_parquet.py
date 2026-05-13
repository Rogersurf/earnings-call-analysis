import sqlite3
import pandas as pd

from rich import print


INPUT_DB = (
    "data/database/transcripts_clean.db"
)

OUTPUT_PARQUET = (
    "data/database/transcripts_clean.parquet"
)


def main():

    print(
        "\n[bold cyan]"
        "Loading clean database..."
        "[/bold cyan]"
    )

    conn = sqlite3.connect(INPUT_DB)

    query = """
    SELECT *
    FROM transcripts
    """

    df = pd.read_sql_query(
        query,
        conn,
    )

    conn.close()

    print(
        f"\n[bold green]"
        f"Loaded {len(df)} rows"
        f"[/bold green]"
    )

    print(
        "\n[bold yellow]"
        "Exporting parquet..."
        "[/bold yellow]"
    )

    df.to_parquet(
        OUTPUT_PARQUET,
        index=False,
    )

    print(
        "\n[bold green]"
        "PARQUET EXPORTED"
        "[/bold green]"
    )

    print(
        f"\n[bold cyan]"
        f"Saved:"
        f" {OUTPUT_PARQUET}"
        f"[/bold cyan]"
    )


if __name__ == "__main__":

    main()