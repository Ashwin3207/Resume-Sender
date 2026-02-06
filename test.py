import smtplib
from email.message import EmailMessage
import os
import csv
from dotenv import load_dotenv
import time

# ===== Load environment variables =====
load_dotenv()

EMAIL = os.getenv("GMAIL_EMAIL")
APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

CSV_FILE = "hr_contacts.csv"

SUBJECT = "Invitation for Campus Placement Drive at Government Engineering College Munger"

HTML_BODY_TEMPLATE = """
<html>
<body style="font-family: Arial, sans-serif; line-height:1.6;">

<p><b>To,</b><br>
<b>{title},</b><br>
<b>{company}</b></p>

<p>
The Government Engineering College Munger, added to the Bihar Engineering University brotherhood in 2019, has grown enormously during the last six years.
</p>

<p>
The institute offers B.Tech programmes in Computer Science & Engineering (Artificial Intelligence & Data Science), Mechanical Engineering, Civil Engineering, and Electrical Engineering.
</p>

<p>
The Training and Placement Cell is glad to invite your esteemed organization for campus recruitment of students graduating in May 2026.
</p>

<p>
Our students possess strong technical knowledge, creativity, discipline, and professional ethics.
</p>

<p>
Kindly acknowledge this invitation and let us know your hiring requirements. We would be happy to arrange online interviews, campus visits, and provide student profiles.
</p>

<p>
Looking forward to your positive response.
</p>

<p>
Yours sincerely,<br><br>

Mr. Abhishek Anand<br>
Professor In-Charge<br>
Training & Placement Cell<br>
GEC Munger<br><br>

📞 +91-9304466728<br>
📧 tpogecmunger@gmail.com<br>
🌐 https://gecmunger.org
</p>

</body>
</html>
"""


def send_email(to_email, title, company):

    msg = EmailMessage()
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg["Subject"] = SUBJECT

    html_body = HTML_BODY_TEMPLATE.format(
        title=title,
        company=company
    )

    msg.add_alternative(html_body, subtype="html")

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
                time.sleep(2)   # prevent Gmail rate limit
            except Exception as e:
                print(f"❌ Failed for {email} -> {e}")


if __name__ == "__main__":
    send_bulk_emails()
