# Week 33: Project Architecture

## Overview
This week covers proper project structure, configuration management, and building CLI tools.

---

## Part 1: Project Structure

### Basic Structure

```
my_project/
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── user.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── user_service.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_models/
│   └── test_services/
├── docs/
├── scripts/
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
└── requirements.txt
```

### Advanced Structure

```
my_project/
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── __main__.py      # For python -m my_package
│       ├── cli.py           # CLI entry point
│       ├── config.py        # Configuration
│       ├── exceptions.py    # Custom exceptions
│       ├── api/
│       │   ├── __init__.py
│       │   └── routes.py
│       ├── core/
│       │   ├── __init__.py
│       │   └── logic.py
│       ├── db/
│       │   ├── __init__.py
│       │   ├── connection.py
│       │   └── models.py
│       └── utils/
│           └── __init__.py
├── tests/
│   ├── unit/
│   └── integration/
├── docker/
│   └── Dockerfile
├── .github/
│   └── workflows/
│       └── ci.yml
└── pyproject.toml
```

---

## Part 2: Configuration Management

### Using dataclasses

```python
# config.py
from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    name: str = "myapp"
    user: str = "postgres"
    password: str = ""

    @property
    def url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

@dataclass
class AppConfig:
    debug: bool = False
    secret_key: str = "change-me"
    log_level: str = "INFO"

@dataclass
class Config:
    app: AppConfig
    database: DatabaseConfig

def load_config() -> Config:
    return Config(
        app=AppConfig(
            debug=os.getenv("DEBUG", "false").lower() == "true",
            secret_key=os.getenv("SECRET_KEY", "change-me"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        ),
        database=DatabaseConfig(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            name=os.getenv("DB_NAME", "myapp"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", ""),
        ),
    )

# Usage
config = load_config()
print(config.database.url)
```

### Using Pydantic

```python
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    debug: bool = False
    secret_key: str = Field(..., env="SECRET_KEY")

    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "myapp"
    db_user: str = "postgres"
    db_password: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

settings = Settings()
```

---

## Part 3: CLI with argparse

```python
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="My CLI Application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s process input.csv -o output.csv
  %(prog)s analyze data/ --verbose
        """
    )

    # Positional argument
    parser.add_argument("input", help="Input file path")

    # Optional arguments
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--format", choices=["json", "csv"], default="json")
    parser.add_argument("-n", "--count", type=int, default=10, help="Number of items")

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Process command
    process_parser = subparsers.add_parser("process", help="Process files")
    process_parser.add_argument("files", nargs="+", help="Files to process")

    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze data")
    analyze_parser.add_argument("--deep", action="store_true")

    args = parser.parse_args()

    if args.command == "process":
        process_files(args.files, verbose=args.verbose)
    elif args.command == "analyze":
        analyze_data(deep=args.deep)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
```

---

## Part 4: CLI with Click

```python
import click

@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def cli(ctx, debug):
    """My CLI Application."""
    ctx.ensure_object(dict)
    ctx.obj["DEBUG"] = debug

@cli.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), help="Output file")
@click.option("-f", "--format", type=click.Choice(["json", "csv"]), default="json")
@click.pass_context
def process(ctx, input_file, output, format):
    """Process a file."""
    if ctx.obj["DEBUG"]:
        click.echo(f"Debug mode: processing {input_file}")

    click.echo(f"Processing {input_file} to {output} as {format}")

@cli.command()
@click.argument("directory", type=click.Path(exists=True))
@click.option("--recursive", "-r", is_flag=True, help="Recursive analysis")
@click.option("--depth", type=int, default=1, help="Analysis depth")
def analyze(directory, recursive, depth):
    """Analyze a directory."""
    click.echo(f"Analyzing {directory}")
    click.echo(f"Recursive: {recursive}, Depth: {depth}")

@cli.command()
@click.confirmation_option(prompt="Are you sure you want to reset?")
def reset():
    """Reset the application."""
    click.echo("Resetting...")

if __name__ == "__main__":
    cli()
```

---

## Part 5: pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
version = "0.1.0"
description = "My Python package"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "you@example.com"}
]
keywords = ["python", "cli", "tool"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
]
dependencies = [
    "click>=8.0",
    "requests>=2.28",
    "pydantic>=1.10",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=23.0",
    "ruff>=0.0.270",
    "mypy>=1.0",
]

[project.scripts]
myapp = "my_package.cli:main"

[project.urls]
Homepage = "https://github.com/username/my-package"
Documentation = "https://my-package.readthedocs.io"
Repository = "https://github.com/username/my-package"

[tool.setuptools.packages.find]
where = ["src"]

[tool.black]
line-length = 100
target-version = ["py310"]

[tool.ruff]
line-length = 100
select = ["E", "F", "W", "I"]

[tool.mypy]
python_version = "3.10"
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --cov=my_package"
```

---

## Part 6: Entry Points

### __main__.py

```python
# src/my_package/__main__.py
"""Allow running as python -m my_package."""
from my_package.cli import main

if __name__ == "__main__":
    main()
```

### Installation

```bash
# Install in development mode
pip install -e .

# Now you can run
myapp --help
python -m my_package --help
```

---

## Part 7: Dependency Injection

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

# Interface
class UserRepository(ABC):
    @abstractmethod
    def get(self, user_id: int):
        pass

    @abstractmethod
    def save(self, user):
        pass

# Implementation
class SQLUserRepository(UserRepository):
    def __init__(self, db_session):
        self.db = db_session

    def get(self, user_id: int):
        return self.db.query(User).get(user_id)

    def save(self, user):
        self.db.add(user)
        self.db.commit()

# Service using the interface
class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_user(self, user_id: int):
        return self.user_repo.get(user_id)

# Dependency container
@dataclass
class Container:
    db_session: Any
    user_repo: UserRepository = None
    user_service: UserService = None

    def __post_init__(self):
        self.user_repo = SQLUserRepository(self.db_session)
        self.user_service = UserService(self.user_repo)

# Usage
container = Container(db_session=create_session())
user = container.user_service.get_user(1)
```

---

## Week 33 Project: Restructure a Project

Take a past project and restructure it with proper architecture:

1. Create proper package structure
2. Separate configuration from code
3. Add CLI interface
4. Create pyproject.toml
5. Make it installable with pip

---

## Key Takeaways

1. **Organize code** into logical modules
2. **Separate configuration** from code
3. **Use environment variables** for secrets
4. **pyproject.toml** is the modern standard
5. **Click** or **argparse** for CLI
6. **Entry points** make packages runnable
7. **Dependency injection** improves testability
8. Good structure **scales** as project grows

---

## Next Week Preview
Weeks 34-38: Build a capstone project combining multiple skills.
