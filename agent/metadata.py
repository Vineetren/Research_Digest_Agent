from bs4 import BeautifulSoup
from typing import Optional


def extract_title(raw_html: str) -> Optional[str]:
    """
    Extracts title from HTML.
    Priority:
    1. <title> tag
    2. First <h1>
    3. None
    """
    try:
        soup = BeautifulSoup(raw_html, "html.parser")

        # 1. Try <title>
        if soup.title and soup.title.string:
            return soup.title.string.strip()

        # 2. Try first <h1>
        h1 = soup.find("h1")
        if h1:
            return h1.get_text(strip=True)

    except Exception:
        return None

    return None
