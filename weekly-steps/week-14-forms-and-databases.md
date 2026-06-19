# Week 14: Forms and Databases

## Overview
This week covers handling form input properly, working with SQLite databases, and using SQLAlchemy ORM to interact with your database from Flask.

---

## Part 1: Flask-WTF for Forms

### Installation

```bash
pip install flask-wtf
```

### Creating a Form

```python
# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        Length(min=3, max=20)
    ])
    email = StringField("Email", validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=6)
    ])
    confirm = PasswordField("Confirm Password", validators=[
        DataRequired(),
        EqualTo("password", message="Passwords must match")
    ])
    submit = SubmitField("Register")

class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    message = TextAreaField("Message", validators=[
        DataRequired(),
        Length(min=10, max=500)
    ])
    submit = SubmitField("Send")
```

### Using Forms in Routes

```python
# app.py
from flask import Flask, render_template, flash, redirect, url_for
from forms import LoginForm, ContactForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key"

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Form is valid
        username = form.username.data
        password = form.password.data
        # Check credentials...
        flash(f"Welcome, {username}!", "success")
        return redirect(url_for("index"))

    return render_template("login.html", form=form)
```

### Rendering Forms in Templates

```html
<!-- templates/login.html -->
{% extends "base.html" %}

{% block content %}
<h1>Login</h1>

<form method="POST">
    {{ form.hidden_tag() }}

    <div class="form-group">
        {{ form.username.label }}
        {{ form.username(class="form-control") }}
        {% for error in form.username.errors %}
            <span class="error">{{ error }}</span>
        {% endfor %}
    </div>

    <div class="form-group">
        {{ form.password.label }}
        {{ form.password(class="form-control") }}
        {% for error in form.password.errors %}
            <span class="error">{{ error }}</span>
        {% endfor %}
    </div>

    {{ form.submit(class="btn btn-primary") }}
</form>
{% endblock %}
```

---

## Part 2: Form Validators

### Built-in Validators

```python
from wtforms.validators import (
    DataRequired,     # Field must not be empty
    Email,            # Must be valid email
    Length,           # Min/max length
    EqualTo,          # Must equal another field
    NumberRange,      # Number in range
    Optional,         # Field is optional
    Regexp,           # Match regex pattern
    URL,              # Must be valid URL
    AnyOf,            # Must be one of values
    NoneOf,           # Must not be one of values
)

class ExampleForm(FlaskForm):
    # Required with length
    name = StringField("Name", validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])

    # Email validation
    email = StringField("Email", validators=[
        DataRequired(),
        Email(message="Enter a valid email")
    ])

    # Number in range
    age = IntegerField("Age", validators=[
        DataRequired(),
        NumberRange(min=18, max=120)
    ])

    # Regex pattern
    phone = StringField("Phone", validators=[
        Optional(),
        Regexp(r"^\d{3}-\d{3}-\d{4}$", message="Format: 123-456-7890")
    ])
```

### Custom Validators

```python
from wtforms.validators import ValidationError

def validate_username(form, field):
    """Check if username is available."""
    if User.query.filter_by(username=field.data).first():
        raise ValidationError("Username already taken")

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        validate_username  # Add custom validator
    ])

    # Or as a method
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered")
```

---

## Part 3: SQLite Basics

### Direct SQLite Usage

```python
import sqlite3

# Connect to database (creates if doesn't exist)
conn = sqlite3.connect("app.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# Insert data
cursor.execute(
    "INSERT INTO users (username, email) VALUES (?, ?)",
    ("alice", "alice@example.com")
)
conn.commit()

# Query data
cursor.execute("SELECT * FROM users WHERE username = ?", ("alice",))
user = cursor.fetchone()
print(user)

# Close connection
conn.close()
```

---

## Part 4: SQLAlchemy ORM

### Installation

```bash
pip install flask-sqlalchemy
```

### Configuration

```python
# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your-secret-key"

db = SQLAlchemy(app)
```

### Defining Models

```python
# models.py
from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Post {self.title}>"
```

### Column Types

| Type | Description |
|------|-------------|
| `Integer` | Integer |
| `String(n)` | String with max length n |
| `Text` | Long text |
| `Float` | Floating point |
| `Boolean` | True/False |
| `DateTime` | Date and time |
| `Date` | Date only |
| `Time` | Time only |
| `LargeBinary` | Binary data |

### Creating Tables

```python
# Run once to create tables
with app.app_context():
    db.create_all()
```

---

## Part 5: CRUD Operations

### Create (INSERT)

```python
# Create new user
user = User(username="alice", email="alice@example.com")
db.session.add(user)
db.session.commit()

# Create with relationship
post = Post(title="My First Post", content="Hello!", author=user)
db.session.add(post)
db.session.commit()
```

### Read (SELECT)

```python
# Get all
users = User.query.all()

# Get by primary key
user = User.query.get(1)

# Get by ID (preferred in newer versions)
user = db.session.get(User, 1)

# Filter
user = User.query.filter_by(username="alice").first()
users = User.query.filter(User.email.like("%@gmail.com")).all()

# Order
users = User.query.order_by(User.created_at.desc()).all()

# Limit
users = User.query.limit(10).all()

# Pagination
page = User.query.paginate(page=1, per_page=10)
print(page.items)      # Current page items
print(page.total)      # Total items
print(page.pages)      # Total pages
print(page.has_next)   # Has next page?
print(page.has_prev)   # Has previous page?
```

### Update

```python
# Get and modify
user = User.query.get(1)
user.email = "newemail@example.com"
db.session.commit()

# Update multiple
User.query.filter_by(active=False).update({"active": True})
db.session.commit()
```

### Delete

```python
# Delete single
user = User.query.get(1)
db.session.delete(user)
db.session.commit()

# Delete multiple
User.query.filter_by(active=False).delete()
db.session.commit()
```

---

## Part 6: Relationships

### One-to-Many

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

# Usage
user = User.query.first()
user.posts  # Get all posts by user

post = Post.query.first()
post.author  # Get the user who wrote the post
```

### Many-to-Many

```python
# Association table
tags = db.Table("tags",
    db.Column("post_id", db.Integer, db.ForeignKey("post.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"))
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    tags = db.relationship("Tag", secondary=tags, backref="posts")

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

# Usage
post = Post(title="Python Tips")
python_tag = Tag(name="python")
post.tags.append(python_tag)
db.session.commit()
```

---

## Part 7: Integrating with Flask

### Full Example

```python
# app.py
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///guestbook.db"
app.config["SECRET_KEY"] = "secret"
db = SQLAlchemy(app)

# Model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

# Form
class MessageForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Sign Guestbook")

# Routes
@app.route("/", methods=["GET", "POST"])
def index():
    form = MessageForm()

    if form.validate_on_submit():
        msg = Message(name=form.name.data, message=form.message.data)
        db.session.add(msg)
        db.session.commit()
        flash("Thanks for signing!", "success")
        return redirect(url_for("index"))

    messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template("index.html", form=form, messages=messages)

@app.route("/delete/<int:id>")
def delete(id):
    msg = Message.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    flash("Message deleted", "info")
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

```html
<!-- templates/index.html -->
{% extends "base.html" %}

{% block content %}
<h1>Guestbook</h1>

<form method="POST">
    {{ form.hidden_tag() }}

    {{ form.name.label }}
    {{ form.name() }}
    {% for error in form.name.errors %}
        <span class="error">{{ error }}</span>
    {% endfor %}

    {{ form.message.label }}
    {{ form.message() }}
    {% for error in form.message.errors %}
        <span class="error">{{ error }}</span>
    {% endfor %}

    {{ form.submit() }}
</form>

<h2>Messages</h2>
{% for msg in messages %}
<div class="message">
    <strong>{{ msg.name }}</strong>
    <small>{{ msg.created_at.strftime("%Y-%m-%d %H:%M") }}</small>
    <p>{{ msg.message }}</p>
    <a href="{{ url_for('delete', id=msg.id) }}">Delete</a>
</div>
{% else %}
<p>No messages yet. Be the first to sign!</p>
{% endfor %}
{% endblock %}
```

---

## Week 14 Project: Guestbook Application

Build a complete guestbook with database storage:

```python
# app.py
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///guestbook.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your-secret-key-change-this"

db = SQLAlchemy(app)

# Models
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Entry {self.id} by {self.name}>"

# Forms
class GuestbookForm(FlaskForm):
    name = StringField("Your Name", validators=[
        DataRequired(),
        Length(min=2, max=100)
    ])
    email = StringField("Email", validators=[
        DataRequired(),
        Email()
    ])
    message = TextAreaField("Message", validators=[
        DataRequired(),
        Length(min=5, max=500)
    ])
    submit = SubmitField("Sign Guestbook")

# Routes
@app.route("/", methods=["GET", "POST"])
def index():
    form = GuestbookForm()
    page = request.args.get("page", 1, type=int)

    if form.validate_on_submit():
        entry = Entry(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        db.session.add(entry)
        db.session.commit()
        flash(f"Thanks for signing, {form.name.data}!", "success")
        return redirect(url_for("index"))

    entries = Entry.query.order_by(Entry.created_at.desc()).paginate(
        page=page, per_page=5
    )

    return render_template("index.html", form=form, entries=entries)

@app.route("/entry/<int:id>")
def entry(id):
    entry = Entry.query.get_or_404(id)
    return render_template("entry.html", entry=entry)

@app.route("/entry/<int:id>/delete", methods=["POST"])
def delete_entry(id):
    entry = Entry.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted.", "info")
    return redirect(url_for("index"))

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
```

---

## Key Takeaways

1. **Flask-WTF** provides form handling with CSRF protection
2. **Validators** ensure data meets requirements
3. **SQLAlchemy** is an ORM for database operations
4. **Models** define database tables as Python classes
5. **db.session** manages database transactions
6. **Relationships** connect related models
7. **Pagination** handles large datasets efficiently
8. Always use **parameterized queries** to prevent SQL injection

---

## Next Week Preview
Week 15 covers user authentication: sessions, login/logout, and password hashing.
