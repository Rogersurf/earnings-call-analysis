import sqlite3
import pandas as pd

from rich import print


INPUT_DB = "data/database/transcripts.db"

OUTPUT_DB = "data/database/transcripts_clean.db"


def extract_section(
    text: str,
    start: str,
    end: str,
):

    if start in text and end in text:

        return (
            text.split(start)[1]
            .split(end)[0]
            .strip()
        )

    return ""


def extract_transcript(
    text: str,
):

    marker = (
        "Full Conference Call Transcript"
    )

    if marker in text:

        return (
            text.split(marker)[1]
            .split("Read Next")[0]
            .strip()
        )

    return text


def main():

    print(
        "\n[bold cyan]"
        "Loading database..."
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

    # ==========================================
    # CLEANING
    # ==========================================

    article_intro = []

    takeaways = []

    summaries = []

    glossaries = []

    cleaned_transcripts = []

    for idx, row in df.iterrows():

        text = row["transcript"]

        intro = extract_section(
            text,
            "Earnings Call Transcript",
            "TAKEAWAYS",
        )

        takeaway = extract_section(
            text,
            "TAKEAWAYS",
            "SUMMARY",
        )

        summary = extract_section(
            text,
            "SUMMARY",
            "INDUSTRY GLOSSARY",
        )

        glossary = extract_section(
            text,
            "INDUSTRY GLOSSARY",
            "Full Conference Call Transcript",
        )

        transcript_clean = (
            extract_transcript(text)
        )

        article_intro.append(intro)

        takeaways.append(takeaway)

        summaries.append(summary)

        glossaries.append(glossary)

        cleaned_transcripts.append(
            transcript_clean
        )

        if idx % 500 == 0:

            print(
                f"[yellow]"
                f"Processed {idx}"
                f"[/yellow]"
            )

    # ==========================================
    # NEW COLUMNS
    # ==========================================

    df["article_intro"] = article_intro

    df["takeaways"] = takeaways

    df["summary"] = summaries

    df["glossary"] = glossaries

    df["transcript_clean"] = (
        cleaned_transcripts
    )

    # ==========================================
    # SAVE CLEAN DB
    # ==========================================

    print(
        "\n[bold cyan]"
        "Saving clean database..."
        "[/bold cyan]"
    )

    clean_conn = sqlite3.connect(
        OUTPUT_DB
    )

    df.to_sql(
        "transcripts",
        clean_conn,
        if_exists="replace",
        index=False,
    )

    clean_conn.close()

    print(
        "\n[bold green]"
        "CLEAN DATABASE SAVED"
        "[/bold green]"
    )

    print(
        f"\n[bold cyan]"
        f"OUTPUT:"
        f" {OUTPUT_DB}"
        f"[/bold cyan]"
    )


if __name__ == "__main__":

    main()