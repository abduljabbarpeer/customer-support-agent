"""
The FAQ tool.

The agent can call get_faq_answers() to read DemoKart's FAQ Google Sheet.
"""

import csv
import io
import os
import re

import requests
from dotenv import load_dotenv

# Read the settings in the .env file (FAQ_SHEET_URL is the Sheet's normal link).
load_dotenv()


def get_faq_answers() -> dict:
    """Get all of DemoKart's frequently asked questions and their answers.

    Call this before answering any question about DemoKart's business, such as
    delivery, returns, payments or how things work.

    Returns:
        A dictionary with "status" ("ok" or "error") and, when ok, a "faqs" list
        where each item has a "question" and an "answer".
    """
    # 1. Get the Sheet's normal link from the settings.
    url = os.environ.get("FAQ_SHEET_URL", "").strip()
    if not url:
        return {"status": "error", "message": "The FAQ Sheet link is not set."}

    # 2. Work out the CSV download link from the normal link.
    #    Normal link: https://docs.google.com/spreadsheets/d/<ID>/edit#gid=<TAB>
    sheet_id = re.search(r"/spreadsheets/d/([A-Za-z0-9_-]+)", url)
    if not sheet_id:
        return {"status": "error", "message": "The FAQ Sheet link looks wrong."}
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id.group(1)}/export?format=csv"
    # If the link points to a specific tab, keep that tab.
    tab = re.search(r"gid=(\d+)", url)
    if tab:
        csv_url += f"&gid={tab.group(1)}"

    # 3. Download the Sheet as CSV.
    try:
        response = requests.get(csv_url, timeout=15)
        response.raise_for_status()
    except requests.RequestException:
        return {"status": "error", "message": "Could not download the FAQ Sheet."}

    # 4. Read the rows. The first row has the column names (question, answer).
    text = response.content.decode("utf-8-sig")
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows or not rows[0]:
        return {"status": "error", "message": "The FAQ Sheet is empty."}
    columns = list(rows[0].keys())

    # Use the columns called "question" and "answer"; if not found, use the first two.
    def pick(word, fallback_index):
        for name in columns:
            if name and word in name.lower():
                return name
        return columns[fallback_index] if len(columns) > fallback_index else None

    q_col, a_col = pick("question", 0), pick("answer", 1)
    faqs = [
        {"question": (row.get(q_col) or "").strip(), "answer": (row.get(a_col) or "").strip()}
        for row in rows
        if (row.get(q_col) or "").strip()
    ]
    return {"status": "ok", "faqs": faqs}
