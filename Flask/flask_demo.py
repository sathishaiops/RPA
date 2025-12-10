"""
Flask API that opens a URL using Playwright, extracts visible text,
and returns/saves the output.
"""

from flask import Flask, jsonify
from playwright.sync_api import sync_playwright
import time
import os
from flask import request

app = Flask(__name__)

URL = "https://www.snowflake.com/resource/generative-ai-and-llms-for-dummies/?utm_source=google&utm_medium=paidsearch&utm_campaign=em-ae-en-nb-genaigeneral-exact&utm_content=go-rsa-evg-eb-generative-ai-and-llms-for-dummies&utm_term=c-g-genai-e-704466044095&gad_source=1&gad_campaignid=21434137834&gbraid=0AAAAADCzRJUsm97bQgUPCSVtjrwn10OWQ&gclid=Cj0KCQiArt_JBhCTARIsADQZaymxeefJ0-0tpRCjkYLyNe_KbiFCLP1XGHC5jTB9Cl7d8nBE50fB9PoaAvAaEALw_wcB"


def extract_page_text(headless=True):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()

        page.goto(URL, wait_until="networkidle")
        time.sleep(2)

        page_text = page.inner_text("body")

        # Save to file
        output_path = os.path.join(os.getcwd(), "output.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(page_text)

        context.close()
        browser.close()

        return page_text, output_path


@app.route("/extract", methods=["GET"])
def extract():
    try:
        text, saved_path = extract_page_text(headless=True)
        return jsonify({
            "status": "success",
            "message": "Page extracted successfully",
            "saved_to": saved_path,
            "text_preview": text[:500]  # prevent huge response
        })
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500
@app.route("/add", methods=["POST"])
def add():
    data = request.get_json()
    a = data.get("a")
    b = data.get("b")
    return jsonify({
        "operation": "addition",
        "a": a,
        "b": b,
        "result": a + b
    })


@app.route("/subtract", methods=["POST"])
def subtract():
    data = request.get_json()
    a = data.get("a")
    b = data.get("b")
    return jsonify({
        "operation": "subtraction",
        "a": a,
        "b": b,
        "result": a - b
    })


@app.route("/multiply", methods=["POST"])
def multiply():
    data = request.get_json()
    a = data.get("a")
    b = data.get("b")
    return jsonify({
        "operation": "multiplication",
        "a": a,
        "b": b,
        "result": a * b
    })


@app.route("/divide", methods=["POST"])
def divide():
    data = request.get_json()
    a = data.get("a")
    b = data.get("b")

    if b == 0:
        return jsonify({
            "operation": "division",
            "error": "Cannot divide by zero"
        }), 400

    return jsonify({
        "operation": "division",
        "a": a,
        "b": b,
        "result": a / b
    })    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
