# Weeks 17-18: Web Project - Task Manager

## Overview
Over these two weeks, you'll build a complete task manager web application combining Flask, SQLAlchemy, authentication, forms, and REST APIs.

---

## Project Features

- User registration and login
- Create, edit, delete tasks
- Task categories/tags
- Due dates and priorities
- Mark tasks complete
- Filter and search tasks
- REST API endpoints
- Responsive design

---

## Project Structure

```
task_manager/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── main.py
│   │   └── api.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── tasks/
│   │       ├── list.html
│   │       ├── create.html
│   │       └── edit.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── main.js
├── config.py
├── requirements.txt
└── run.py
```

---

## Week 17: Core Application

### config.py

```python
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///tasks.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### app/__init__.py

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.api import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(api_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app
```

### app/models.py

```python
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tasks = db.relationship("Task", backref="owner", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(7), default="#6c757d")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    tasks = db.relationship("Task", backref="category", lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.Integer, default=2)  # 1=High, 2=Medium, 3=Low
    due_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "priority": self.priority,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat(),
            "category_id": self.category_id
        }
```

### app/forms.py

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DateField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from app.models import User

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

class TaskForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=200)])
    description = TextAreaField("Description", validators=[Optional(), Length(max=1000)])
    priority = SelectField("Priority", choices=[
        ("1", "High"),
        ("2", "Medium"),
        ("3", "Low")
    ], coerce=int)
    due_date = DateField("Due Date", validators=[Optional()])
    category_id = SelectField("Category", coerce=int, validators=[Optional()])
    submit = SubmitField("Save Task")

class CategoryForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=50)])
    color = StringField("Color", default="#6c757d")
    submit = SubmitField("Save Category")
```

### app/routes/auth.py

```python
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Category
from app.forms import LoginForm, RegistrationForm

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)

        # Create default categories
        defaults = [
            ("Work", "#007bff"),
            ("Personal", "#28a745"),
            ("Shopping", "#ffc107")
        ]
        for name, color in defaults:
            cat = Category(name=name, color=color, user_id=user.id)
            db.session.add(cat)

        db.session.commit()
        flash("Registration successful!", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main.dashboard"))
        flash("Invalid username or password", "error")

    return render_template("auth/login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for("main.index"))
```

### app/routes/main.py

```python
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models import Task, Category
from app.forms import TaskForm, CategoryForm

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("index.html")

@main_bp.route("/dashboard")
@login_required
def dashboard():
    # Get filter parameters
    status = request.args.get("status", "all")
    category_id = request.args.get("category", type=int)
    priority = request.args.get("priority", type=int)

    # Base query
    query = Task.query.filter_by(user_id=current_user.id)

    # Apply filters
    if status == "pending":
        query = query.filter_by(completed=False)
    elif status == "completed":
        query = query.filter_by(completed=True)

    if category_id:
        query = query.filter_by(category_id=category_id)

    if priority:
        query = query.filter_by(priority=priority)

    # Order by due date, then priority
    tasks = query.order_by(Task.due_date.asc().nullslast(), Task.priority.asc()).all()
    categories = Category.query.filter_by(user_id=current_user.id).all()

    # Stats
    total = Task.query.filter_by(user_id=current_user.id).count()
    completed = Task.query.filter_by(user_id=current_user.id, completed=True).count()
    pending = total - completed

    return render_template(
        "tasks/list.html",
        tasks=tasks,
        categories=categories,
        stats={"total": total, "completed": completed, "pending": pending}
    )

@main_bp.route("/tasks/create", methods=["GET", "POST"])
@login_required
def create_task():
    form = TaskForm()
    form.category_id.choices = [(0, "No Category")] + [
        (c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id).all()
    ]

    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data,
            due_date=form.due_date.data,
            category_id=form.category_id.data if form.category_id.data else None,
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        flash("Task created!", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("tasks/create.html", form=form)

@main_bp.route("/tasks/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        flash("Access denied", "error")
        return redirect(url_for("main.dashboard"))

    form = TaskForm(obj=task)
    form.category_id.choices = [(0, "No Category")] + [
        (c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id).all()
    ]

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.priority = form.priority.data
        task.due_date = form.due_date.data
        task.category_id = form.category_id.data if form.category_id.data else None
        db.session.commit()
        flash("Task updated!", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("tasks/edit.html", form=form, task=task)

@main_bp.route("/tasks/<int:id>/toggle", methods=["POST"])
@login_required
def toggle_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        return {"error": "Access denied"}, 403

    task.completed = not task.completed
    task.completed_at = datetime.utcnow() if task.completed else None
    db.session.commit()

    return redirect(url_for("main.dashboard"))

@main_bp.route("/tasks/<int:id>/delete", methods=["POST"])
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        flash("Access denied", "error")
        return redirect(url_for("main.dashboard"))

    db.session.delete(task)
    db.session.commit()
    flash("Task deleted", "info")
    return redirect(url_for("main.dashboard"))
```

---

## Week 18: API and Polish

### app/routes/api.py

```python
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models import Task, Category

api_bp = Blueprint("api", __name__)

@api_bp.route("/tasks", methods=["GET"])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([t.to_dict() for t in tasks])

@api_bp.route("/tasks/<int:id>", methods=["GET"])
@login_required
def get_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        return jsonify({"error": "Access denied"}), 403
    return jsonify(task.to_dict())

@api_bp.route("/tasks", methods=["POST"])
@login_required
def create_task():
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Title required"}), 400

    task = Task(
        title=data["title"],
        description=data.get("description", ""),
        priority=data.get("priority", 2),
        user_id=current_user.id
    )
    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201

@api_bp.route("/tasks/<int:id>", methods=["PUT"])
@login_required
def update_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        return jsonify({"error": "Access denied"}), 403

    data = request.get_json()
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.priority = data.get("priority", task.priority)
    task.completed = data.get("completed", task.completed)
    db.session.commit()

    return jsonify(task.to_dict())

@api_bp.route("/tasks/<int:id>", methods=["DELETE"])
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        return jsonify({"error": "Access denied"}), 403

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted"})

@api_bp.route("/stats", methods=["GET"])
@login_required
def get_stats():
    total = Task.query.filter_by(user_id=current_user.id).count()
    completed = Task.query.filter_by(user_id=current_user.id, completed=True).count()

    return jsonify({
        "total": total,
        "completed": completed,
        "pending": total - completed,
        "completion_rate": round(completed / total * 100, 1) if total > 0 else 0
    })
```

### run.py

```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

### requirements.txt

```
flask
flask-sqlalchemy
flask-login
flask-wtf
email-validator
```

---

## Key Features Implemented

1. **User Authentication** - Register, login, logout
2. **Task CRUD** - Create, read, update, delete tasks
3. **Categories** - Organize tasks by category
4. **Priorities** - High, medium, low priorities
5. **Due Dates** - Track task deadlines
6. **Filtering** - Filter by status, category, priority
7. **REST API** - JSON endpoints for tasks
8. **Statistics** - Task completion stats

---

## Next Steps

- Add email notifications for due dates
- Implement task sharing between users
- Add recurring tasks
- Create mobile-responsive design
- Add task comments
- Implement drag-and-drop reordering

---

## Next Week Preview
Week 19 begins the Data Track with Pandas basics.
