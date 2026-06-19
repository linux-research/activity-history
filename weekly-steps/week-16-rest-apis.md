# Week 16: REST APIs

## Overview
This week covers building REST APIs with Flask: returning JSON, handling HTTP methods, API design principles, and error handling.

---

## Part 1: REST Basics

### What is REST?
- **RE**presentational **S**tate **T**ransfer
- Architectural style for web APIs
- Uses HTTP methods for operations
- Stateless communication

### HTTP Methods

| Method | Purpose | Example |
|--------|---------|---------|
| GET | Retrieve data | Get all users |
| POST | Create data | Create new user |
| PUT | Replace data | Update entire user |
| PATCH | Partial update | Update user email |
| DELETE | Remove data | Delete user |

### RESTful URL Patterns

```
GET    /api/users          # List all users
POST   /api/users          # Create user
GET    /api/users/1        # Get user 1
PUT    /api/users/1        # Replace user 1
PATCH  /api/users/1        # Update user 1
DELETE /api/users/1        # Delete user 1
```

---

## Part 2: Returning JSON

### Basic JSON Response

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/hello")
def hello():
    return jsonify({"message": "Hello, World!"})

@app.route("/api/users")
def get_users():
    users = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ]
    return jsonify(users)

# With status code
@app.route("/api/created")
def created():
    return jsonify({"status": "created"}), 201
```

### From Database Models

```python
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

@app.route("/api/users")
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route("/api/users/<int:id>")
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())
```

---

## Part 3: Receiving JSON

```python
from flask import request, jsonify

@app.route("/api/users", methods=["POST"])
def create_user():
    # Get JSON data from request
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Validate required fields
    if "username" not in data or "email" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    # Create user
    user = User(username=data["username"], email=data["email"])
    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201

@app.route("/api/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()

    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    db.session.commit()

    return jsonify(user.to_dict())

@app.route("/api/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted"}), 200
```

---

## Part 4: Error Handling

### Custom Error Handlers

```python
from flask import jsonify

@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad request", "message": str(e)}), 400

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500
```

### Custom Exception

```python
class APIError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code

@app.errorhandler(APIError)
def handle_api_error(error):
    return jsonify({"error": error.message}), error.status_code

# Usage
@app.route("/api/users/<int:id>")
def get_user(id):
    user = User.query.get(id)
    if not user:
        raise APIError("User not found", 404)
    return jsonify(user.to_dict())
```

---

## Part 5: Request Validation

```python
def validate_user_data(data, required_fields=None):
    """Validate user data from request."""
    errors = []

    if required_fields:
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing field: {field}")

    if "email" in data:
        if "@" not in data["email"]:
            errors.append("Invalid email format")

    if "username" in data:
        if len(data["username"]) < 3:
            errors.append("Username must be at least 3 characters")

    return errors

@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()

    errors = validate_user_data(data, required_fields=["username", "email"])
    if errors:
        return jsonify({"errors": errors}), 400

    # Create user...
```

---

## Part 6: Pagination

```python
@app.route("/api/users")
def get_users():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    # Limit per_page
    per_page = min(per_page, 100)

    pagination = User.query.paginate(page=page, per_page=per_page)

    return jsonify({
        "users": [u.to_dict() for u in pagination.items],
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }
    })
```

---

## Part 7: Complete API Example

```python
# app.py
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///api.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Models
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at.isoformat()
        }

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad request"}), 400

# Routes
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    return jsonify([t.to_dict() for t in tasks])

@app.route("/api/tasks/<int:id>", methods=["GET"])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify(task.to_dict())

@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    task = Task(
        title=data["title"],
        description=data.get("description", "")
    )
    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201

@app.route("/api/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()

    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.completed = data.get("completed", task.completed)
    db.session.commit()

    return jsonify(task.to_dict())

@app.route("/api/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted"})

@app.route("/api/tasks/<int:id>/toggle", methods=["POST"])
def toggle_task(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()

    return jsonify(task.to_dict())

# Initialize
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
```

---

## Part 8: Testing Your API

### Using curl

```bash
# GET all tasks
curl http://localhost:5000/api/tasks

# GET single task
curl http://localhost:5000/api/tasks/1

# POST create task
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Flask", "description": "Build REST API"}'

# PUT update task
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated title", "completed": true}'

# DELETE task
curl -X DELETE http://localhost:5000/api/tasks/1
```

### Using Python requests

```python
import requests

BASE_URL = "http://localhost:5000/api"

# GET all
response = requests.get(f"{BASE_URL}/tasks")
print(response.json())

# POST create
response = requests.post(
    f"{BASE_URL}/tasks",
    json={"title": "New task", "description": "Test"}
)
print(response.json())

# PUT update
response = requests.put(
    f"{BASE_URL}/tasks/1",
    json={"completed": True}
)
print(response.json())

# DELETE
response = requests.delete(f"{BASE_URL}/tasks/1")
print(response.json())
```

---

## Key Takeaways

1. **REST** uses HTTP methods for CRUD operations
2. **jsonify()** returns JSON responses
3. **request.get_json()** parses JSON from request body
4. Always **validate input** data
5. Return appropriate **status codes**
6. Implement **pagination** for large datasets
7. Create **custom error handlers** for APIs
8. Use **to_dict()** methods on models

---

## Next Week Preview
Weeks 17-18: Build a complete web application combining everything learned.
