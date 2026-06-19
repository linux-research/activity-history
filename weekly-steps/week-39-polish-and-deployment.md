# Week 39: Polish and Deployment

## Overview
This week covers finalizing your capstone: polishing code, writing documentation, and deploying so others can use it.

---

## Part 1: Final Code Review

### Checklist

```markdown
## Code Review Checklist

### Style
- [ ] Follows PEP 8
- [ ] Consistent naming conventions
- [ ] No unused imports/variables
- [ ] Line length under 100 chars

### Quality
- [ ] Functions are small and focused
- [ ] Classes have single responsibility
- [ ] No code duplication (DRY)
- [ ] Error handling is comprehensive

### Documentation
- [ ] All public functions have docstrings
- [ ] Complex logic has comments
- [ ] Type hints on all functions
- [ ] README is complete

### Testing
- [ ] All tests pass
- [ ] Coverage > 80%
- [ ] Edge cases covered
- [ ] Integration tests exist
```

### Run All Checks

```bash
#!/bin/bash
# scripts/check.sh

echo "Running checks..."

echo "1. Format check..."
black --check src tests || exit 1

echo "2. Lint..."
ruff check src tests || exit 1

echo "3. Type check..."
mypy src || exit 1

echo "4. Tests..."
pytest --cov=mypackage --cov-fail-under=80 || exit 1

echo "All checks passed!"
```

---

## Part 2: Complete Documentation

### README Template

```markdown
# Project Name

Short description of what the project does.

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

\`\`\`bash
pip install my-project
\`\`\`

### From source

\`\`\`bash
git clone https://github.com/user/project.git
cd project
pip install -e .
\`\`\`

## Quick Start

\`\`\`python
from myproject import main

result = main.process("input.txt")
print(result)
\`\`\`

## CLI Usage

\`\`\`bash
myproject --help
myproject process input.txt -o output.json
\`\`\`

## Configuration

Environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| LOG_LEVEL | Logging level | INFO |
| OUTPUT_DIR | Output directory | ./output |

## Development

\`\`\`bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src tests

# Check types
mypy src
\`\`\`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License - see LICENSE file
```

### API Documentation

```python
# Use pdoc or sphinx for auto-generated docs

# Install pdoc
pip install pdoc

# Generate HTML docs
pdoc --html src/mypackage -o docs/

# Or use docstrings like this:
def process_data(
    input_path: str,
    output_path: str,
    *,
    format: str = "json",
    validate: bool = True
) -> ProcessResult:
    """Process data from input file and write to output.

    This function reads data from the input file, applies
    transformations, validates the result, and writes to
    the output file.

    Args:
        input_path: Path to input file. Must exist.
        output_path: Path to output file. Will be created.
        format: Output format. One of 'json', 'csv'.
        validate: Whether to validate output.

    Returns:
        ProcessResult containing statistics about the run.

    Raises:
        FileNotFoundError: If input_path doesn't exist.
        ValueError: If format is not supported.
        ValidationError: If validation fails.

    Example:
        >>> result = process_data("data.csv", "out.json")
        >>> print(result.records_processed)
        100

    Note:
        Large files may take significant time to process.
    """
```

---

## Part 3: Packaging for Distribution

### pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "my-project"
version = "1.0.0"
description = "My capstone project"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.10"
authors = [
    {name = "Your Name", email = "you@example.com"}
]
dependencies = [
    "click>=8.0",
    "requests>=2.28",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "black>=23.0",
    "mypy>=1.0",
    "ruff>=0.0.270",
]

[project.scripts]
myproject = "myproject.cli:main"

[project.urls]
Homepage = "https://github.com/user/project"
```

### Build Package

```bash
# Install build tools
pip install build twine

# Build
python -m build

# Check the package
twine check dist/*

# Upload to PyPI (when ready)
twine upload dist/*
```

---

## Part 4: Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY src/ ./src/
COPY pyproject.toml .

# Install package
RUN pip install .

# Run
CMD ["myproject", "run"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    environment:
      - LOG_LEVEL=INFO
      - DATABASE_URL=postgresql://db:5432/myapp
    volumes:
      - ./data:/app/data
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_PASSWORD=secret
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Build and Run

```bash
# Build
docker build -t myproject .

# Run
docker run -it myproject

# With docker-compose
docker-compose up -d
```

---

## Part 5: GitHub Actions CI/CD

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11']

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"

    - name: Format check
      run: black --check src tests

    - name: Lint
      run: ruff check src tests

    - name: Type check
      run: mypy src

    - name: Test
      run: pytest --cov=mypackage --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

---

## Part 6: Deployment Options

### Option 1: PyPI
- For Python libraries/tools
- `pip install my-package`

### Option 2: Docker Hub
- For containerized apps
- `docker pull user/myapp`

### Option 3: Cloud Platforms
- Heroku
- AWS Lambda
- Google Cloud Run
- DigitalOcean App Platform

### Option 4: Self-hosted
- VPS with systemd service
- Docker on any server

---

## Week 39 Checklist

- [ ] All code review items addressed
- [ ] README is comprehensive
- [ ] docstrings on all public functions
- [ ] pyproject.toml complete
- [ ] CI/CD pipeline working
- [ ] Package builds successfully
- [ ] Docker works (if applicable)
- [ ] Deployed and accessible

---

## Key Takeaways

1. **Polish before shipping**
2. **Documentation is critical**
3. **Automate testing and deployment**
4. **Package properly** for distribution
5. **Docker** simplifies deployment
6. **CI/CD** catches issues early
7. **Make installation easy**
8. **Test the deployed version**

---

## Next Week Preview
Week 40: Reflection and planning next steps.
