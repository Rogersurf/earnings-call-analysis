import json
import os
import re
import time
import random
from datetime import datetime, UTC

import httpx

from rich import print
from selectolax.parser import HTMLParser
from fake_useragent import UserAgent


INPUT_FILE = "data/discovered_urls.json"

OUTPUT_JSON_DIR = "data/processed/json/"
OUTPUT_TXT_DIR = "data/processed/txt/"


def fetch_html(url: str) -> str:

    headers = {
        "User-Agent": UserAgent().random,
        "Accept-Language": "en-US,en;q=0.9",
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

    candidates = tree.css("div, section, article, main")

    best_text = ""

    for node in candidates:

        text = node.text(separator="\n", strip=True)

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

    os.makedirs(OUTPUT_JSON_DIR, exist_ok=True)
    os.makedirs(OUTPUT_TXT_DIR, exist_ok=True)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:

        urls = json.load(f)

    print(
        f"\n[bold green]"
        f"TOTAL URLS: {len(urls)}"
        f"[/bold green]"
    )

    for idx, url in enumerate(urls, start=1):

        print(
            f"\n[cyan]"
            f"[{idx}/{len(urls)}]"
            f" Fetching:"
            f"[/cyan] {url}"
        )

        try:

            html = fetch_html(url)

            metadata = parse_metadata_from_url(url)

            if not metadata:

                print(
                    "[yellow]Skipping invalid URL[/yellow]"
                )

                continue

            transcript_data = extract_transcript(html)

            final_data = {
                **metadata,
                **transcript_data,
                "source_url": url,
                "scraped_at": datetime.now(UTC).isoformat(),
            }

            filename = (
                f"{metadata['date']}_"
                f"{metadata['ticker']}_"
                f"{metadata['quarter']}_"
                f"{metadata['earnings_year']}"
            )

            json_path = (
                f"{OUTPUT_JSON_DIR}{filename}.json"
            )

            txt_path = (
                f"{OUTPUT_TXT_DIR}{filename}.txt"
            )

            if os.path.exists(json_path):

                print(
                    f"[yellow]SKIPPING EXISTING:[/yellow] "
                    f"{filename}"
                )

                continue

            with open(
                json_path,
                "w",
                encoding="utf-8",
            ) as f:

                json.dump(
                    final_data,
                    f,
                    ensure_ascii=False,
                    indent=4,
                )

            with open(
                txt_path,
                "w",
                encoding="utf-8",
            ) as f:

                f.write(final_data["transcript"])

            print(
                f"[green]Saved:[/green] "
                f"{filename}"
            )

            time.sleep(random.uniform(1, 3))

        except Exception as e:

            print(f"[red]ERROR:[/red] {e}")