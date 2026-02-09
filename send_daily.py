import smtplib
from email.message import EmailMessage
import os
import csv
import time
import random
from dotenv import load_dotenv
from datetime import datetime

# ===== LOAD ENV =====
load_dotenv()

EMAIL = os.getenv("GMAIL_EMAIL")
APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

CSV_FILE = "hr_contacts.csv"
RESUME_FILE = "ashwin_2026.pdf"

SENT_LOG_FILE = "sent_log.csv"

DAILY_LIMIT = 5

SUBJECT = "Application – Software Engineer / Internship"

BODY_TEMPLATE = """Hi {name},

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

def send_email(to_email, name):

    msg = EmailMessage()
    msg["From"] = f"Ashwin Kumar Mathura <{EMAIL}>"
    msg["To"] = to_email
    msg["Subject"] = SUBJECT

    msg.set_content(BODY_TEMPLATE.format(
        name=name
    ))

    # Attach resume (use script dir to ensure correct path)
    resume_path = os.path.join(os.path.dirname(__file__), RESUME_FILE)
    with open(resume_path, "rb") as f:
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

    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, CSV_FILE)
    sent_log_path = os.path.join(base_dir, SENT_LOG_FILE)

    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    rows = ensure_sent_column(rows)

    # load already-sent emails from sent_log (best-effort)
    sent_emails = set()
    if os.path.exists(sent_log_path):
        try:
            with open(sent_log_path, newline="", encoding="utf-8") as sf:
                reader = csv.DictReader(sf)
                for r in reader:
                    e = r.get("Email") or r.get("email")
                    status = r.get("Status") or r.get("status")
                    if e and status and status.lower().startswith("sent"):
                        sent_emails.add(e.strip().lower())
        except Exception:
            pass

    sent_today = 0

    for row in rows:

        if sent_today >= DAILY_LIMIT:
            break

        email = (row.get("Email") or "").strip()

        if row.get("Sent", "").upper() == "YES":
            continue

        if email and email.lower() in sent_emails:
            continue

        name = row.get("Name", "")

        try:
            send_email(email, name)

            print(f"✅ Sent to {name} ({email})")

            row["Sent"] = "YES"
            sent_today += 1

            # record to sent log immediately
            try:
                log_exists = os.path.exists(sent_log_path)
                with open(sent_log_path, "a", newline="", encoding="utf-8") as lf:
                    fieldnames = ["Name", "Company", "Email", "Status", "Time"]
                    lw = csv.DictWriter(lf, fieldnames=fieldnames)
                    if not log_exists:
                        lw.writeheader()
                    lw.writerow({
                        "Name": name,
                        "Company": row.get("Company", ""),
                        "Email": email,
                        "Status": "Sent",
                        "Time": datetime.now().isoformat()
                    })
                    sent_emails.add(email.lower())
            except Exception:
                pass

            # spam-safe delay
            time.sleep(random.randint(20, 40))

        except Exception as e:
            print(f"❌ Failed for {email} -> {e}")

    # Save updated CSV
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n📬 Sent today: {sent_today}")


if __name__ == "__main__":
    send_daily_emails()
