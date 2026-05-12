import httpx
from selectolax.parser import HTMLParser
from fake_useragent import UserAgent
from rich import print
import json
import re
from datetime import datetime, UTC


URL = "https://www.fool.com/earnings/call-transcripts/2026/05/12/atlanticus-atlc-q1-2026-earnings-transcript/"


def fetch_html(url: str) -> str:

    headers = {
        "User-Agent": UserAgent().random,
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://google.com",
    }

    response = httpx.get(
        url,
        headers=headers,
        timeout=30,
        follow_redirects=True,
    )

    response.raise_for_status()

    return response.text


def parse_metadata_from_url(url: str):

    pattern = (
        r"/earnings/call-transcripts/"
        r"(\d{4})/(\d{2})/(\d{2})/"
        r"(.+)-([A-Za-z]+)-q(\d)-(\d{4})"
    )

    match = re.search(pattern, url)

    if not match:
        return {}

    year, month, day, company, ticker, quarter, earnings_year = match.groups()

    return {
        "date": f"{year}-{month}-{day}",
        "company": company.replace("-", " ").title(),
        "ticker": ticker.upper(),
        "quarter": f"Q{quarter}",
        "earnings_year": earnings_year,
    }


def extract_transcript(html: str):

    tree = HTMLParser(html)

    title_node = tree.css_first("h1")

    title = title_node.text(strip=True) if title_node else None

    transcript_parts = []

    # Procura divs/main/sections grandes
    candidates = tree.css("div, section, article, main")

    best_text = ""

    for node in candidates:

        text = node.text(separator="\n", strip=True)

        # transcript pages são MUITO grandes
        if len(text) > len(best_text):
            best_text = text

    start_marker = "Earnings Call Transcript"
    end_marker = "Read Next"

    start_idx = best_text.find(start_marker)
    end_idx = best_text.find(end_marker)

    if start_idx != -1 and end_idx != -1:
        transcript = (
            best_text[start_idx:end_idx]
            .replace("\\n", "\n")
            .strip()
        )
    else:
        transcript = best_text

    return {
        "title": title,
        "transcript": transcript,
    }


if __name__ == "__main__":

    print("[cyan]Fetching transcript...[/cyan]")

    html = fetch_html(URL)

    # DEBUG HTML
    with open(
        "data/raw/debug.html",
        "w",
        encoding="utf-8",
    ) as f:
        f.write(html)

    metadata = parse_metadata_from_url(URL)

    transcript_data = extract_transcript(html)

    final_data = {
        **metadata,
        **transcript_data,
        "source_url": URL,
        "scraped_at": datetime.now(UTC).isoformat(),
    }

    print("\n[bold green]METADATA[/bold green]")

    for key, value in metadata.items():
        print(f"{key}: {value}")

    with open(
        "data/processed/test_transcript.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            final_data,
            f,
            ensure_ascii=False,
            indent=4,
        )

        txt_path = "data/processed/atlanticus_q1_2026.txt"

        with open(
            txt_path,
            "w",
            encoding="utf-8",
        ) as f:

            f.write(final_data["transcript"])

    print("\n[bold cyan]Saved JSON successfully[/bold cyan]")