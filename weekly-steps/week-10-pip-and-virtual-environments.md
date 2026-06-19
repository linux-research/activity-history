# Week 10: pip and Virtual Environments

## Overview
This week covers Python package management: using pip to install packages, creating isolated virtual environments, and managing project dependencies.

---

## Part 1: Understanding pip

pip is Python's package installer, connecting to PyPI (Python Package Index).

### Basic Commands

```bash
# Check pip version
pip --version
pip3 --version

# Install a package
pip install requests

# Install specific version
pip install requests==2.28.0

# Install minimum version
pip install "requests>=2.25.0"

# Upgrade a package
pip install --upgrade requests

# Uninstall a package
pip uninstall requests

# Show installed packages
pip list

# Show package info
pip show requests

# Search for packages (use PyPI website instead)
# pip search is disabled; visit https://pypi.org
```

### Installing Multiple Packages

```bash
# Install multiple at once
pip install requests beautifulsoup4 pandas

# Install from requirements file
pip install -r requirements.txt
```

---

## Part 2: Virtual Environments

Virtual environments isolate project dependencies.

### Why Virtual Environments?

- Different projects need different package versions
- Avoid polluting system Python
- Reproducible environments
- Easy dependency management

### Creating Virtual Environments

```bash
# Create virtual environment
python -m venv myenv

# On some systems
python3 -m venv myenv

# Common naming conventions
python -m venv venv        # Simple
python -m venv .venv       # Hidden directory
python -m venv env         # Alternative
```

### Activating/Deactivating

```bash
# Linux/Mac
source myenv/bin/activate

# Windows (Command Prompt)
myenv\Scripts\activate.bat

# Windows (PowerShell)
myenv\Scripts\Activate.ps1

# Deactivate (any platform)
deactivate
```

### Using the Virtual Environment

```bash
# Activate first
source myenv/bin/activate

# Your prompt changes
(myenv) $ pip install requests

# Packages install only in this environment
(myenv) $ pip list

# Deactivate when done
(myenv) $ deactivate
```

---

## Part 3: Requirements Files

### Creating requirements.txt

```bash
# Freeze current environment
pip freeze > requirements.txt

# Manual creation
# requirements.txt
requests==2.28.0
beautifulsoup4>=4.11.0
pandas~=1.5.0
python-dotenv
```

### Version Specifiers

| Specifier | Meaning |
|-----------|---------|
| `==2.28.0` | Exact version |
| `>=2.25.0` | Minimum version |
| `<=3.0.0` | Maximum version |
| `>=2.25,<3.0` | Version range |
| `~=2.28.0` | Compatible release (~=2.28.0 means >=2.28.0,<2.29.0) |
| `!=2.27.0` | Exclude version |

### Installing from Requirements

```bash
# Install all requirements
pip install -r requirements.txt

# Upgrade all packages to latest allowed versions
pip install --upgrade -r requirements.txt
```

### Development vs Production

```
# requirements.txt (production)
requests==2.28.0
pandas==1.5.3

# requirements-dev.txt (development)
-r requirements.txt
pytest==7.2.0
black==23.1.0
flake8==6.0.0
```

```bash
# Install production
pip install -r requirements.txt

# Install development (includes production)
pip install -r requirements-dev.txt
```

---

## Part 4: Project Structure

### Recommended Structure

```
my_project/
├── venv/                   # Virtual environment (don't commit)
├── src/
│   └── my_package/
│       ├── __init__.py
│       └── main.py
├── tests/
│   └── test_main.py
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── .gitignore
└── README.md
```

### .gitignore for Python

```gitignore
# Virtual environment
venv/
.venv/
env/

# Python
__pycache__/
*.py[cod]
*.pyo
.Python

# Distribution
dist/
build/
*.egg-info/

# IDE
.idea/
.vscode/
*.swp

# Environment variables
.env

# Test coverage
.coverage
htmlcov/
```

---

## Part 5: Popular Third-Party Packages

### requests - HTTP Library

```python
import requests

# GET request
response = requests.get("https://api.github.com/users/python")
print(response.status_code)  # 200
print(response.json())       # Parse JSON response

# With parameters
response = requests.get(
    "https://api.github.com/search/repositories",
    params={"q": "python", "sort": "stars"}
)

# POST request
response = requests.post(
    "https://httpbin.org/post",
    json={"name": "Alice", "age": 30}
)

# Headers
response = requests.get(
    "https://api.github.com/user",
    headers={"Authorization": "token YOUR_TOKEN"}
)

# Error handling
try:
    response = requests.get("https://example.com", timeout=5)
    response.raise_for_status()  # Raise exception for 4xx/5xx
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

### python-dotenv - Environment Variables

```python
# .env file
# API_KEY=your_secret_key
# DATABASE_URL=postgresql://localhost/db

from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Access variables
api_key = os.getenv("API_KEY")
database_url = os.getenv("DATABASE_URL")

# With default values
debug = os.getenv("DEBUG", "false").lower() == "true"
```

### Other Useful Packages

```bash
# HTTP and APIs
pip install requests httpx aiohttp

# Data processing
pip install pandas numpy

# Web scraping
pip install beautifulsoup4 lxml

# Testing
pip install pytest pytest-cov

# Code quality
pip install black flake8 mypy

# CLI tools
pip install click typer rich

# Date/time
pip install python-dateutil arrow

# Configuration
pip install python-dotenv pyyaml
```

---

## Part 6: Working with APIs

### Basic API Request

```python
import requests

def get_weather(city, api_key):
    """Get weather data from OpenWeatherMap API."""
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        return {
            "city": data["name"],
            "temp": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"]
        }
    else:
        raise Exception(f"API error: {response.status_code}")

# Usage (you'd need a real API key)
# weather = get_weather("London", "your_api_key")
```

### Handling Pagination

```python
import requests

def get_all_repos(username):
    """Get all repos for a GitHub user (handles pagination)."""
    repos = []
    page = 1

    while True:
        response = requests.get(
            f"https://api.github.com/users/{username}/repos",
            params={"page": page, "per_page": 100}
        )

        if response.status_code != 200:
            break

        data = response.json()
        if not data:
            break

        repos.extend(data)
        page += 1

    return repos

# Usage
# all_repos = get_all_repos("python")
```

---

## Part 7: Error Handling with External Services

```python
import requests
from requests.exceptions import (
    RequestException,
    ConnectionError,
    Timeout,
    HTTPError
)
import time

def robust_request(url, max_retries=3, timeout=10):
    """Make HTTP request with retries and error handling."""

    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response

        except ConnectionError:
            print(f"Connection failed (attempt {attempt + 1})")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff

        except Timeout:
            print(f"Request timed out (attempt {attempt + 1})")
            if attempt < max_retries - 1:
                time.sleep(1)

        except HTTPError as e:
            if e.response.status_code >= 500:
                # Server error, retry
                print(f"Server error {e.response.status_code}")
                if attempt < max_retries - 1:
                    time.sleep(2)
            else:
                # Client error, don't retry
                raise

    raise RequestException(f"Failed after {max_retries} attempts")
```

---

## Week 10 Project: API Data Fetcher

Build a tool to fetch and save data from public APIs:

```python
import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class APIClient:
    """Generic API client with common functionality."""

    def __init__(self, base_url, headers=None):
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def get(self, endpoint, params=None):
        """Make GET request."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_all_pages(self, endpoint, params=None, page_key="page",
                      per_page_key="per_page", per_page=100):
        """Get all pages of paginated endpoint."""
        params = params or {}
        params[per_page_key] = per_page

        all_data = []
        page = 1

        while True:
            params[page_key] = page
            data = self.get(endpoint, params)

            if isinstance(data, list):
                if not data:
                    break
                all_data.extend(data)
            elif isinstance(data, dict) and "items" in data:
                if not data["items"]:
                    break
                all_data.extend(data["items"])
            else:
                all_data.append(data)
                break

            page += 1

        return all_data


class GitHubClient(APIClient):
    """GitHub API client."""

    def __init__(self, token=None):
        headers = {"Accept": "application/vnd.github.v3+json"}
        if token:
            headers["Authorization"] = f"token {token}"

        super().__init__("https://api.github.com", headers)

    def get_user(self, username):
        """Get user information."""
        return self.get(f"/users/{username}")

    def get_repos(self, username):
        """Get all repositories for a user."""
        return self.get_all_pages(
            f"/users/{username}/repos",
            params={"sort": "updated"}
        )

    def get_repo_languages(self, owner, repo):
        """Get languages used in a repository."""
        return self.get(f"/repos/{owner}/{repo}/languages")

    def search_repos(self, query, sort="stars", max_results=100):
        """Search repositories."""
        results = []
        page = 1

        while len(results) < max_results:
            data = self.get("/search/repositories", params={
                "q": query,
                "sort": sort,
                "per_page": min(100, max_results - len(results)),
                "page": page
            })

            results.extend(data.get("items", []))

            if len(data.get("items", [])) < 100:
                break

            page += 1

        return results[:max_results]


class JSONPlaceholderClient(APIClient):
    """JSONPlaceholder API client for testing."""

    def __init__(self):
        super().__init__("https://jsonplaceholder.typicode.com")

    def get_posts(self, user_id=None):
        """Get posts, optionally filtered by user."""
        params = {"userId": user_id} if user_id else None
        return self.get("/posts", params)

    def get_users(self):
        """Get all users."""
        return self.get("/users")

    def get_comments(self, post_id):
        """Get comments for a post."""
        return self.get(f"/posts/{post_id}/comments")


def save_data(data, filename, format="json"):
    """Save data to file."""
    if format == "json":
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
    elif format == "csv":
        import csv
        if data and isinstance(data[0], dict):
            with open(filename, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)


def main():
    """Demo the API clients."""
    print("=" * 60)
    print("API Data Fetcher")
    print("=" * 60)

    # Demo with JSONPlaceholder (no auth required)
    print("\n--- JSONPlaceholder Demo ---")

    client = JSONPlaceholderClient()

    try:
        # Fetch users
        users = client.get_users()
        print(f"Fetched {len(users)} users")

        # Fetch posts for first user
        posts = client.get_posts(user_id=1)
        print(f"User 1 has {len(posts)} posts")

        # Save data
        save_data(users, "users.json")
        save_data(posts, "user1_posts.json")
        print("Data saved to users.json and user1_posts.json")

    except requests.RequestException as e:
        print(f"Error: {e}")

    # Demo with GitHub (optional auth)
    print("\n--- GitHub Demo ---")

    github_token = os.getenv("GITHUB_TOKEN")
    github = GitHubClient(token=github_token)

    try:
        # Get Python org info
        user = github.get_user("python")
        print(f"Python org: {user['name']}")
        print(f"Public repos: {user['public_repos']}")
        print(f"Followers: {user['followers']}")

        # Search for Python projects
        repos = github.search_repos("language:python stars:>10000", max_results=10)
        print(f"\nTop 10 Python repos:")
        for i, repo in enumerate(repos, 1):
            print(f"  {i}. {repo['full_name']} ({repo['stargazers_count']} stars)")

        # Save results
        save_data(repos, "top_python_repos.json")
        print("\nData saved to top_python_repos.json")

    except requests.RequestException as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
```

### Running the Project

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install requests python-dotenv

# Create .env file (optional, for GitHub API)
echo "GITHUB_TOKEN=your_token_here" > .env

# Run
python api_fetcher.py

# Save dependencies
pip freeze > requirements.txt
```

---

## Key Takeaways

1. **pip** installs packages from PyPI
2. **Virtual environments** isolate project dependencies
3. **requirements.txt** documents dependencies
4. Always activate venv before installing packages
5. Use **version specifiers** for reproducibility
6. **requests** is the standard HTTP library
7. **python-dotenv** manages environment variables
8. Handle API errors with retries and timeouts

---

## Next Week Preview
Week 11 covers testing with pytest - writing and running tests for your code.
