import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

from rich import print


DB_PATH = (
    "data/database/transcripts_clean.db"
)

OUTPUT_DIR = (
    "analysis/charts_clean"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True,
)


def main():

    print(
        "\n[bold cyan]"
        "Loading clean database..."
        "[/bold cyan]"
    )

    conn = sqlite3.connect(DB_PATH)

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

    # ==========================================
    # TRANSCRIPT LENGTH
    # ==========================================

    df["transcript_length"] = (
        df["transcript_clean"]
        .fillna("")
        .str.len()
    )

    # ==========================================
    # DATE
    # ==========================================

    df["call_date"] = pd.to_datetime(
        df["call_date"]
    )

    # ==========================================
    # INFO
    # ==========================================

    print(
        "\n[bold yellow]"
        "DATAFRAME INFO:"
        "[/bold yellow]"
    )

    df.info()

    # ==========================================
    # DESCRIBE
    # ==========================================

    print(
        "\n[bold yellow]"
        "TRANSCRIPT LENGTH STATS:"
        "[/bold yellow]"
    )

    print(
        df["transcript_length"]
        .describe()
    )

    # ==========================================
    # EMPTY TRANSCRIPTS
    # ==========================================

    empty_count = (
        df["transcript_clean"]
        .fillna("")
        .str.strip()
        .eq("")
        .sum()
    )

    print(
        f"\n[bold red]"
        f"EMPTY CLEAN TRANSCRIPTS: "
        f"{empty_count}"
        f"[/bold red]"
    )

    # ==========================================
    # HISTOGRAM
    # ==========================================

    print(
        "\n[bold yellow]"
        "Generating histogram..."
        "[/bold yellow]"
    )

    plt.figure(figsize=(12, 6))

    plt.hist(
        df["transcript_length"],
        bins=50,
    )

    plt.title(
        "Clean Transcript Length Distribution"
    )

    plt.xlabel("Transcript Length")

    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/"
        f"clean_transcript_histogram.png"
    )

    plt.close()

    # ==========================================
    # BOXPLOT
    # ==========================================

    print(
        "\n[bold yellow]"
        "Generating boxplot..."
        "[/bold yellow]"
    )

    plt.figure(figsize=(12, 6))

    plt.boxplot(
        df["transcript_length"],
        vert=False,
    )

    plt.title(
        "Clean Transcript Length Boxplot"
    )

    plt.xlabel("Transcript Length")

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/"
        f"clean_transcript_boxplot.png"
    )

    plt.close()

    # ==========================================
    # YEAR DISTRIBUTION
    # ==========================================

    year_counts = (
        df["earnings_year"]
        .value_counts()
        .sort_index()
    )

    plt.figure(figsize=(10, 6))

    year_counts.plot(kind="bar")

    plt.title(
        "Clean Earnings Calls by Year"
    )

    plt.xlabel("Year")

    plt.ylabel("Count")

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/"
        f"clean_year_distribution.png"
    )

    plt.close()

    # ==========================================
    # TIMELINE
    # ==========================================

    timeline = (
        df.groupby(
            df["call_date"]
            .dt.to_period("M")
        )
        .size()
    )

    timeline.index = (
        timeline.index.astype(str)
    )

    plt.figure(figsize=(18, 6))

    timeline.plot()

    plt.title(
        "Clean Earnings Calls Over Time"
    )

    plt.xlabel("Month")

    plt.ylabel("Count")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/"
        f"clean_calls_over_time.png"
    )

    plt.close()

    print(
        "\n[bold green]"
        "CLEAN EDA COMPLETE"
        "[/bold green]"
    )

    print(
        f"\n[bold cyan]"
        f"Charts saved to:"
        f" {OUTPUT_DIR}"
        f"[/bold cyan]"
    )
    
        # ==========================================
    # TOP TICKERS
    # ==========================================

    top_tickers = (
        df["ticker"]
        .value_counts()
        .head(20)
    )

    plt.figure(figsize=(14, 8))

    top_tickers.plot(kind="bar")

    plt.title(
        "Top 20 Tickers"
    )

    plt.xlabel("Ticker")

    plt.ylabel("Transcript Count")

    plt.xticks(rotation=90)

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/"
        f"clean_top_tickers.png"
    )

    plt.close()
    
        # ==========================================
    # QUARTER DISTRIBUTION
    # ==========================================

    quarter_counts = (
        df["quarter"]
        .value_counts()
    )

    plt.figure(figsize=(10, 6))

    quarter_counts.plot(kind="bar")

    plt.title(
        "Clean Earnings Calls by Quarter"
    )

    plt.xlabel("Quarter")

    plt.ylabel("Count")

    plt.xticks(rotation=0)

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/"
        f"clean_quarter_distribution.png"
    )

    plt.close()

        # ==========================================
    # TOP COMPANIES
    # ==========================================

    top_companies = (
        df["company"]
        .value_counts()
        .head(20)
    )

    plt.figure(figsize=(14, 8))

    top_companies.plot(kind="bar")

    plt.title(
        "Top 20 Companies"
    )

    plt.xlabel("Company")

    plt.ylabel("Transcript Count")

    plt.xticks(rotation=90)

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/"
        f"clean_top_companies.png"
    )

    plt.close()
    
        # ==========================================
    # RAW VS CLEAN LENGTH
    # ==========================================

    df["raw_length"] = (
        df["transcript"]
        .fillna("")
        .str.len()
    )

    plt.figure(figsize=(12, 6))

    plt.hist(
        df["raw_length"],
        bins=50,
        alpha=0.5,
        label="Raw",
    )

    plt.hist(
        df["transcript_length"],
        bins=50,
        alpha=0.5,
        label="Clean",
    )

    plt.title(
        "Raw vs Clean Transcript Length"
    )

    plt.xlabel("Transcript Length")

    plt.ylabel("Frequency")

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/"
        f"raw_vs_clean_histogram.png"
    )

    plt.close()

if __name__ == "__main__":

    main()