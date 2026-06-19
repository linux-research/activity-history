# Week 11: Testing with pytest

## Overview
This week covers writing and running tests using pytest. Testing ensures your code works correctly and helps prevent bugs when making changes.

---

## Part 1: Why Testing?

### Benefits of Testing
- **Catch bugs early** before they reach production
- **Document behavior** tests show how code should work
- **Refactor safely** know if changes break anything
- **Design better** testable code is often better code

### Types of Tests
- **Unit tests**: Test individual functions/classes
- **Integration tests**: Test components working together
- **End-to-end tests**: Test complete workflows

---

## Part 2: Getting Started with pytest

### Installation

```bash
pip install pytest
```

### Your First Test

```python
# test_example.py

def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific file
pytest test_example.py

# Run specific test
pytest test_example.py::test_add

# Verbose output
pytest -v

# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf
```

---

## Part 3: Test Structure

### Naming Conventions

```python
# Files: test_*.py or *_test.py
# Functions: test_*
# Classes: Test*

# test_calculator.py
def test_addition():
    pass

def test_subtraction():
    pass

class TestCalculator:
    def test_multiply(self):
        pass
```

### Arrange-Act-Assert Pattern

```python
def test_user_creation():
    # Arrange - set up test data
    name = "Alice"
    age = 30

    # Act - perform the action
    user = User(name, age)

    # Assert - verify the result
    assert user.name == "Alice"
    assert user.age == 30
```

---

## Part 4: Assertions

### Basic Assertions

```python
def test_assertions():
    # Equality
    assert 1 + 1 == 2
    assert "hello".upper() == "HELLO"

    # Truthiness
    assert True
    assert [1, 2, 3]  # Non-empty list is truthy
    assert not []     # Empty list is falsy

    # Comparisons
    assert 5 > 3
    assert 10 <= 10

    # Membership
    assert 3 in [1, 2, 3]
    assert "h" in "hello"

    # Identity
    a = [1, 2]
    b = a
    assert a is b

    # Type checking
    assert isinstance("hello", str)
    assert isinstance(42, int)
```

### Testing Exceptions

```python
import pytest

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)

def test_divide_by_zero_message():
    with pytest.raises(ValueError) as exc_info:
        divide(10, 0)
    assert "zero" in str(exc_info.value)

def test_divide_by_zero_match():
    with pytest.raises(ValueError, match="Cannot divide"):
        divide(10, 0)
```

### Approximate Comparisons

```python
import pytest

def test_float_comparison():
    # Floating point comparison
    assert 0.1 + 0.2 == pytest.approx(0.3)

    # With tolerance
    assert 2.0 == pytest.approx(2.02, rel=0.01)  # 1% tolerance
    assert 2.0 == pytest.approx(2.02, abs=0.05)  # Absolute tolerance
```

---

## Part 5: Fixtures

Fixtures provide reusable test setup.

### Basic Fixtures

```python
import pytest

@pytest.fixture
def sample_list():
    return [1, 2, 3, 4, 5]

@pytest.fixture
def empty_list():
    return []

def test_list_length(sample_list):
    assert len(sample_list) == 5

def test_list_sum(sample_list):
    assert sum(sample_list) == 15

def test_empty_list(empty_list):
    assert len(empty_list) == 0
```

### Fixture Scope

```python
import pytest

@pytest.fixture(scope="function")  # Default: run for each test
def per_test():
    print("\nSetting up for test")
    return {"data": "test"}

@pytest.fixture(scope="module")  # Run once per module
def per_module():
    print("\nSetting up for module")
    return create_expensive_resource()

@pytest.fixture(scope="session")  # Run once per test session
def per_session():
    print("\nSetting up for session")
    return create_database_connection()
```

### Fixture with Cleanup

```python
import pytest

@pytest.fixture
def temp_file():
    # Setup
    import tempfile
    f = tempfile.NamedTemporaryFile(delete=False)
    f.write(b"test data")
    f.close()

    yield f.name  # Provide the fixture value

    # Cleanup (runs after test)
    import os
    os.unlink(f.name)

def test_read_temp_file(temp_file):
    with open(temp_file, "rb") as f:
        assert f.read() == b"test data"
```

### conftest.py - Shared Fixtures

```python
# conftest.py - automatically discovered by pytest

import pytest

@pytest.fixture
def database():
    """Shared fixture available to all tests."""
    db = Database()
    db.connect()
    yield db
    db.disconnect()

@pytest.fixture
def sample_user():
    return {"name": "Alice", "email": "alice@test.com"}
```

---

## Part 6: Parametrized Tests

Run the same test with different inputs.

```python
import pytest

def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]

@pytest.mark.parametrize("input,expected", [
    ("radar", True),
    ("hello", False),
    ("A man a plan a canal Panama", True),
    ("", True),
    ("a", True),
])
def test_is_palindrome(input, expected):
    assert is_palindrome(input) == expected

# Multiple parameters
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

---

## Part 7: Markers

### Built-in Markers

```python
import pytest

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_feature():
    pass

@pytest.mark.xfail(reason="Known bug")
def test_known_failure():
    assert 1 == 2  # Expected to fail
```

### Custom Markers

```python
# pytest.ini
# [pytest]
# markers =
#     slow: marks tests as slow
#     integration: marks tests as integration tests

import pytest

@pytest.mark.slow
def test_slow_operation():
    import time
    time.sleep(5)

@pytest.mark.integration
def test_database_connection():
    pass
```

```bash
# Run only slow tests
pytest -m slow

# Exclude slow tests
pytest -m "not slow"

# Run slow or integration tests
pytest -m "slow or integration"
```

---

## Part 8: Mocking

Replace parts of code during testing.

```python
from unittest.mock import Mock, patch, MagicMock

# Basic Mock
def test_mock_basic():
    mock = Mock()
    mock.method.return_value = 42

    result = mock.method()

    assert result == 42
    mock.method.assert_called_once()

# Patching
def get_data_from_api():
    import requests
    response = requests.get("https://api.example.com/data")
    return response.json()

def test_api_call():
    with patch("requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"key": "value"}

        result = get_data_from_api()

        assert result == {"key": "value"}
        mock_get.assert_called_once_with("https://api.example.com/data")

# Decorator style
@patch("requests.get")
def test_api_call_decorator(mock_get):
    mock_get.return_value.json.return_value = {"key": "value"}
    result = get_data_from_api()
    assert result == {"key": "value"}
```

---

## Part 9: Testing Classes

```python
# bank_account.py
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self._balance += amount
        return self._balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        return amount


# test_bank_account.py
import pytest
from bank_account import BankAccount

class TestBankAccount:

    @pytest.fixture
    def account(self):
        return BankAccount("Alice", 100)

    @pytest.fixture
    def empty_account(self):
        return BankAccount("Bob")

    def test_initial_balance(self, account):
        assert account.balance == 100

    def test_default_balance(self, empty_account):
        assert empty_account.balance == 0

    def test_deposit(self, account):
        result = account.deposit(50)
        assert result == 150
        assert account.balance == 150

    def test_deposit_negative(self, account):
        with pytest.raises(ValueError, match="positive"):
            account.deposit(-10)

    def test_withdraw(self, account):
        result = account.withdraw(30)
        assert result == 30
        assert account.balance == 70

    def test_withdraw_insufficient_funds(self, account):
        with pytest.raises(ValueError, match="Insufficient"):
            account.withdraw(200)

    @pytest.mark.parametrize("deposit_amount,expected", [
        (50, 150),
        (100, 200),
        (0.01, 100.01),
    ])
    def test_multiple_deposits(self, account, deposit_amount, expected):
        account.deposit(deposit_amount)
        assert account.balance == pytest.approx(expected)
```

---

## Part 10: Test Coverage

### Install pytest-cov

```bash
pip install pytest-cov
```

### Run with Coverage

```bash
# Basic coverage
pytest --cov=my_module

# With report
pytest --cov=my_module --cov-report=term-missing

# HTML report
pytest --cov=my_module --cov-report=html

# Minimum coverage requirement
pytest --cov=my_module --cov-fail-under=80
```

### Coverage Configuration

```ini
# pytest.ini or setup.cfg
[coverage:run]
source = src
omit = */tests/*

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
```

---

## Week 11 Project: Testing Bank Account Classes

Complete test suite for the Bank Account from Week 6-7:

```python
# test_bank_account.py
import pytest
from datetime import datetime
from bank_account import BankAccount, SavingsAccount, CheckingAccount

class TestBankAccount:
    """Tests for base BankAccount class."""

    @pytest.fixture
    def account(self):
        """Create a basic account for testing."""
        return BankAccount("Alice", 1000)

    @pytest.fixture
    def empty_account(self):
        """Create an empty account for testing."""
        return BankAccount("Bob", 0)

    # Initialization tests
    def test_create_account(self, account):
        assert account.owner == "Alice"
        assert account.balance == 1000

    def test_create_account_default_balance(self):
        account = BankAccount("Test")
        assert account.balance == 0

    def test_create_account_negative_balance(self):
        with pytest.raises(ValueError, match="negative"):
            BankAccount("Test", -100)

    # Deposit tests
    def test_deposit_positive(self, account):
        result = account.deposit(500)
        assert result == 1500
        assert account.balance == 1500

    def test_deposit_zero(self, account):
        with pytest.raises(ValueError, match="positive"):
            account.deposit(0)

    def test_deposit_negative(self, account):
        with pytest.raises(ValueError, match="positive"):
            account.deposit(-100)

    @pytest.mark.parametrize("amount,expected", [
        (100, 1100),
        (0.01, 1000.01),
        (99999, 100999),
    ])
    def test_deposit_various_amounts(self, account, amount, expected):
        account.deposit(amount)
        assert account.balance == pytest.approx(expected)

    # Withdrawal tests
    def test_withdraw_valid(self, account):
        result = account.withdraw(300)
        assert result == 300
        assert account.balance == 700

    def test_withdraw_all(self, account):
        account.withdraw(1000)
        assert account.balance == 0

    def test_withdraw_insufficient_funds(self, account):
        with pytest.raises(ValueError, match="Insufficient"):
            account.withdraw(2000)

    def test_withdraw_from_empty(self, empty_account):
        with pytest.raises(ValueError):
            empty_account.withdraw(1)

    def test_withdraw_negative(self, account):
        with pytest.raises(ValueError, match="positive"):
            account.withdraw(-100)

    def test_withdraw_zero(self, account):
        with pytest.raises(ValueError, match="positive"):
            account.withdraw(0)

    # Transaction history tests
    def test_transaction_recorded(self, account):
        account.deposit(100)
        assert len(account._transactions) > 0

    def test_multiple_transactions(self, account):
        initial_count = len(account._transactions)
        account.deposit(100)
        account.withdraw(50)
        account.deposit(200)
        assert len(account._transactions) == initial_count + 3


class TestSavingsAccount:
    """Tests for SavingsAccount class."""

    @pytest.fixture
    def savings(self):
        return SavingsAccount("Alice", 1000, interest_rate=0.05)

    def test_create_savings_account(self, savings):
        assert savings.owner == "Alice"
        assert savings.balance == 1000
        assert savings.interest_rate == 0.05

    def test_apply_interest(self, savings):
        # Monthly interest = 0.05 / 12 = ~0.00417
        interest = savings.apply_interest()
        expected_interest = 1000 * (0.05 / 12)
        assert interest == pytest.approx(expected_interest)
        assert savings.balance == pytest.approx(1000 + expected_interest)

    def test_minimum_balance_enforcement(self, savings):
        # Try to withdraw below minimum balance
        with pytest.raises(ValueError, match="[Mm]inimum"):
            savings.withdraw(950)  # Would leave < $100

    def test_withdraw_respects_minimum(self, savings):
        # Should be able to withdraw down to minimum
        savings.withdraw(900)  # Leaves exactly $100
        assert savings.balance == 100

    @pytest.mark.parametrize("rate", [0.01, 0.05, 0.10])
    def test_different_interest_rates(self, rate):
        account = SavingsAccount("Test", 1000, interest_rate=rate)
        interest = account.apply_interest()
        expected = 1000 * (rate / 12)
        assert interest == pytest.approx(expected)


class TestCheckingAccount:
    """Tests for CheckingAccount class."""

    @pytest.fixture
    def checking(self):
        return CheckingAccount("Bob", 500, overdraft_limit=200)

    def test_create_checking_account(self, checking):
        assert checking.owner == "Bob"
        assert checking.balance == 500
        assert checking.overdraft_limit == 200

    def test_available_balance(self, checking):
        assert checking.available_balance == 700  # 500 + 200

    def test_overdraft_allowed(self, checking):
        checking.withdraw(600)  # Uses $100 of overdraft
        assert checking.balance < 0

    def test_overdraft_limit_enforced(self, checking):
        with pytest.raises(ValueError, match="[Oo]verdraft|[Ee]xceeds"):
            checking.withdraw(800)  # Exceeds limit

    def test_overdraft_fee_applied(self, checking):
        checking.withdraw(600)  # Goes into overdraft
        # Fee should be applied
        assert checking.balance < -100  # 500 - 600 - fee


class TestTransfer:
    """Tests for transfers between accounts."""

    @pytest.fixture
    def alice_account(self):
        return BankAccount("Alice", 1000)

    @pytest.fixture
    def bob_account(self):
        return BankAccount("Bob", 500)

    def test_transfer_success(self, alice_account, bob_account):
        alice_account.transfer(bob_account, 300)
        assert alice_account.balance == 700
        assert bob_account.balance == 800

    def test_transfer_insufficient_funds(self, alice_account, bob_account):
        with pytest.raises(ValueError):
            alice_account.transfer(bob_account, 2000)

    def test_transfer_to_invalid_account(self, alice_account):
        with pytest.raises(TypeError):
            alice_account.transfer("not an account", 100)


# Fixtures for integration tests
@pytest.fixture
def bank_system():
    """Create a mini banking system for integration tests."""
    accounts = {
        "alice": SavingsAccount("Alice", 5000, 0.03),
        "bob": CheckingAccount("Bob", 1000, 500),
        "charlie": BankAccount("Charlie", 2000),
    }
    return accounts


class TestBankingIntegration:
    """Integration tests for banking system."""

    def test_multiple_transfers(self, bank_system):
        accounts = bank_system

        # Series of transfers
        accounts["alice"].transfer(accounts["bob"], 500)
        accounts["bob"].transfer(accounts["charlie"], 300)
        accounts["charlie"].transfer(accounts["alice"], 100)

        assert accounts["alice"].balance == pytest.approx(4600)
        assert accounts["bob"].balance == pytest.approx(1200)
        assert accounts["charlie"].balance == pytest.approx(2200)

    def test_interest_on_multiple_accounts(self, bank_system):
        # Apply interest to savings account
        bank_system["alice"].apply_interest()

        # Others shouldn't have interest method (or it does nothing)
        initial_bob = bank_system["bob"].balance
        if hasattr(bank_system["bob"], "apply_interest"):
            bank_system["bob"].apply_interest()
        # Bob's balance unchanged (checking accounts typically don't earn interest)
```

### Running the Tests

```bash
# Run all tests
pytest test_bank_account.py -v

# Run with coverage
pytest test_bank_account.py --cov=bank_account --cov-report=term-missing

# Run specific test class
pytest test_bank_account.py::TestSavingsAccount -v

# Run tests matching pattern
pytest test_bank_account.py -k "deposit" -v
```

---

## Key Takeaways

1. **pytest** is the standard Python testing framework
2. Test files: `test_*.py`, test functions: `test_*`
3. Use **assert** for simple assertions
4. **Fixtures** provide reusable test setup
5. **@pytest.mark.parametrize** for testing multiple inputs
6. **pytest.raises** for testing exceptions
7. **Mocking** isolates code from external dependencies
8. **Coverage** shows what code is tested

---

## Next Week Preview
Week 12 covers debugging techniques: using pdb, IDE debuggers, and reading tracebacks.
