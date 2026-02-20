import os
import uuid
import requests
import logging
from bs4 import BeautifulSoup
from typing import List
from agent.models import Source
from agent.cleaning import clean_html

# Configure basic logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def ingest_urls(urls: List[str]) -> List[Source]:
    sources = []

    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                logging.warning(f"Failed to fetch URL {url}: Status code {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.title.string if soup.title else None
            content = clean_html(soup.get_text())
            if not content:
                logging.warning(f"No content extracted from URL {url}")
                continue

            sources.append(
                Source(
                    source_id=str(uuid.uuid4()),
                    title=title,
                    url=url,
                    content=content,
                    length=len(content),
                )
            )

        except Exception as e:
            logging.error(f"Error fetching URL {url}: {e}")
            continue

    return sources


def ingest_folder(folder_path: str) -> List[Source]:
    sources = []

    for filename in os.listdir(folder_path):
        path = os.path.join(folder_path, filename)

        if not os.path.isfile(path):
            continue

        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = f.read().strip()

            # 🔹 If HTML file → clean it
            if filename.lower().endswith((".html", ".htm")):
                content = clean_html(raw)
            else:
                # 🔹 Plain text file → use raw text
                content = raw

            if not content:
                logging.warning(f"No content extracted from file {filename}")
                continue

            sources.append(
                Source(
                    source_id=str(uuid.uuid4()),
                    title=filename,
                    url=None,
                    content=content,
                    length=len(content),
                )
            )

        except Exception as e:
            logging.error(f"Error reading file {filename}: {e}")
            continue

    return sources
