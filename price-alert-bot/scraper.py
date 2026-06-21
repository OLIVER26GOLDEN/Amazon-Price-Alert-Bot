import requests
from bs4 import BeautifulSoup
import random
import time

HEADERS_LIST = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    },
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
]

PRICE_SELECTORS = [
    {"class": "a-price-whole"},
    {"id": "priceblock_ourprice"},
    {"id": "priceblock_dealprice"},
    {"class": "a-offscreen"},
]

def get_price(url: str) -> float | None:
    try:
        time.sleep(random.uniform(1, 3))
        headers = random.choice(HEADERS_LIST)
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            print(f"Status {response.status_code} para {url}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        for selector in PRICE_SELECTORS:
            tag = soup.find("span", selector)
            if tag:
                text = tag.get_text()
                text = text.replace(".", "").replace(",", ".").strip()
                cleaned = ''.join(c for c in text if c.isdigit() or c == '.')
                if cleaned:
                    return float(cleaned)

        return None

    except Exception as e:
        print(f"Error scrapeando {url}: {e}")
        return None