# Weeks 29-30: Automation Project

## Overview
Over these two weeks, build a complete automation tool for a real task you do repeatedly.

---

## Project Ideas

1. **File Backup System**: Automated backups with compression and cloud sync
2. **Data Pipeline**: Scrape, process, and report on data daily
3. **System Monitor**: Track disk space, CPU, memory with alerts
4. **Social Media Bot**: Post content on schedule
5. **Invoice Generator**: Create PDFs from data
6. **Website Monitor**: Check uptime and get notified of issues

---

## Example Project: Website Monitor

```python
#!/usr/bin/env python3
"""
Website Uptime Monitor
Monitors websites and sends alerts when they go down.
"""

import requests
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import json
from pathlib import Path
import logging
from dataclasses import dataclass
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("monitor.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class Website:
    """Website to monitor."""
    name: str
    url: str
    expected_status: int = 200
    timeout: int = 30

@dataclass
class CheckResult:
    """Result of a website check."""
    website: Website
    is_up: bool
    status_code: Optional[int]
    response_time: Optional[float]
    error: Optional[str]
    timestamp: datetime

class Monitor:
    """Website monitor."""

    def __init__(self, websites: List[Website]):
        self.websites = websites
        self.results_file = Path("monitor_results.json")
        self.last_status = {}
        self._load_last_status()

    def _load_last_status(self):
        """Load last known status."""
        if self.results_file.exists():
            with open(self.results_file) as f:
                self.last_status = json.load(f)

    def _save_status(self):
        """Save current status."""
        with open(self.results_file, "w") as f:
            json.dump(self.last_status, f, indent=2)

    def check_website(self, website: Website) -> CheckResult:
        """Check a single website."""
        try:
            start = time.time()
            response = requests.get(
                website.url,
                timeout=website.timeout,
                headers={"User-Agent": "UptimeMonitor/1.0"}
            )
            response_time = time.time() - start

            is_up = response.status_code == website.expected_status

            return CheckResult(
                website=website,
                is_up=is_up,
                status_code=response.status_code,
                response_time=response_time,
                error=None,
                timestamp=datetime.now()
            )

        except requests.exceptions.Timeout:
            return CheckResult(
                website=website,
                is_up=False,
                status_code=None,
                response_time=None,
                error="Timeout",
                timestamp=datetime.now()
            )
        except requests.exceptions.RequestException as e:
            return CheckResult(
                website=website,
                is_up=False,
                status_code=None,
                response_time=None,
                error=str(e),
                timestamp=datetime.now()
            )

    def check_all(self) -> List[CheckResult]:
        """Check all websites."""
        results = []
        for website in self.websites:
            result = self.check_website(website)
            results.append(result)

            status = "UP" if result.is_up else "DOWN"
            if result.response_time:
                logger.info(f"{website.name}: {status} ({result.response_time:.2f}s)")
            else:
                logger.info(f"{website.name}: {status} ({result.error})")

        return results

    def get_status_changes(self, results: List[CheckResult]) -> List[CheckResult]:
        """Find websites that changed status."""
        changes = []

        for result in results:
            name = result.website.name
            current = "up" if result.is_up else "down"
            previous = self.last_status.get(name)

            if previous is not None and previous != current:
                changes.append(result)

            self.last_status[name] = current

        self._save_status()
        return changes

class Alerter:
    """Send alerts."""

    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("EMAIL_USER")
        self.password = os.getenv("EMAIL_PASSWORD")
        self.recipients = os.getenv("ALERT_RECIPIENTS", "").split(",")

    def send_alert(self, result: CheckResult):
        """Send alert for status change."""
        status = "UP" if result.is_up else "DOWN"
        emoji = "✅" if result.is_up else "❌"

        subject = f"{emoji} {result.website.name} is {status}"

        body = f"""
        <html>
        <body>
        <h2>Website Status Alert</h2>
        <p><strong>Website:</strong> {result.website.name}</p>
        <p><strong>URL:</strong> {result.website.url}</p>
        <p><strong>Status:</strong> {status}</p>
        <p><strong>Time:</strong> {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>
        """

        if result.is_up:
            body += f"<p><strong>Response Time:</strong> {result.response_time:.2f}s</p>"
        else:
            body += f"<p><strong>Error:</strong> {result.error or f'Status {result.status_code}'}</p>"

        body += """
        </body>
        </html>
        """

        self._send_email(subject, body)

    def send_daily_report(self, results: List[CheckResult]):
        """Send daily summary report."""
        up_count = sum(1 for r in results if r.is_up)
        down_count = len(results) - up_count

        subject = f"Daily Monitor Report: {up_count}/{len(results)} sites up"

        rows = ""
        for result in results:
            status = "✅ UP" if result.is_up else "❌ DOWN"
            time_str = f"{result.response_time:.2f}s" if result.response_time else "N/A"
            rows += f"""
            <tr>
                <td>{result.website.name}</td>
                <td>{status}</td>
                <td>{time_str}</td>
            </tr>
            """

        body = f"""
        <html>
        <body>
        <h2>Daily Uptime Report</h2>
        <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d')}</p>
        <p><strong>Summary:</strong> {up_count} up, {down_count} down</p>

        <table border="1" cellpadding="10">
            <tr>
                <th>Website</th>
                <th>Status</th>
                <th>Response Time</th>
            </tr>
            {rows}
        </table>
        </body>
        </html>
        """

        self._send_email(subject, body)

    def _send_email(self, subject, body):
        """Send email."""
        if not self.sender_email or not self.password:
            logger.warning("Email not configured")
            return

        try:
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = ", ".join(self.recipients)
            message["Subject"] = subject
            message.attach(MIMEText(body, "html"))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.send_message(message)

            logger.info(f"Alert sent: {subject}")

        except Exception as e:
            logger.error(f"Failed to send email: {e}")

class UptimeMonitor:
    """Main application."""

    def __init__(self, config_file: str = "config.json"):
        self.config = self._load_config(config_file)
        self.websites = [
            Website(**site) for site in self.config.get("websites", [])
        ]
        self.monitor = Monitor(self.websites)
        self.alerter = Alerter()

    def _load_config(self, config_file: str) -> dict:
        """Load configuration."""
        path = Path(config_file)
        if path.exists():
            with open(path) as f:
                return json.load(f)
        return {"websites": [], "check_interval": 5}

    def check_and_alert(self):
        """Run check and send alerts for changes."""
        logger.info("Running check...")
        results = self.monitor.check_all()

        changes = self.monitor.get_status_changes(results)
        for result in changes:
            status = "UP" if result.is_up else "DOWN"
            logger.warning(f"Status change: {result.website.name} is now {status}")
            self.alerter.send_alert(result)

    def daily_report(self):
        """Send daily summary."""
        logger.info("Generating daily report...")
        results = self.monitor.check_all()
        self.alerter.send_daily_report(results)

    def run(self):
        """Run the monitor."""
        interval = self.config.get("check_interval", 5)

        # Schedule checks
        schedule.every(interval).minutes.do(self.check_and_alert)
        schedule.every().day.at("09:00").do(self.daily_report)

        # Initial check
        self.check_and_alert()

        logger.info(f"Monitor started. Checking every {interval} minutes.")

        while True:
            schedule.run_pending()
            time.sleep(10)

def create_sample_config():
    """Create sample configuration."""
    config = {
        "websites": [
            {"name": "Google", "url": "https://www.google.com"},
            {"name": "GitHub", "url": "https://github.com"},
            {"name": "Your Site", "url": "https://example.com"}
        ],
        "check_interval": 5
    }

    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)

    print("Sample config.json created")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--init":
        create_sample_config()
    else:
        monitor = UptimeMonitor()
        monitor.run()
```

---

## Project Checklist

### Week 29: Core Functionality
- [ ] Define project requirements
- [ ] Set up project structure
- [ ] Implement core functionality
- [ ] Add configuration file support
- [ ] Add logging

### Week 30: Polish and Deploy
- [ ] Add error handling
- [ ] Implement notifications
- [ ] Add scheduling
- [ ] Write documentation
- [ ] Create installation script
- [ ] Test thoroughly
- [ ] Deploy and monitor

---

## Key Takeaways

1. **Plan before coding** - define requirements
2. **Use configuration files** for flexibility
3. **Log everything** for debugging
4. **Handle errors** gracefully
5. **Test thoroughly** before deploying
6. **Document** your code
7. **Monitor** automated tasks
8. **Start simple**, add features iteratively

---

## Next Week Preview
Week 31 begins the Capstone Phase with code quality practices.
