import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from rich import print


DB_PATH = "data/database/transcripts.db"


def main():

    print(
        "\n[bold cyan]"
        "Loading database..."
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
        f"Loaded {len(df)} rows"
        f"[/bold green]"
    )

    # ==========================================
    # Transcript Length
    # ==========================================

    df["transcript_length"] = (
        df["transcript"]
        .fillna("")
        .str.len()
    )

    # ==========================================
    # Convert Dates
    # ==========================================

    df["call_date"] = pd.to_datetime(
        df["call_date"]
    )

    # ==========================================
    # OUTPUT FOLDER
    # ==========================================

    import os

    os.makedirs(
        "analysis/charts",
        exist_ok=True,
    )

    # ==========================================
    # 1. Earnings Year Distribution
    # ==========================================

    print(
        "\n[bold yellow]"
        "Generating year distribution chart..."
        "[/bold yellow]"
    )

    year_counts = (
        df["earnings_year"]
        .value_counts()
        .sort_index()
    )

    plt.figure(figsize=(10, 6))

    year_counts.plot(kind="bar")

    plt.title("Earnings Calls by Year")

    plt.xlabel("Year")

    plt.ylabel("Count")

    plt.tight_layout()

    plt.savefig(
        "analysis/charts/earnings_by_year.png"
    )

    plt.close()

    # ==========================================
    # 2. Quarter Distribution
    # ==========================================

    print(
        "\n[bold yellow]"
        "Generating quarter distribution chart..."
        "[/bold yellow]"
    )

    quarter_counts = (
        df["quarter"]
        .value_counts()
    )

    plt.figure(figsize=(10, 6))

    quarter_counts.plot(kind="bar")

    plt.title("Earnings Calls by Quarter")

    plt.xlabel("Quarter")

    plt.ylabel("Count")

    plt.tight_layout()

    plt.savefig(
        "analysis/charts/earnings_by_quarter.png"
    )

    plt.close()

    # ==========================================
    # 3. Top 20 Tickers
    # ==========================================

    print(
        "\n[bold yellow]"
        "Generating top tickers chart..."
        "[/bold yellow]"
    )

    top_tickers = (
        df["ticker"]
        .value_counts()
        .head(20)
    )

    plt.figure(figsize=(14, 8))

    top_tickers.plot(kind="bar")

    plt.title("Top 20 Tickers")

    plt.xlabel("Ticker")

    plt.ylabel("Transcript Count")

    plt.tight_layout()

    plt.savefig(
        "analysis/charts/top_tickers.png"
    )

    plt.close()

    # ==========================================
    # 4. Transcript Length Histogram
    # ==========================================

    print(
        "\n[bold yellow]"
        "Generating transcript length histogram..."
        "[/bold yellow]"
    )

    plt.figure(figsize=(12, 6))

    plt.hist(
        df["transcript_length"],
        bins=50,
    )

    plt.title("Transcript Length Distribution")

    plt.xlabel("Transcript Length")

    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(
        "analysis/charts/transcript_length_histogram.png"
    )

    plt.close()

    # ==========================================
    # 5. Transcript Length Boxplot
    # ==========================================

    print(
        "\n[bold yellow]"
        "Generating transcript length boxplot..."
        "[/bold yellow]"
    )

    plt.figure(figsize=(12, 6))

    plt.boxplot(
        df["transcript_length"],
        vert=False,
    )

    plt.title("Transcript Length Boxplot")

    plt.xlabel("Transcript Length")

    plt.tight_layout()

    plt.savefig(
        "analysis/charts/transcript_length_boxplot.png"
    )

    plt.close()

    # ==========================================
    # 6. Calls Over Time
    # ==========================================

    print(
        "\n[bold yellow]"
        "Generating timeline chart..."
        "[/bold yellow]"
    )

    timeline = (
        df.groupby(
            df["call_date"].dt.to_period("M")
        )
        .size()
    )

    timeline.index = (
        timeline.index.astype(str)
    )

    plt.figure(figsize=(18, 6))

    timeline.plot()

    plt.title("Earnings Calls Over Time")

    plt.xlabel("Month")

    plt.ylabel("Count")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        "analysis/charts/calls_over_time.png"
    )

    plt.close()

    # ==========================================
    # Final Stats
    # ==========================================

    print(
        "\n[bold green]"
        "EDA COMPLETE"
        "[/bold green]"
    )

    print(
        "\n[bold cyan]"
        "Charts saved to:"
        " analysis/charts/"
        "[/bold cyan]"
    )
    
    outliers = df[
    df["transcript_length"] > 120000
    ]

    print(
        "\n[bold red]"
        "OUTLIERS > 120K:"
        "[/bold red]"
    )

    print(
        outliers[
            [
                "ticker",
                "company",
                "quarter",
                "earnings_year",
                "transcript_length",
            ]
        ]
    )
    
    outliers.to_csv(
    "analysis/outliers.csv",
    index=False,
    )


if __name__ == "__main__":

    main()