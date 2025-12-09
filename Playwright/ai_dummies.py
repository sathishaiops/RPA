"""
extract_page_to_file.py
Opens a URL in Playwright, extracts the visible text, and saves it to output.txt.
"""

from playwright.sync_api import sync_playwright
import time
import os

URL = "https://www.snowflake.com/resource/generative-ai-and-llms-for-dummies/?utm_source=google&utm_medium=paidsearch&utm_campaign=em-ae-en-nb-genaigeneral-exact&utm_content=go-rsa-evg-eb-generative-ai-and-llms-for-dummies&utm_term=c-g-genai-e-704466044095&gad_source=1&gad_campaignid=21434137834&gbraid=0AAAAADCzRJUsm97bQgUPCSVtjrwn10OWQ&gclid=Cj0KCQiArt_JBhCTARIsADQZaymxeefJ0-0tpRCjkYLyNe_KbiFCLP1XGHC5jTB9Cl7d8nBE50fB9PoaAvAaEALw_wcB"


def main(headless=False):
    with sync_playwright() as p:
        # launch browser
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()

        print(f"Opening URL: {URL}")
        page.goto(URL, wait_until="networkidle")
        time.sleep(2)  # allow lazy-loaded elements to appear

        # Extract full visible text of page
        page_text = page.inner_text("body")

        # Save to file in same path
        output_path = os.path.join(os.getcwd(), "output.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(page_text)

        print(f"\nSaved extracted text to: {output_path}")

        # cleanup
        context.close()
        browser.close()


if __name__ == "__main__":
    main(headless=False)  # set True to hide browser
