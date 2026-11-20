"""
Support tickets.

When the agent hands a customer over to a person, it saves a ticket here.
Tickets are rows in a file called tickets.csv in the project folder.
Only Python's built-in modules are used.
"""

import csv
from datetime import datetime
from pathlib import Path

# tickets.csv sits in the project folder (one level above this support_agent folder).
TICKETS_FILE = Path(__file__).resolve().parent.parent / "tickets.csv"

# The columns of the file, in order.
HEADER = ["ticket_id", "date_time", "name", "contact", "order_id", "reason", "summary"]


def _next_ticket_id() -> str:
    """Look at the last ticket in the file and return the next ID (T-1001 for the first one)."""
    last_number = 1000
    if TICKETS_FILE.exists():
        with open(TICKETS_FILE, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                try:
                    last_number = int(row["ticket_id"].split("-")[1])
                except (KeyError, ValueError, IndexError):
                    pass  # skip a row we can't read
    return f"T-{last_number + 1}"


def create_ticket(name: str, contact: str, reason: str, summary: str, order_id: str = "") -> dict:
    """Saves a support ticket when the customer is handed over to a person.

    Call this only after the customer has given their name and a contact (phone or email).

    Args:
        name: The customer's name.
        contact: The customer's phone number or email.
        reason: Why we are handing over. One of: "no answer", "refund", "angry customer", "asked for a person".
        summary: A one-line summary of the customer's problem.
        order_id: The order ID, if the customer gave one. Leave empty if not.

    Returns:
        A dictionary with the ticket_id of the new ticket.
    """
    ticket_id = _next_ticket_id()
    is_new_file = not TICKETS_FILE.exists()

    with open(TICKETS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new_file:
            writer.writerow(HEADER)  # header row only when the file is new
        writer.writerow([
            ticket_id,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            name,
            contact,
            order_id,
            reason,
            summary,
        ])

    return {"status": "success", "ticket_id": ticket_id}
