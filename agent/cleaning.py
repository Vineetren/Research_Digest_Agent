import re
from bs4 import BeautifulSoup
from config.settings import MIN_CONTENT_LENGTH


def clean_html(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "html.parser")

    for script in soup(["script", "style"]):
        script.decompose()

    text = soup.get_text(separator="\n")
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    text = text.strip()

    if len(text) < MIN_CONTENT_LENGTH:
        return ""

    return text
