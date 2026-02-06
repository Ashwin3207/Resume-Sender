import smtplib
from email.message import EmailMessage
import os
import csv
from dotenv import load_dotenv

# ===== Load environment variables =====
load_dotenv()

EMAIL = os.getenv("GMAIL_EMAIL")
APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

CSV_FILE = "hr_contacts.csv"

SUBJECT = ""

BODY_TEMPLATE = """To,

{title},
{company}

"""


def send_email(to_email, title, company):

    msg = EmailMessage()
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg["Subject"] = SUBJECT

    body = BODY_TEMPLATE.format(
        title=title,
        company=company
    )

    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL, APP_PASSWORD)
        server.send_message(msg)

    print(f"✅ Sent to {to_email}")


def send_bulk_emails():

    with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            email = row["Email"]
            title = row["Title"]
            company = row["Company"]

            try:
                send_email(email, title, company)
            except Exception as e:
                print(f"❌ Failed for {email} -> {e}")


if __name__ == "__main__":
    send_bulk_emails()
