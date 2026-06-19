# Week 28: Scheduling and Notifications

## Overview
This week covers scheduling Python scripts to run automatically and sending email notifications.

---

## Part 1: Scheduling with Cron (Linux/Mac)

### Cron Syntax

```
* * * * * command
│ │ │ │ │
│ │ │ │ └── Day of week (0-7, Sun=0 or 7)
│ │ │ └──── Month (1-12)
│ │ └────── Day of month (1-31)
│ └──────── Hour (0-23)
└────────── Minute (0-59)
```

### Common Examples

```bash
# Every minute
* * * * * /usr/bin/python3 /path/to/script.py

# Every hour
0 * * * * /usr/bin/python3 /path/to/script.py

# Every day at midnight
0 0 * * * /usr/bin/python3 /path/to/script.py

# Every Monday at 9 AM
0 9 * * 1 /usr/bin/python3 /path/to/script.py

# Every 5 minutes
*/5 * * * * /usr/bin/python3 /path/to/script.py

# First day of every month
0 0 1 * * /usr/bin/python3 /path/to/script.py
```

### Managing Cron Jobs

```bash
# Edit crontab
crontab -e

# List cron jobs
crontab -l

# Remove all cron jobs
crontab -r
```

### Cron with Virtual Environment

```bash
# Use full paths
0 * * * * /home/user/venv/bin/python /home/user/script.py

# Or activate venv
0 * * * * cd /home/user/project && source venv/bin/activate && python script.py
```

---

## Part 2: Scheduling with schedule Library

### Installation

```bash
pip install schedule
```

### Basic Usage

```python
import schedule
import time

def job():
    print("Job running...")

# Schedule jobs
schedule.every(10).seconds.do(job)
schedule.every(5).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
schedule.every().monday.do(job)
schedule.every().wednesday.at("13:15").do(job)

# Run scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
```

### Advanced Usage

```python
import schedule
import time
from datetime import datetime

def job_with_args(name):
    print(f"Running job for {name}")

def job_that_may_fail():
    try:
        # Do something
        pass
    except Exception as e:
        print(f"Job failed: {e}")

# Pass arguments
schedule.every().day.do(job_with_args, name="daily_report")

# Run once then cancel
def run_once():
    print("This runs once")
    return schedule.CancelJob

schedule.every().day.at("00:00").do(run_once)

# Clear all jobs
schedule.clear()

# Tag jobs
schedule.every().day.do(job).tag("daily", "reports")
schedule.clear("daily")  # Clear jobs with tag
```

---

## Part 3: Sending Email with smtplib

### Basic Email

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email, subject, body):
    # Email configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "your_email@gmail.com"
    password = "your_app_password"  # Use app password, not regular password

    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(message)

    print(f"Email sent to {to_email}")

send_email("recipient@example.com", "Test Subject", "This is the email body.")
```

### HTML Email with Attachments

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

def send_html_email(to_email, subject, html_content, attachments=None):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "your_email@gmail.com"
    password = "your_app_password"

    message = MIMEMultipart("alternative")
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject

    # HTML content
    html_part = MIMEText(html_content, "html")
    message.attach(html_part)

    # Attachments
    if attachments:
        for filepath in attachments:
            path = Path(filepath)
            with open(path, "rb") as f:
                attachment = MIMEBase("application", "octet-stream")
                attachment.set_payload(f.read())
            encoders.encode_base64(attachment)
            attachment.add_header(
                "Content-Disposition",
                f"attachment; filename={path.name}"
            )
            message.attach(attachment)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(message)

# Usage
html = """
<html>
<body>
    <h1>Report</h1>
    <p>This is the <strong>daily report</strong>.</p>
    <table border="1">
        <tr><th>Metric</th><th>Value</th></tr>
        <tr><td>Sales</td><td>$10,000</td></tr>
    </table>
</body>
</html>
"""
send_html_email("recipient@example.com", "Daily Report", html, ["report.pdf"])
```

---

## Part 4: Logging

```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
def setup_logging(log_file="app.log"):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1024*1024,  # 1MB
        backupCount=5
    )
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    ))

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    ))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Usage
logger = setup_logging()
logger.info("Application started")
logger.warning("Something might be wrong")
logger.error("An error occurred")
```

---

## Part 5: Environment Variables

```python
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get variables
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
```

`.env` file:
```
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
```

---

## Week 28 Project: Daily Report Scheduler

```python
#!/usr/bin/env python3
"""
Daily Report Automation
Generates and emails daily reports on schedule.
"""

import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from pathlib import Path
import logging
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("scheduler.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ReportGenerator:
    """Generate reports."""

    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    def generate_daily_report(self):
        """Generate daily summary report."""
        today = datetime.now()

        # Simulate gathering data
        report_data = {
            "date": today.strftime("%Y-%m-%d"),
            "generated_at": today.isoformat(),
            "metrics": {
                "total_users": 1234,
                "active_users": 567,
                "new_signups": 23,
                "revenue": 45678.90
            },
            "alerts": [
                {"level": "info", "message": "Daily backup completed"},
                {"level": "warning", "message": "Disk usage at 75%"}
            ]
        }

        # Save JSON
        json_file = self.data_dir / f"report_{today.strftime('%Y%m%d')}.json"
        with open(json_file, "w") as f:
            json.dump(report_data, f, indent=2)

        # Generate HTML
        html = self._generate_html(report_data)

        return html, json_file

    def _generate_html(self, data):
        """Generate HTML report."""
        alerts_html = ""
        for alert in data["alerts"]:
            color = "green" if alert["level"] == "info" else "orange"
            alerts_html += f'<p style="color:{color}">• {alert["message"]}</p>'

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #4CAF50; color: white; }}
                .alerts {{ background-color: #f9f9f9; padding: 15px; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h1>Daily Report - {data['date']}</h1>

            <h2>Key Metrics</h2>
            <table>
                <tr><th>Metric</th><th>Value</th></tr>
                <tr><td>Total Users</td><td>{data['metrics']['total_users']:,}</td></tr>
                <tr><td>Active Users</td><td>{data['metrics']['active_users']:,}</td></tr>
                <tr><td>New Signups</td><td>{data['metrics']['new_signups']:,}</td></tr>
                <tr><td>Revenue</td><td>${data['metrics']['revenue']:,.2f}</td></tr>
            </table>

            <h2>Alerts</h2>
            <div class="alerts">
                {alerts_html}
            </div>

            <p><small>Generated at {data['generated_at']}</small></p>
        </body>
        </html>
        """

class EmailSender:
    """Send emails."""

    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("EMAIL_USER")
        self.password = os.getenv("EMAIL_PASSWORD")

    def send(self, to_email, subject, html_content, attachments=None):
        """Send email with optional attachments."""
        if not self.sender_email or not self.password:
            logger.error("Email credentials not configured")
            return False

        try:
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = to_email
            message["Subject"] = subject

            message.attach(MIMEText(html_content, "html"))

            if attachments:
                for filepath in attachments:
                    self._attach_file(message, filepath)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.send_message(message)

            logger.info(f"Email sent to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False

    def _attach_file(self, message, filepath):
        """Attach file to email."""
        path = Path(filepath)
        with open(path, "rb") as f:
            attachment = MIMEBase("application", "octet-stream")
            attachment.set_payload(f.read())
        encoders.encode_base64(attachment)
        attachment.add_header(
            "Content-Disposition",
            f"attachment; filename={path.name}"
        )
        message.attach(attachment)

class DailyReportJob:
    """Daily report job."""

    def __init__(self, recipients):
        self.recipients = recipients
        self.generator = ReportGenerator()
        self.emailer = EmailSender()

    def run(self):
        """Generate and send daily report."""
        logger.info("Starting daily report job...")

        try:
            html, json_file = self.generator.generate_daily_report()

            today = datetime.now().strftime("%Y-%m-%d")
            subject = f"Daily Report - {today}"

            for recipient in self.recipients:
                self.emailer.send(
                    recipient,
                    subject,
                    html,
                    attachments=[json_file]
                )

            logger.info("Daily report job completed successfully")

        except Exception as e:
            logger.error(f"Daily report job failed: {e}")

def main():
    """Main scheduler."""
    recipients = os.getenv("REPORT_RECIPIENTS", "").split(",")

    if not recipients or recipients == [""]:
        logger.warning("No recipients configured. Set REPORT_RECIPIENTS env var.")
        recipients = ["test@example.com"]

    job = DailyReportJob(recipients)

    # Schedule daily at 8 AM
    schedule.every().day.at("08:00").do(job.run)

    # Also run immediately for testing
    logger.info("Running initial report...")
    job.run()

    logger.info("Scheduler started. Press Ctrl+C to stop.")

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
```

`.env` file:
```
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
REPORT_RECIPIENTS=recipient1@example.com,recipient2@example.com
```

---

## Key Takeaways

1. **Cron** for system-level scheduling
2. **schedule** library for Python-based scheduling
3. Use **smtplib** for sending emails
4. Store credentials in **environment variables**
5. **Logging** is essential for scheduled tasks
6. Handle **errors gracefully** in automated jobs
7. Use **app passwords** for Gmail
8. Test jobs **manually** before scheduling

---

## Next Week Preview
Weeks 29-30: Build a complete automation project.
