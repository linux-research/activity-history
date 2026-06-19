# Week 32: Advanced Testing

## Overview
This week covers advanced testing techniques: mocking external services, fixtures for complex setups, test coverage, and integration testing.

---

## Part 1: Mocking Basics

### Why Mock?
- Isolate code from external dependencies
- Test without network calls, databases, etc.
- Control test conditions precisely
- Speed up tests

### Basic Mocking

```python
from unittest.mock import Mock, patch

# Create a mock object
mock_obj = Mock()
mock_obj.method.return_value = 42
print(mock_obj.method())  # 42

# Mock with side_effect
mock_obj.method.side_effect = ValueError("Error!")
# mock_obj.method()  # Raises ValueError

# Mock assertions
mock_obj.method(1, 2, key="value")
mock_obj.method.assert_called_once_with(1, 2, key="value")
```

---

## Part 2: Patching

### Patching Functions

```python
from unittest.mock import patch
import requests

def get_user(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

# Test with patch
@patch("requests.get")
def test_get_user(mock_get):
    mock_get.return_value.json.return_value = {"id": 1, "name": "Alice"}

    result = get_user(1)

    assert result["name"] == "Alice"
    mock_get.assert_called_once()

# Context manager style
def test_get_user_context():
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"id": 1, "name": "Alice"}

        result = get_user(1)

        assert result["name"] == "Alice"
```

### Patching Classes

```python
from unittest.mock import patch, MagicMock

class Database:
    def connect(self):
        pass

    def query(self, sql):
        pass

def get_users(db):
    db.connect()
    return db.query("SELECT * FROM users")

@patch("module.Database")
def test_get_users(MockDatabase):
    mock_db = MockDatabase.return_value
    mock_db.query.return_value = [{"id": 1, "name": "Alice"}]

    result = get_users(mock_db)

    assert len(result) == 1
    mock_db.connect.assert_called_once()
```

---

## Part 3: pytest Fixtures

### Basic Fixtures

```python
import pytest

@pytest.fixture
def sample_data():
    return {"name": "Alice", "age": 30}

@pytest.fixture
def user():
    return User("Alice", "alice@test.com")

def test_with_fixtures(sample_data, user):
    assert sample_data["name"] == "Alice"
    assert user.email == "alice@test.com"
```

### Fixture Scope

```python
import pytest

@pytest.fixture(scope="function")  # Default: new for each test
def per_test_fixture():
    return create_resource()

@pytest.fixture(scope="class")
def per_class_fixture():
    return create_resource()

@pytest.fixture(scope="module")
def per_module_fixture():
    return create_resource()

@pytest.fixture(scope="session")
def per_session_fixture():
    return create_database_connection()
```

### Fixture with Setup/Teardown

```python
import pytest

@pytest.fixture
def database():
    # Setup
    db = Database()
    db.connect()

    yield db  # Test runs here

    # Teardown
    db.close()

@pytest.fixture
def temp_file(tmp_path):
    file_path = tmp_path / "test.txt"
    file_path.write_text("test content")
    yield file_path
    # File automatically cleaned up by tmp_path
```

### Parametrized Fixtures

```python
import pytest

@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def database_type(request):
    return request.param

def test_database_operations(database_type):
    # Test runs three times, once for each database type
    print(f"Testing with {database_type}")
```

---

## Part 4: conftest.py

```python
# conftest.py - shared fixtures

import pytest

@pytest.fixture(scope="session")
def app():
    """Create application instance."""
    from myapp import create_app
    app = create_app(testing=True)
    return app

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture
def db(app):
    """Create database tables."""
    from myapp import db as _db
    with app.app_context():
        _db.create_all()
        yield _db
        _db.drop_all()

@pytest.fixture
def sample_user(db):
    """Create a sample user."""
    from myapp.models import User
    user = User(username="testuser", email="test@test.com")
    db.session.add(user)
    db.session.commit()
    return user
```

---

## Part 5: Test Coverage

### Installation

```bash
pip install pytest-cov
```

### Running with Coverage

```bash
# Basic coverage
pytest --cov=mypackage

# With report
pytest --cov=mypackage --cov-report=term-missing

# HTML report
pytest --cov=mypackage --cov-report=html

# Fail if coverage below threshold
pytest --cov=mypackage --cov-fail-under=80
```

### Coverage Configuration

```ini
# .coveragerc or pyproject.toml
[coverage:run]
source = src
omit =
    */tests/*
    */__init__.py
    */migrations/*

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if __name__ == "__main__":
```

---

## Part 6: Integration Testing

```python
import pytest
from myapp import create_app, db
from myapp.models import User

@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

class TestUserAPI:

    def test_create_user(self, client):
        response = client.post("/api/users", json={
            "username": "testuser",
            "email": "test@test.com"
        })

        assert response.status_code == 201
        assert response.json["username"] == "testuser"

    def test_get_user(self, client, sample_user):
        response = client.get(f"/api/users/{sample_user.id}")

        assert response.status_code == 200
        assert response.json["email"] == sample_user.email

    def test_user_flow(self, client):
        # Create
        create_response = client.post("/api/users", json={
            "username": "flowuser",
            "email": "flow@test.com"
        })
        assert create_response.status_code == 201
        user_id = create_response.json["id"]

        # Read
        get_response = client.get(f"/api/users/{user_id}")
        assert get_response.status_code == 200

        # Update
        update_response = client.put(f"/api/users/{user_id}", json={
            "email": "updated@test.com"
        })
        assert update_response.status_code == 200

        # Delete
        delete_response = client.delete(f"/api/users/{user_id}")
        assert delete_response.status_code == 204
```

---

## Part 7: Testing External Services

```python
import pytest
from unittest.mock import patch, Mock
import requests

class PaymentService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.payment.com"

    def charge(self, amount, card_token):
        response = requests.post(
            f"{self.base_url}/charges",
            json={"amount": amount, "token": card_token},
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return response.json()

class TestPaymentService:

    @pytest.fixture
    def payment_service(self):
        return PaymentService("test_api_key")

    @patch("requests.post")
    def test_charge_success(self, mock_post, payment_service):
        mock_post.return_value.json.return_value = {
            "id": "ch_123",
            "status": "succeeded",
            "amount": 1000
        }

        result = payment_service.charge(1000, "tok_visa")

        assert result["status"] == "succeeded"
        mock_post.assert_called_once()

    @patch("requests.post")
    def test_charge_failure(self, mock_post, payment_service):
        mock_post.return_value.json.return_value = {
            "error": "Card declined"
        }

        result = payment_service.charge(1000, "tok_declined")

        assert "error" in result

    @patch("requests.post")
    def test_charge_network_error(self, mock_post, payment_service):
        mock_post.side_effect = requests.exceptions.ConnectionError()

        with pytest.raises(requests.exceptions.ConnectionError):
            payment_service.charge(1000, "tok_visa")
```

---

## Part 8: Test Markers and Organization

```python
import pytest

# Skip tests
@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_feature():
    pass

# Expected failures
@pytest.mark.xfail(reason="Known bug #123")
def test_known_bug():
    pass

# Custom markers
@pytest.mark.slow
def test_slow_operation():
    pass

@pytest.mark.integration
def test_database_integration():
    pass

# Run specific markers
# pytest -m slow
# pytest -m "not slow"
# pytest -m "slow or integration"
```

### pytest.ini

```ini
[pytest]
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests

testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = -v --tb=short
```

---

## Week 32 Project: Achieve 80% Coverage

1. Choose a project with existing tests
2. Run coverage and identify untested code
3. Write tests to achieve 80%+ coverage
4. Add mocks for external services
5. Set up CI to enforce coverage threshold

---

## Key Takeaways

1. **Mock** external dependencies for isolation
2. **Fixtures** provide reusable test setup
3. **Scoped fixtures** optimize resource usage
4. **Coverage** shows what's tested
5. **Integration tests** verify components work together
6. Use **markers** to organize tests
7. **conftest.py** shares fixtures across tests
8. **80% coverage** is a good target

---

## Next Week Preview
Week 33 covers project architecture and CLI tools.
