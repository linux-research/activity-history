# Week 15: User Authentication

## Overview
This week covers implementing user authentication in Flask: sessions, login/logout functionality, password hashing, and protecting routes.

---

## Part 1: Sessions in Flask

### Understanding Sessions

Sessions store user data across requests. Flask uses signed cookies by default.

```python
from flask import Flask, session

app = Flask(__name__)
app.secret_key = "your-secret-key"  # Required for sessions

@app.route("/")
def index():
    # Get session data
    visits = session.get("visits", 0)
    session["visits"] = visits + 1
    return f"You have visited {visits + 1} times"

@app.route("/set/<name>")
def set_name(name):
    session["username"] = name
    return f"Name set to {name}"

@app.route("/get")
def get_name():
    name = session.get("username", "Guest")
    return f"Hello, {name}"

@app.route("/clear")
def clear():
    session.clear()
    return "Session cleared"
```

---

## Part 2: Password Hashing

Never store passwords in plain text! Use proper hashing.

### Using Werkzeug

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Hash a password
password = "mysecretpassword"
hashed = generate_password_hash(password)
print(hashed)  # pbkdf2:sha256:260000$...

# Verify a password
check_password_hash(hashed, "mysecretpassword")  # True
check_password_hash(hashed, "wrongpassword")     # False
```

### In User Model

```python
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Usage
user = User(username="alice", email="alice@test.com")
user.set_password("secretpassword")
db.session.add(user)
db.session.commit()

# Later, verify
if user.check_password("secretpassword"):
    print("Password correct!")
```

---

## Part 3: Flask-Login

### Installation

```bash
pip install flask-login
```

### Setup

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"  # Redirect unauthorized users here
login_manager.login_message = "Please log in to access this page."

# User model must inherit from UserMixin
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

### UserMixin Provides

- `is_authenticated`: True if logged in
- `is_active`: True if account is active
- `is_anonymous`: False for regular users
- `get_id()`: Returns the user ID as a string

---

## Part 4: Login and Logout

### Forms

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        Length(min=3, max=20)
    ])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=6)
    ])
    confirm = PasswordField("Confirm Password", validators=[
        DataRequired(),
        EqualTo("password")
    ])
    submit = SubmitField("Register")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already taken")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered")
```

### Routes

```python
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Logged in successfully!", "success")

            # Redirect to requested page or home
            next_page = request.args.get("next")
            return redirect(next_page or url_for("index"))

        flash("Invalid username or password", "error")

    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))
```

---

## Part 5: Protecting Routes

### @login_required Decorator

```python
from flask_login import login_required, current_user

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html")
```

### Custom Decorators

```python
from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@app.route("/admin")
@login_required
@admin_required
def admin_panel():
    return render_template("admin.html")
```

---

## Part 6: Using current_user in Templates

```html
<!-- templates/base.html -->
<nav>
    <a href="{{ url_for('index') }}">Home</a>

    {% if current_user.is_authenticated %}
        <a href="{{ url_for('profile') }}">{{ current_user.username }}</a>
        <a href="{{ url_for('logout') }}">Logout</a>
    {% else %}
        <a href="{{ url_for('login') }}">Login</a>
        <a href="{{ url_for('register') }}">Register</a>
    {% endif %}
</nav>
```

```html
<!-- templates/dashboard.html -->
{% extends "base.html" %}

{% block content %}
<h1>Welcome, {{ current_user.username }}!</h1>
<p>Email: {{ current_user.email }}</p>
{% endblock %}
```

---

## Part 7: Complete Example

```python
# app.py
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Forms
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already taken")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered")

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful!", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard"))
        flash("Invalid username or password", "error")

    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for("index"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

# Initialize
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
```

---

## Week 15 Project: Add Auth to Guestbook

Add user accounts to the guestbook from Week 14.

See full implementation in the project files.

---

## Key Takeaways

1. **Sessions** store user data across requests
2. **Never store plain text passwords** - use hashing
3. **Flask-Login** manages user sessions
4. **@login_required** protects routes
5. **current_user** accesses logged-in user anywhere
6. **Remember me** extends session duration
7. Validate **unique usernames/emails** in forms
8. Redirect to **next** page after login

---

## Next Week Preview
Week 16 covers REST APIs: returning JSON from Flask.
