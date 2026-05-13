import sqlite3
import pandas as pd

from rich import print

print("SCRIPT STARTED")

DB_PATH = "data/database/transcripts.db"


def main():

    print(
        "\n[bold cyan]"
        "Loading SQLite database..."
        "[/bold cyan]"
    )

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT *
    FROM transcripts
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    print(
        f"\n[bold green]"
        f"TOTAL ROWS: {len(df)}"
        f"[/bold green]"
    )

    print(
        f"[bold green]"
        f"TOTAL COLUMNS: {len(df.columns)}"
        f"[/bold green]"
    )

    print("\n[bold yellow]COLUMNS:[/bold yellow]")

    print(df.columns.tolist())

    print(
        "\n[bold yellow]"
        "MISSING VALUES:"
        "[/bold yellow]"
    )

    print(df.isnull().sum())

    print(
        "\n[bold yellow]"
        "DUPLICATED SOURCE_URL:"
        "[/bold yellow]"
    )

    duplicates = df.duplicated(
        subset=["source_url"]
    ).sum()

    print(duplicates)

    print(
        "\n[bold yellow]"
        "EMPTY TRANSCRIPTS:"
        "[/bold yellow]"
    )

    empty_transcripts = (
        df["transcript"]
        .fillna("")
        .str.strip()
        .eq("")
        .sum()
    )

    print(empty_transcripts)

    print(
        "\n[bold yellow]"
        "TRANSCRIPT LENGTH STATS:"
        "[/bold yellow]"
    )

    transcript_lengths = (
        df["transcript"]
        .fillna("")
        .str.len()
    )

    print(transcript_lengths.describe())

    print(
        "\n[bold yellow]"
        "TOP 20 TICKERS:"
        "[/bold yellow]"
    )

    print(
        df["ticker"]
        .value_counts()
        .head(20)
    )

    print(
        "\n[bold yellow]"
        "QUARTER DISTRIBUTION:"
        "[/bold yellow]"
    )

    print(
        df["quarter"]
        .value_counts()
    )

    print(
        "\n[bold yellow]"
        "EARNINGS YEAR DISTRIBUTION:"
        "[/bold yellow]"
    )

    print(
        df["earnings_year"]
        .value_counts()
        .sort_index()
    )

    print(
        "\n[bold yellow]"
        "SAMPLE ROW:"
        "[/bold yellow]"
    )

    print(df.head(1).T)

    print(
        "\n[bold green]"
        "VALIDATION COMPLETE"
        "[/bold green]"
    )
    
    # Data info
    print(
    "\n[bold yellow]"
    "DATAFRAME INFO:"
    "[/bold yellow]"
    )

    df.info()
    
    # Describe numeric
    print(
    "\n[bold yellow]"
    "NUMERIC DESCRIBE:"
    "[/bold yellow]"
    )

    print(df.describe())
    
    # Describe full
    print(
    "\n[bold yellow]"
    "FULL DESCRIBE:"
    "[/bold yellow]"
    )

    print(
        df.describe(
            include="all"
        )
    )
    
    # Memory usage
    print(
    "\n[bold yellow]"
    "MEMORY USAGE:"
    "[/bold yellow]"
    )

    print(
        df.memory_usage(
            deep=True
        )
    )
    
    # Transcript length column
    df["transcript_length"] = (
    df["transcript"]
    .str.len()
    )
    
    print(
    "\n[bold yellow]"
    "TRANSCRIPT LENGTH DESCRIBE:"
    "[/bold yellow]"
    )

    print(
        df["transcript_length"]
        .describe()
    )


if __name__ == "__main__":

    main()