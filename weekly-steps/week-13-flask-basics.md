# Week 13: Flask Basics

## Overview
This week begins the Web Track. You'll learn Flask, a lightweight web framework for building web applications. We'll cover routes, templates, and serving HTML pages.

---

## Part 1: Introduction to Flask

### What is Flask?
- Lightweight Python web framework
- Easy to learn and get started
- Flexible and extensible
- Great for APIs and web applications

### Installation

```bash
pip install flask
```

### Your First Flask App

```python
# app.py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/about")
def about():
    return "About page"

if __name__ == "__main__":
    app.run(debug=True)
```

### Running the App

```bash
python app.py
# Open http://127.0.0.1:5000 in browser
```

---

## Part 2: Routes and URL Building

### Basic Routes

```python
from flask import Flask

app = Flask(__name__)

# Simple route
@app.route("/")
def index():
    return "Home Page"

# Route with trailing slash (Flask redirects /about to /about/)
@app.route("/about/")
def about():
    return "About Page"

# Multiple routes for one function
@app.route("/hello")
@app.route("/hi")
def greeting():
    return "Hello!"
```

### Dynamic Routes

```python
# Variable in URL
@app.route("/user/<username>")
def user_profile(username):
    return f"Profile: {username}"

# Type converters
@app.route("/post/<int:post_id>")
def show_post(post_id):
    return f"Post ID: {post_id}"

@app.route("/path/<path:subpath>")
def show_path(subpath):
    return f"Path: {subpath}"

# Available converters:
# string (default), int, float, path, uuid
```

### URL Building

```python
from flask import Flask, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return "Home"

@app.route("/user/<username>")
def profile(username):
    return f"User: {username}"

@app.route("/login")
def login():
    return "Login"

with app.test_request_context():
    print(url_for("index"))           # /
    print(url_for("profile", username="john"))  # /user/john
    print(url_for("login"))           # /login
    print(url_for("login", next="/"))  # /login?next=/
```

---

## Part 3: HTTP Methods

```python
from flask import Flask, request

app = Flask(__name__)

# GET only (default)
@app.route("/get-example")
def get_example():
    return "GET request"

# Multiple methods
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return "Processing login..."
    return "Login form"

# Separate handlers
@app.get("/items")
def get_items():
    return "List of items"

@app.post("/items")
def create_item():
    return "Item created"
```

---

## Part 4: Templates with Jinja2

### Project Structure

```
my_app/
├── app.py
├── templates/
│   ├── base.html
│   ├── index.html
│   └── about.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

### Basic Template

```python
# app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user/<name>")
def user(name):
    return render_template("user.html", username=name)
```

```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>My Flask App</title>
</head>
<body>
    <h1>Welcome to Flask!</h1>
    <p>This is the home page.</p>
</body>
</html>
```

```html
<!-- templates/user.html -->
<!DOCTYPE html>
<html>
<head>
    <title>User Profile</title>
</head>
<body>
    <h1>Hello, {{ username }}!</h1>
</body>
</html>
```

### Template Variables

```python
@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html",
        title="Dashboard",
        user={"name": "Alice", "email": "alice@test.com"},
        items=["Item 1", "Item 2", "Item 3"],
        logged_in=True
    )
```

```html
<!-- templates/dashboard.html -->
<h1>{{ title }}</h1>
<p>Welcome, {{ user.name }}!</p>
<p>Email: {{ user.email }}</p>

<ul>
{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}
</ul>

{% if logged_in %}
    <a href="/logout">Logout</a>
{% else %}
    <a href="/login">Login</a>
{% endif %}
```

---

## Part 5: Jinja2 Template Syntax

### Variables

```html
{{ variable }}
{{ user.name }}
{{ items[0] }}
{{ get_username() }}
```

### Control Structures

```html
<!-- If statements -->
{% if user %}
    <p>Hello, {{ user.name }}!</p>
{% elif guest %}
    <p>Hello, Guest!</p>
{% else %}
    <p>Please log in.</p>
{% endif %}

<!-- For loops -->
{% for item in items %}
    <p>{{ loop.index }}. {{ item }}</p>
{% else %}
    <p>No items found.</p>
{% endfor %}

<!-- Loop variables -->
{{ loop.index }}     <!-- 1-indexed -->
{{ loop.index0 }}    <!-- 0-indexed -->
{{ loop.first }}     <!-- True if first iteration -->
{{ loop.last }}      <!-- True if last iteration -->
{{ loop.length }}    <!-- Total number of items -->
```

### Filters

```html
{{ name|capitalize }}
{{ name|upper }}
{{ name|lower }}
{{ name|title }}
{{ text|truncate(50) }}
{{ items|length }}
{{ items|join(", ") }}
{{ number|default(0) }}
{{ html_content|safe }}
{{ price|round(2) }}
```

### Comments

```html
{# This is a comment #}
```

---

## Part 6: Template Inheritance

### Base Template

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My App{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    {% block head %}{% endblock %}
</head>
<body>
    <nav>
        <a href="{{ url_for('index') }}">Home</a>
        <a href="{{ url_for('about') }}">About</a>
        <a href="{{ url_for('contact') }}">Contact</a>
    </nav>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <p>&copy; 2024 My App</p>
    </footer>

    {% block scripts %}{% endblock %}
</body>
</html>
```

### Child Template

```html
<!-- templates/index.html -->
{% extends "base.html" %}

{% block title %}Home - My App{% endblock %}

{% block content %}
<h1>Welcome!</h1>
<p>This is the home page.</p>
{% endblock %}
```

```html
<!-- templates/about.html -->
{% extends "base.html" %}

{% block title %}About - My App{% endblock %}

{% block content %}
<h1>About Us</h1>
<p>We are a Flask application.</p>
{% endblock %}
```

---

## Part 7: Static Files

### Serving Static Files

```html
<!-- In templates -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
<script src="{{ url_for('static', filename='js/main.js') }}"></script>
<img src="{{ url_for('static', filename='images/logo.png') }}">
```

### Example CSS

```css
/* static/css/style.css */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

nav {
    background: #333;
    padding: 10px;
    margin-bottom: 20px;
}

nav a {
    color: white;
    text-decoration: none;
    margin-right: 15px;
}

nav a:hover {
    text-decoration: underline;
}

footer {
    margin-top: 40px;
    padding-top: 20px;
    border-top: 1px solid #ccc;
    text-align: center;
    color: #666;
}
```

---

## Part 8: Request Data

### Query Parameters

```python
from flask import request

@app.route("/search")
def search():
    query = request.args.get("q", "")
    page = request.args.get("page", 1, type=int)
    return f"Searching for: {query}, page {page}"

# URL: /search?q=python&page=2
```

### Form Data

```python
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Process login
        return f"Logging in {username}"
    return render_template("login.html")
```

```html
<!-- templates/login.html -->
<form method="POST">
    <input type="text" name="username" placeholder="Username">
    <input type="password" name="password" placeholder="Password">
    <button type="submit">Login</button>
</form>
```

---

## Part 9: Flash Messages

```python
from flask import Flask, flash, redirect, url_for, render_template

app = Flask(__name__)
app.secret_key = "your-secret-key"  # Required for sessions

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    # Process form...
    flash("Your submission was successful!", "success")
    flash("Note: This is a demo.", "info")
    return redirect(url_for("index"))
```

```html
<!-- In template -->
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="alert alert-{{ category }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

---

## Part 10: Error Handling

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500

# Custom abort
from flask import abort

@app.route("/admin")
def admin():
    if not is_admin():
        abort(403)  # Forbidden
    return "Admin page"
```

```html
<!-- templates/404.html -->
{% extends "base.html" %}

{% block content %}
<h1>Page Not Found</h1>
<p>Sorry, the page you're looking for doesn't exist.</p>
<a href="{{ url_for('index') }}">Go Home</a>
{% endblock %}
```

---

## Week 13 Project: Multi-Page Website

Build a simple multi-page website:

```python
# app.py
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = "your-secret-key-here"

# Sample data
PORTFOLIO_ITEMS = [
    {"title": "Project 1", "description": "A web application", "image": "project1.jpg"},
    {"title": "Project 2", "description": "Mobile app design", "image": "project2.jpg"},
    {"title": "Project 3", "description": "Data visualization", "image": "project3.jpg"},
]

TEAM_MEMBERS = [
    {"name": "Alice", "role": "Developer", "bio": "Full-stack developer with 5 years experience."},
    {"name": "Bob", "role": "Designer", "bio": "UI/UX designer passionate about user experience."},
    {"name": "Charlie", "role": "Manager", "bio": "Project manager keeping everything on track."},
]

@app.route("/")
def index():
    return render_template("index.html", featured=PORTFOLIO_ITEMS[:2])

@app.route("/about")
def about():
    return render_template("about.html", team=TEAM_MEMBERS)

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html", items=PORTFOLIO_ITEMS)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        # In real app, send email or save to database
        if name and email and message:
            flash(f"Thanks {name}! We'll get back to you soon.", "success")
            return redirect(url_for("contact"))
        else:
            flash("Please fill in all fields.", "error")

    return render_template("contact.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)
```

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Portfolio{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <header>
        <nav>
            <div class="logo">MyPortfolio</div>
            <ul>
                <li><a href="{{ url_for('index') }}">Home</a></li>
                <li><a href="{{ url_for('about') }}">About</a></li>
                <li><a href="{{ url_for('portfolio') }}">Portfolio</a></li>
                <li><a href="{{ url_for('contact') }}">Contact</a></li>
            </ul>
        </nav>
    </header>

    <main>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <div class="messages">
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
                </div>
            {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </main>

    <footer>
        <p>&copy; 2024 MyPortfolio. All rights reserved.</p>
    </footer>
</body>
</html>
```

```html
<!-- templates/index.html -->
{% extends "base.html" %}

{% block title %}Home - My Portfolio{% endblock %}

{% block content %}
<section class="hero">
    <h1>Welcome to My Portfolio</h1>
    <p>I'm a developer passionate about building great web applications.</p>
    <a href="{{ url_for('portfolio') }}" class="btn">View My Work</a>
</section>

<section class="featured">
    <h2>Featured Projects</h2>
    <div class="grid">
        {% for item in featured %}
        <div class="card">
            <h3>{{ item.title }}</h3>
            <p>{{ item.description }}</p>
        </div>
        {% endfor %}
    </div>
</section>
{% endblock %}
```

```html
<!-- templates/contact.html -->
{% extends "base.html" %}

{% block title %}Contact - My Portfolio{% endblock %}

{% block content %}
<h1>Contact Me</h1>

<form method="POST" class="contact-form">
    <div class="form-group">
        <label for="name">Name</label>
        <input type="text" id="name" name="name" required>
    </div>

    <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" name="email" required>
    </div>

    <div class="form-group">
        <label for="message">Message</label>
        <textarea id="message" name="message" rows="5" required></textarea>
    </div>

    <button type="submit" class="btn">Send Message</button>
</form>
{% endblock %}
```

---

## Key Takeaways

1. **Flask** is a lightweight web framework
2. **Routes** map URLs to Python functions
3. **Templates** separate HTML from Python code
4. **Jinja2** provides template inheritance and control structures
5. **Static files** serve CSS, JS, and images
6. **request** object accesses form and query data
7. **flash()** displays one-time messages
8. Use **url_for()** to build URLs dynamically

---

## Next Week Preview
Week 14 covers forms, databases with SQLite, and SQLAlchemy.
