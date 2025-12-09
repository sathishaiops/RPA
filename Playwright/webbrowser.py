"""
sa_vs_ind_bing_news.py
Fully automated news scraper using Bing News (no CAPTCHAs).

Requirements:
pip install playwright
python -m playwright install
"""

from playwright.sync_api import sync_playwright
from urllib.parse import quote
import time
import json

QUERY = "SA vs ind update"
MAX_ITEMS = 10  # number of news items to collect


def extract_from_bing_news(page):
    """
    Extract news items from Bing News search results.
    Returns a list of dicts.
    """
    results = []

    # Bing news card selector
    cards = page.query_selector_all("div.news-card, div.t_s, div.card")
    
    # Fallback: any headline link on the page
    if not cards:
        cards = page.query_selector_all("a.title, article")

    for card in cards[:MAX_ITEMS]:
        try:
            # Clickable title link
            a = card.query_selector("a")  
            title = a.inner_text().strip() if a else ""

            link = a.get_attribute("href") if a else ""

            # Source + time meta
            source = ""
            time_text = ""
            snippet = ""

            meta = card.query_selector("div.source, span.source, div.caption, cite")
            if meta:
                meta_text = meta.inner_text().strip()
                source = meta_text

            time_el = card.query_selector("span.time, span.timestamp, div.time")
            if time_el:
                time_text = time_el.inner_text().strip()

            # Snippet / description
            snippet_el = card.query_selector("div.snippet, p, .snippet")
            if snippet_el:
                snippet = snippet_el.inner_text().strip()

            results.append({
                "title": title,
                "source": source,
                "time": time_text,
                "snippet": snippet,
                "link": link
            })

        except:
            continue

    return results


def main(headless=False):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()

        # === 1. Load Bing News page ===
        url = f"https://www.bing.com/news/search?q={quote(QUERY)}"
        print("Opening:", url)
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(1)

        # === 2. Extract news items ===
        news = extract_from_bing_news(page)

        if not news:
            print("No results found — selectors may need updating.")
        else:
            news = news[:MAX_ITEMS]
            print("\n=== Latest SA vs IND News (Bing) ===")
            for i, item in enumerate(news, 1):
                print(f"\n{i}. {item['title']}")
                print(f"   Source: {item['source']}")
                print(f"   Time: {item['time']}")
                print(f"   Snippet: {item['snippet']}")
                print(f"   Link: {item['link']}")

            # JSON output
            print("\n=== JSON Output ===")
            print(json.dumps(news, indent=2, ensure_ascii=False))

        context.close()
        browser.close()


if __name__ == "__main__":
    main(headless=False)
