import json
import time
import random

import httpx

from rich import print
from selectolax.parser import HTMLParser
from fake_useragent import UserAgent


BASE_URL = "https://www.fool.com"

START_PAGE = 1
END_PAGE = 500


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


def extract_transcript_links(html: str):

    tree = HTMLParser(html)

    links = set()

    for node in tree.css("a"):

        href = node.attributes.get("href", "")

        if "/earnings/call-transcripts/" in href:

            if href.startswith("/"):

                full_url = BASE_URL + href

            else:

                full_url = href

            links.add(full_url)

    return list(links)


if __name__ == "__main__":

    all_links = set()

    for page in range(START_PAGE, END_PAGE + 1):

        if page == 1:

            url = (
                "https://www.fool.com/"
                "earnings-call-transcripts/"
            )

        else:

            url = (
                "https://www.fool.com/"
                f"earnings-call-transcripts/page/{page}/"
            )

        print(f"\n[cyan]Fetching:[/cyan] {url}")

        try:

            html = fetch_html(url)

            links = extract_transcript_links(html)

            print(
                f"[green]Found {len(links)} links "
                f"on page {page}[/green]"
            )

            all_links.update(links)

            time.sleep(random.uniform(1, 3))

        except Exception as e:

            print(f"[red]ERROR:[/red] {e}")

    all_links = sorted(list(all_links))

    print(
        f"\n[bold green]"
        f"TOTAL UNIQUE LINKS: {len(all_links)}"
        f"[/bold green]"
    )

    with open(
        "data/discovered_urls.json",
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            all_links,
            f,
            ensure_ascii=False,
            indent=4,
        )

    print(
        "\n[bold cyan]"
        "Saved URLs successfully"
        "[/bold cyan]"
    )