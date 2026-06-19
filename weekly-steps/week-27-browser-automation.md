# Week 27: Browser Automation

## Overview
This week covers browser automation using Selenium and Playwright for interacting with dynamic web pages.

---

## Part 1: Selenium Setup

### Installation

```bash
pip install selenium webdriver-manager
```

### Basic Setup

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Auto-install and setup ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Navigate to page
driver.get("https://example.com")

# Get page info
print(driver.title)
print(driver.current_url)

# Close browser
driver.quit()
```

### Headless Mode

```python
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)
```

---

## Part 2: Finding Elements

```python
from selenium.webdriver.common.by import By

# By ID
element = driver.find_element(By.ID, "username")

# By class name
elements = driver.find_elements(By.CLASS_NAME, "item")

# By CSS selector
element = driver.find_element(By.CSS_SELECTOR, "div.container > p")

# By XPath
element = driver.find_element(By.XPATH, "//button[@type='submit']")

# By name
element = driver.find_element(By.NAME, "email")

# By tag name
elements = driver.find_elements(By.TAG_NAME, "a")

# By link text
element = driver.find_element(By.LINK_TEXT, "Click here")
element = driver.find_element(By.PARTIAL_LINK_TEXT, "Click")
```

---

## Part 3: Interacting with Elements

```python
from selenium.webdriver.common.keys import Keys

# Click
button = driver.find_element(By.ID, "submit")
button.click()

# Type text
input_field = driver.find_element(By.ID, "username")
input_field.clear()
input_field.send_keys("myusername")

# Special keys
input_field.send_keys(Keys.ENTER)
input_field.send_keys(Keys.TAB)
input_field.send_keys(Keys.CONTROL, "a")  # Select all

# Get text
text = element.text

# Get attribute
href = link.get_attribute("href")
value = input_field.get_attribute("value")

# Check state
is_displayed = element.is_displayed()
is_enabled = element.is_enabled()
is_selected = checkbox.is_selected()
```

---

## Part 4: Waiting

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Implicit wait (applies to all finds)
driver.implicitly_wait(10)

# Explicit wait
wait = WebDriverWait(driver, 10)

# Wait for element to be clickable
element = wait.until(EC.element_to_be_clickable((By.ID, "button")))

# Wait for element to be visible
element = wait.until(EC.visibility_of_element_located((By.ID, "content")))

# Wait for element to be present
element = wait.until(EC.presence_of_element_located((By.ID, "loading")))

# Wait for text
wait.until(EC.text_to_be_present_in_element((By.ID, "status"), "Complete"))

# Wait for URL to contain
wait.until(EC.url_contains("dashboard"))

# Custom condition
def check_complete(driver):
    element = driver.find_element(By.ID, "status")
    return "done" in element.text.lower()

wait.until(check_complete)
```

---

## Part 5: Forms and Dropdowns

```python
from selenium.webdriver.support.ui import Select

# Text input
name_input = driver.find_element(By.NAME, "name")
name_input.clear()
name_input.send_keys("John Doe")

# Checkbox
checkbox = driver.find_element(By.ID, "agree")
if not checkbox.is_selected():
    checkbox.click()

# Radio button
radio = driver.find_element(By.CSS_SELECTOR, "input[value='option1']")
radio.click()

# Dropdown (select element)
select = Select(driver.find_element(By.ID, "country"))
select.select_by_visible_text("United States")
select.select_by_value("us")
select.select_by_index(0)

# File upload
file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
file_input.send_keys("/path/to/file.pdf")

# Submit form
form = driver.find_element(By.TAG_NAME, "form")
form.submit()
```

---

## Part 6: JavaScript Execution

```python
# Execute JavaScript
driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

# Scroll to element
element = driver.find_element(By.ID, "footer")
driver.execute_script("arguments[0].scrollIntoView();", element)

# Click via JavaScript (for hidden/obscured elements)
driver.execute_script("arguments[0].click();", element)

# Get return value
result = driver.execute_script("return document.title")

# Set value via JavaScript
driver.execute_script("arguments[0].value = 'new value';", input_field)
```

---

## Part 7: Screenshots and Actions

```python
from selenium.webdriver.common.action_chains import ActionChains

# Take screenshot
driver.save_screenshot("screenshot.png")

# Element screenshot
element.screenshot("element.png")

# Action chains
actions = ActionChains(driver)

# Hover
actions.move_to_element(element).perform()

# Double click
actions.double_click(element).perform()

# Right click
actions.context_click(element).perform()

# Drag and drop
actions.drag_and_drop(source, target).perform()

# Chain actions
actions.move_to_element(menu).click(submenu).perform()
```

---

## Part 8: Playwright Alternative

### Installation

```bash
pip install playwright
playwright install
```

### Basic Usage

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://example.com")
    print(page.title())

    # Click
    page.click("button#submit")

    # Type
    page.fill("input#username", "myuser")

    # Wait for element
    page.wait_for_selector("div.content")

    # Screenshot
    page.screenshot(path="screenshot.png")

    browser.close()
```

### Async Playwright

```python
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://example.com")
        print(await page.title())
        await browser.close()

asyncio.run(main())
```

---

## Week 27 Project: Web Form Automator

```python
#!/usr/bin/env python3
"""
Web Form Automation Script
Automates filling and submitting web forms.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FormAutomator:
    """Automate web form interactions."""

    def __init__(self, headless=False):
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def navigate(self, url):
        """Navigate to URL."""
        logger.info(f"Navigating to {url}")
        self.driver.get(url)
        time.sleep(1)

    def fill_text(self, selector, text, by=By.CSS_SELECTOR):
        """Fill a text input."""
        element = self.wait.until(EC.element_to_be_clickable((by, selector)))
        element.clear()
        element.send_keys(text)
        logger.info(f"Filled '{selector}' with '{text}'")

    def click(self, selector, by=By.CSS_SELECTOR):
        """Click an element."""
        element = self.wait.until(EC.element_to_be_clickable((by, selector)))
        element.click()
        logger.info(f"Clicked '{selector}'")

    def select_dropdown(self, selector, value, by=By.CSS_SELECTOR):
        """Select dropdown option."""
        element = self.wait.until(EC.presence_of_element_located((by, selector)))
        select = Select(element)
        select.select_by_visible_text(value)
        logger.info(f"Selected '{value}' in '{selector}'")

    def check_checkbox(self, selector, check=True, by=By.CSS_SELECTOR):
        """Check or uncheck a checkbox."""
        element = self.wait.until(EC.element_to_be_clickable((by, selector)))
        if element.is_selected() != check:
            element.click()
        logger.info(f"Checkbox '{selector}' set to {check}")

    def wait_for_element(self, selector, by=By.CSS_SELECTOR, timeout=10):
        """Wait for element to be visible."""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, selector))
        )

    def get_text(self, selector, by=By.CSS_SELECTOR):
        """Get element text."""
        element = self.wait.until(EC.presence_of_element_located((by, selector)))
        return element.text

    def screenshot(self, filename):
        """Take screenshot."""
        self.driver.save_screenshot(filename)
        logger.info(f"Screenshot saved: {filename}")

    def close(self):
        """Close browser."""
        self.driver.quit()
        logger.info("Browser closed")

def demo_form_fill():
    """Demo: Fill a practice form."""
    automator = FormAutomator(headless=False)

    try:
        # Navigate to a demo form site
        automator.navigate("https://www.selenium.dev/selenium/web/web-form.html")

        # Fill text inputs
        automator.fill_text("input#my-text-id", "Hello Selenium")
        automator.fill_text("input[name='my-password']", "secret123")
        automator.fill_text("textarea[name='my-textarea']", "This is a test message")

        # Select dropdown
        automator.select_dropdown("select[name='my-select']", "Two")

        # Check checkbox
        automator.check_checkbox("input#my-check-1", True)

        # Screenshot before submit
        automator.screenshot("form_filled.png")

        # Submit
        automator.click("button[type='submit']")

        # Wait and verify
        time.sleep(2)
        automator.screenshot("form_submitted.png")

        logger.info("Form automation complete!")

    finally:
        time.sleep(2)
        automator.close()

def automate_login(url, username, password):
    """Template for login automation."""
    automator = FormAutomator()

    try:
        automator.navigate(url)
        automator.fill_text("#username", username)
        automator.fill_text("#password", password)
        automator.click("#login-button")

        # Wait for dashboard/redirect
        automator.wait_for_element(".dashboard", timeout=10)
        logger.info("Login successful!")

        return True
    except Exception as e:
        logger.error(f"Login failed: {e}")
        automator.screenshot("login_error.png")
        return False
    finally:
        automator.close()

if __name__ == "__main__":
    demo_form_fill()
```

---

## Key Takeaways

1. **Selenium** automates real browsers
2. Use **explicit waits** instead of sleep
3. **Headless mode** for background automation
4. **Find elements** by ID, class, CSS, XPath
5. **ActionChains** for complex interactions
6. Handle **dynamic content** with waits
7. **Playwright** is a modern alternative
8. Always **close the browser** when done

---

## Next Week Preview
Week 28 covers scheduling scripts and email notifications.
