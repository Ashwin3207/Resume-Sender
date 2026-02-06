import smtplib
from email.message import EmailMessage
import os
import csv
import time
import random
from dotenv import load_dotenv

# ===== LOAD ENV =====
load_dotenv()

EMAIL = os.getenv("GMAIL_EMAIL")
APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

CSV_FILE = "hr_contacts.csv"
RESUME_FILE = "ashwin_2026.pdf"

DAILY_LIMIT = 5

SUBJECT = "Application – Software Engineer / Internship"

BODY_TEMPLATE = """To,

{title},
{company}

Respected Sir/Madam,

I am a Computer Science Engineering student with hands-on experience through government internship, research work, and delivering real-world projects for startups and platforms.

I have built full-stack web applications and machine learning solutions, including a MERN-based news platform, an audio streaming platform, and a healthcare ML system.

Please find my resume attached for your kind consideration.

Regards,  
Ashwin Kumar Mathura
"""


# -------- Ensure Sent column exists --------

def ensure_sent_column(rows):
    if "Sent" not in rows[0]:
        for row in rows:
            row["Sent"] = "NO"
    return rows


# -------- Send email --------

def send_email(to_email, title, company):

    msg = EmailMessage()
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg["Subject"] = SUBJECT

    msg.set_content(BODY_TEMPLATE.format(
        title=title,
        company=company
    ))

    with open(RESUME_FILE, "rb") as f:
        resume_data = f.read()

    msg.add_attachment(
        resume_data,
        maintype="application",
        subtype="pdf",
        filename="Ashwin_Kumar_Mathura_Resume.pdf"
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL, APP_PASSWORD)
        server.send_message(msg)


# -------- Daily batch sender --------

def send_daily_emails():

    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    rows = ensure_sent_column(rows)

    sent_today = 0

    for row in rows:

        if sent_today >= DAILY_LIMIT:
            break

        if row["Sent"].upper() == "YES":
            continue

        email = row["Email"]
        title = row["Title"]
        company = row["Company"]

        try:
            send_email(email, title, company)

            print(f"✅ Sent to {email}")

            row["Sent"] = "YES"
            sent_today += 1

            time.sleep(random.randint(20, 40))  # spam-safe delay

        except Exception as e:
            print(f"❌ Failed for {email} -> {e}")

    # Write CSV back with Sent column
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n📬 Sent today: {sent_today}")


if __name__ == "__main__":
    send_daily_emails()
