# Week 31: Code Quality

## Overview
This week covers writing professional-quality Python code: PEP 8 style guide, linting, type hints, and documentation.

---

## Part 1: PEP 8 Style Guide

### Naming Conventions

```python
# Variables and functions: snake_case
user_name = "Alice"
def calculate_total():
    pass

# Classes: PascalCase
class UserAccount:
    pass

# Constants: UPPERCASE
MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 30

# Private: leading underscore
_internal_variable = "private"
def _helper_function():
    pass

# "Really private": double underscore
__very_private = "name mangled"
```

### Indentation and Line Length

```python
# 4 spaces for indentation (not tabs)
def my_function():
    if condition:
        do_something()

# Max 79 characters per line (code)
# Max 72 characters (docstrings/comments)

# Line continuation
long_variable = (
    first_value +
    second_value +
    third_value
)

# Function with many parameters
def function_with_many_args(
    first_arg,
    second_arg,
    third_arg,
    fourth_arg
):
    pass
```

### Whitespace

```python
# Good
spam(ham[1], {eggs: 2})
foo = (0,)
x = 1
y = 2
def complex(real, imag=0.0):
    return magic(r=real, i=imag)

# Bad
spam( ham[ 1 ], { eggs: 2 } )
foo = (0, )
x=1
y=2
def complex(real, imag = 0.0):
    return magic(r = real, i = imag)
```

### Imports

```python
# Imports at top of file
# Standard library first, then third-party, then local
import os
import sys

import requests
import numpy as np

from myproject import utils
from myproject.models import User

# Avoid wildcard imports
from module import *  # Bad
from module import specific_function  # Good
```

---

## Part 2: Linting with Flake8/Ruff

### Installation

```bash
pip install flake8
# Or the faster alternative
pip install ruff
```

### Running Linters

```bash
# Flake8
flake8 my_file.py
flake8 my_project/

# Ruff
ruff check my_file.py
ruff check my_project/
```

### Configuration

```ini
# setup.cfg or .flake8
[flake8]
max-line-length = 100
exclude = .git,__pycache__,venv
ignore = E501,W503
```

```toml
# pyproject.toml (for ruff)
[tool.ruff]
line-length = 100
exclude = [".git", "__pycache__", "venv"]
ignore = ["E501"]
```

### Common Error Codes

| Code | Description |
|------|-------------|
| E101 | Mixed tabs and spaces |
| E302 | Expected 2 blank lines |
| E501 | Line too long |
| E711 | Comparison to None |
| F401 | Imported but unused |
| F841 | Local variable unused |
| W292 | No newline at end of file |

---

## Part 3: Code Formatting with Black

### Installation

```bash
pip install black
```

### Usage

```bash
# Format file
black my_file.py

# Check without modifying
black --check my_file.py

# Format directory
black my_project/
```

### Configuration

```toml
# pyproject.toml
[tool.black]
line-length = 100
target-version = ['py310']
exclude = '''
/(
    \.git
    | venv
    | __pycache__
)/
'''
```

---

## Part 4: Type Hints

### Basic Type Hints

```python
def greet(name: str) -> str:
    return f"Hello, {name}"

def add(a: int, b: int) -> int:
    return a + b

# Variables
age: int = 25
name: str = "Alice"
is_active: bool = True
price: float = 19.99
```

### Complex Types

```python
from typing import List, Dict, Optional, Union, Tuple, Callable

# Lists
def process_items(items: List[str]) -> List[str]:
    return [item.upper() for item in items]

# Dictionaries
def get_config() -> Dict[str, int]:
    return {"timeout": 30, "retries": 3}

# Optional (can be None)
def find_user(id: int) -> Optional[str]:
    if id == 1:
        return "Alice"
    return None

# Union (multiple types)
def process(value: Union[int, str]) -> str:
    return str(value)

# Tuple
def get_coordinates() -> Tuple[float, float]:
    return (1.0, 2.0)

# Callable
def apply_func(func: Callable[[int], int], value: int) -> int:
    return func(value)
```

### Type Aliases and TypedDict

```python
from typing import List, TypedDict

# Type alias
UserId = int
UserIds = List[int]

def get_users(ids: UserIds) -> List[str]:
    pass

# TypedDict for dictionary structure
class UserDict(TypedDict):
    name: str
    age: int
    email: str

def create_user(data: UserDict) -> None:
    print(data["name"])
```

### Type Checking with mypy

```bash
pip install mypy
mypy my_file.py
```

---

## Part 5: Docstrings

### Google Style (Recommended)

```python
def calculate_total(items: List[float], tax_rate: float = 0.1) -> float:
    """Calculate the total price including tax.

    Args:
        items: List of item prices.
        tax_rate: Tax rate as decimal (default 0.1 for 10%).

    Returns:
        Total price including tax.

    Raises:
        ValueError: If items list is empty.
        TypeError: If items contains non-numeric values.

    Example:
        >>> calculate_total([10.0, 20.0, 30.0])
        66.0
    """
    if not items:
        raise ValueError("Items list cannot be empty")

    subtotal = sum(items)
    return subtotal * (1 + tax_rate)
```

### Class Docstrings

```python
class BankAccount:
    """A simple bank account.

    This class represents a bank account with basic operations
    like deposit and withdrawal.

    Attributes:
        owner: Account owner's name.
        balance: Current account balance.

    Example:
        >>> account = BankAccount("Alice", 100)
        >>> account.deposit(50)
        150
    """

    def __init__(self, owner: str, balance: float = 0):
        """Initialize a new bank account.

        Args:
            owner: Account owner's name.
            balance: Initial balance (default 0).
        """
        self.owner = owner
        self.balance = balance
```

---

## Part 6: Pre-commit Hooks

### Installation

```bash
pip install pre-commit
```

### Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.270
    hooks:
      - id: ruff

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
```

### Setup

```bash
# Install hooks
pre-commit install

# Run on all files
pre-commit run --all-files
```

---

## Part 7: Refactoring Example

### Before

```python
def process(d):
    r = []
    for i in d:
        if i['active'] == True:
            n = i['first_name'] + ' ' + i['last_name']
            r.append({'name': n, 'email': i['email']})
    return r
```

### After

```python
from typing import List, TypedDict

class UserInput(TypedDict):
    first_name: str
    last_name: str
    email: str
    active: bool

class UserOutput(TypedDict):
    name: str
    email: str

def process_active_users(users: List[UserInput]) -> List[UserOutput]:
    """Extract active users with formatted names.

    Args:
        users: List of user dictionaries with user data.

    Returns:
        List of active users with combined name and email.
    """
    return [
        {
            "name": f"{user['first_name']} {user['last_name']}",
            "email": user["email"]
        }
        for user in users
        if user["active"]
    ]
```

---

## Week 31 Project: Refactor a Past Project

Choose one of your past projects and apply code quality standards:

1. **Run linters** and fix all issues
2. **Format with Black**
3. **Add type hints** to all functions
4. **Write docstrings** for all public functions/classes
5. **Set up pre-commit hooks**
6. **Create pyproject.toml** with tool configurations

---

## Key Takeaways

1. Follow **PEP 8** style guide
2. Use **linters** (flake8, ruff) to catch issues
3. **Format** code with Black
4. Add **type hints** for clarity
5. Write **docstrings** for documentation
6. Use **pre-commit hooks** for automation
7. **Refactor** for readability
8. Code quality is an **ongoing practice**

---

## Next Week Preview
Week 32 covers advanced testing: mocking, fixtures, and coverage.
