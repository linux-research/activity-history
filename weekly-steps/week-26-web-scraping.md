# Week 26: Web Scraping

## Overview
This week covers web scraping: extracting data from websites using requests and BeautifulSoup.

---

## Part 1: HTTP Requests

```python
import requests

# GET request
response = requests.get("https://example.com")
print(response.status_code)  # 200
print(response.text)         # HTML content
print(response.headers)      # Response headers

# With parameters
params = {"q": "python", "page": 1}
response = requests.get("https://api.example.com/search", params=params)

# With headers
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get("https://example.com", headers=headers)

# With timeout
response = requests.get("https://example.com", timeout=10)

# Error handling
try:
    response = requests.get("https://example.com", timeout=10)
    response.raise_for_status()  # Raise error for 4xx/5xx
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
```

---

## Part 2: BeautifulSoup Basics

### Installation

```bash
pip install beautifulsoup4 lxml
```

### Parsing HTML

```python
from bs4 import BeautifulSoup

html = """
<html>
<head><title>My Page</title></head>
<body>
    <h1 class="title">Welcome</h1>
    <div id="content">
        <p>First paragraph</p>
        <p class="highlight">Second paragraph</p>
    </div>
    <ul>
        <li><a href="/page1">Link 1</a></li>
        <li><a href="/page2">Link 2</a></li>
    </ul>
</body>
</html>
"""

soup = BeautifulSoup(html, "lxml")

# Find elements
title = soup.title.text              # "My Page"
h1 = soup.h1.text                    # "Welcome"
first_p = soup.p.text                # "First paragraph"

# Find by tag
all_p = soup.find_all("p")           # All <p> elements
all_links = soup.find_all("a")       # All <a> elements

# Find by class
highlighted = soup.find(class_="highlight")
highlights = soup.find_all(class_="highlight")

# Find by ID
content = soup.find(id="content")

# Find by attribute
links = soup.find_all("a", href=True)
```

---

## Part 3: CSS Selectors

```python
from bs4 import BeautifulSoup

# CSS selector syntax
soup.select("p")                     # All <p>
soup.select(".highlight")            # Class
soup.select("#content")              # ID
soup.select("div p")                 # <p> inside <div>
soup.select("div > p")               # Direct child <p>
soup.select("a[href]")               # <a> with href
soup.select('a[href^="/"]')          # href starts with /
soup.select("li:nth-child(2)")       # Second <li>

# Select one
soup.select_one("h1")                # First match
```

---

## Part 4: Extracting Data

```python
from bs4 import BeautifulSoup

# Get text
element.text                         # All text
element.get_text()                   # Same
element.get_text(strip=True)         # Stripped
element.get_text(separator=" ")      # With separator

# Get attributes
link = soup.find("a")
href = link["href"]                  # Get attribute
href = link.get("href")              # Safe get (returns None)

# Get all attributes
attrs = link.attrs                   # Dictionary

# Navigate tree
element.parent                       # Parent element
element.children                     # Direct children
element.descendants                  # All descendants
element.next_sibling                 # Next sibling
element.previous_sibling             # Previous sibling
```

---

## Part 5: Complete Scraping Example

```python
import requests
from bs4 import BeautifulSoup
import time

def scrape_quotes():
    """Scrape quotes from quotes.toscrape.com"""
    base_url = "http://quotes.toscrape.com"
    quotes_data = []
    page = 1

    while True:
        url = f"{base_url}/page/{page}/"
        print(f"Scraping page {page}...")

        response = requests.get(url)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "lxml")
        quotes = soup.find_all("div", class_="quote")

        if not quotes:
            break

        for quote in quotes:
            text = quote.find("span", class_="text").text
            author = quote.find("small", class_="author").text
            tags = [tag.text for tag in quote.find_all("a", class_="tag")]

            quotes_data.append({
                "text": text,
                "author": author,
                "tags": tags
            })

        page += 1
        time.sleep(1)  # Be polite

    return quotes_data

quotes = scrape_quotes()
print(f"Scraped {len(quotes)} quotes")
```

---

## Part 6: Handling Pagination

```python
import requests
from bs4 import BeautifulSoup

def scrape_with_pagination(base_url, max_pages=10):
    """Scrape multiple pages."""
    all_data = []

    for page in range(1, max_pages + 1):
        url = f"{base_url}?page={page}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to fetch page {page}")
            break

        soup = BeautifulSoup(response.text, "lxml")
        items = soup.find_all("div", class_="item")

        if not items:
            print(f"No more items on page {page}")
            break

        for item in items:
            data = extract_item(item)
            all_data.append(data)

        print(f"Page {page}: {len(items)} items")
        time.sleep(1)

    return all_data

def follow_next_link(url):
    """Follow 'next' links for pagination."""
    all_data = []

    while url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        # Extract data from current page
        items = soup.find_all("div", class_="item")
        all_data.extend([extract_item(i) for i in items])

        # Find next link
        next_link = soup.find("a", class_="next")
        url = next_link["href"] if next_link else None

        time.sleep(1)

    return all_data
```

---

## Part 7: Saving Scraped Data

```python
import json
import csv

def save_to_json(data, filename):
    """Save data to JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved to {filename}")

def save_to_csv(data, filename):
    """Save data to CSV file."""
    if not data:
        return

    fieldnames = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"Saved to {filename}")
```

---

## Part 8: Best Practices

```python
import requests
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import urljoin

class WebScraper:
    """Polite web scraper with best practices."""

    def __init__(self, base_url, delay=1):
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

    def get_page(self, url):
        """Fetch a page with error handling."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            time.sleep(self.delay + random.uniform(0, 0.5))
            return BeautifulSoup(response.text, "lxml")
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def absolute_url(self, relative_url):
        """Convert relative URL to absolute."""
        return urljoin(self.base_url, relative_url)

    def check_robots_txt(self):
        """Check robots.txt for allowed paths."""
        robots_url = urljoin(self.base_url, "/robots.txt")
        response = self.session.get(robots_url)
        print(response.text)
```

### Ethical Scraping Rules

1. Check `robots.txt` before scraping
2. Add delays between requests (1+ seconds)
3. Identify yourself with a User-Agent
4. Don't overload servers
5. Cache responses when possible
6. Respect rate limits
7. Don't scrape personal data without permission
8. Check website's Terms of Service

---

## Week 26 Project: News Scraper

```python
#!/usr/bin/env python3
"""
News Article Scraper
Scrapes headlines and articles from news websites.
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
from datetime import datetime
from pathlib import Path
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsScraper:
    """Scrape news articles from Hacker News."""

    def __init__(self):
        self.base_url = "https://news.ycombinator.com"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Python News Scraper (Educational)"
        })

    def get_page(self, url):
        """Fetch and parse a page."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.text, "lxml")
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    def scrape_front_page(self):
        """Scrape front page stories."""
        soup = self.get_page(self.base_url)
        if not soup:
            return []

        stories = []
        rows = soup.select("tr.athing")

        for row in rows:
            try:
                story = self._parse_story(row)
                if story:
                    stories.append(story)
            except Exception as e:
                logger.warning(f"Error parsing story: {e}")

        return stories

    def _parse_story(self, row):
        """Parse a single story row."""
        rank_elem = row.select_one("span.rank")
        title_elem = row.select_one("span.titleline > a")
        site_elem = row.select_one("span.sitestr")

        if not title_elem:
            return None

        # Get subtext row (score, author, comments)
        subtext_row = row.find_next_sibling("tr")
        subtext = subtext_row.select_one("td.subtext") if subtext_row else None

        score = "0"
        author = "unknown"
        comments = "0"

        if subtext:
            score_elem = subtext.select_one("span.score")
            author_elem = subtext.select_one("a.hnuser")
            comments_elems = subtext.select("a")

            score = score_elem.text if score_elem else "0"
            author = author_elem.text if author_elem else "unknown"

            for a in comments_elems:
                if "comment" in a.text.lower():
                    comments = a.text.split()[0]

        return {
            "rank": rank_elem.text.strip(".") if rank_elem else "",
            "title": title_elem.text,
            "url": title_elem.get("href", ""),
            "site": site_elem.text if site_elem else "",
            "score": score.replace(" points", ""),
            "author": author,
            "comments": comments.replace("comments", "").strip(),
            "scraped_at": datetime.now().isoformat()
        }

    def scrape_multiple_pages(self, num_pages=3):
        """Scrape multiple pages."""
        all_stories = []

        for page in range(1, num_pages + 1):
            url = f"{self.base_url}/news?p={page}"
            logger.info(f"Scraping page {page}...")

            soup = self.get_page(url)
            if not soup:
                break

            rows = soup.select("tr.athing")
            for row in rows:
                try:
                    story = self._parse_story(row)
                    if story:
                        all_stories.append(story)
                except Exception as e:
                    logger.warning(f"Error: {e}")

            time.sleep(2)  # Be polite

        return all_stories

def save_results(stories, format="json"):
    """Save scraped stories."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if format == "json":
        filename = f"news_{timestamp}.json"
        with open(filename, "w") as f:
            json.dump(stories, f, indent=2)
    elif format == "csv":
        filename = f"news_{timestamp}.csv"
        if stories:
            with open(filename, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=stories[0].keys())
                writer.writeheader()
                writer.writerows(stories)

    logger.info(f"Saved {len(stories)} stories to {filename}")
    return filename

def main():
    scraper = NewsScraper()

    print("Scraping Hacker News...")
    stories = scraper.scrape_multiple_pages(3)

    print(f"\nScraped {len(stories)} stories")
    print("\nTop 5 stories:")
    for story in stories[:5]:
        print(f"  {story['rank']}. {story['title']}")
        print(f"     {story['score']} points | {story['comments']} comments")

    save_results(stories, "json")
    save_results(stories, "csv")

if __name__ == "__main__":
    main()
```

---

## Key Takeaways

1. Use **requests** for HTTP requests
2. **BeautifulSoup** parses HTML
3. Use **CSS selectors** for precise element selection
4. Handle **pagination** properly
5. Be **polite**: add delays, use User-Agent
6. Check **robots.txt** and ToS
7. Handle **errors** gracefully
8. Save data in **multiple formats**

---

## Next Week Preview
Week 27 covers browser automation with Selenium or Playwright.
