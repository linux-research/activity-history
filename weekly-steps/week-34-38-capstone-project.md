# Weeks 34-38: Capstone Project

## Overview
Over these five weeks, build one substantial project combining skills from all three tracks. The project should solve a real problem and demonstrate professional Python development.

---

## Project Requirements

Your capstone must include:

- [ ] **Clean code** following PEP 8
- [ ] **Type hints** on all functions
- [ ] **Docstrings** for public APIs
- [ ] **Classes** with proper OOP design
- [ ] **File or database I/O**
- [ ] **Error handling** throughout
- [ ] **Unit tests** with 80%+ coverage
- [ ] **Configuration management**
- [ ] **CLI or web interface**
- [ ] **Documentation** (README, docstrings)
- [ ] **Git** with meaningful commits

---

## Week 34: Planning and Design

### Define the Problem
- What problem does your project solve?
- Who is the target user?
- What are the key features?

### Technical Design
- What packages will you use?
- How will data flow through the system?
- What's the project structure?

### Create Skeleton

```
my_capstone/
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── config.py
│       ├── models/
│       ├── services/
│       └── utils/
├── tests/
│   ├── conftest.py
│   └── test_*.py
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
└── requirements.txt
```

---

## Week 35-36: Core Implementation

### Build Core Features
- Implement main functionality
- Write tests as you go
- Use version control regularly

### Example: Data Pipeline Project

```python
# src/pipeline/models.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class DataRecord:
    """Represents a single data record."""
    id: str
    source: str
    data: dict
    created_at: datetime
    processed_at: Optional[datetime] = None

@dataclass
class PipelineResult:
    """Result of a pipeline run."""
    records_processed: int
    records_failed: int
    duration_seconds: float
    errors: List[str]
```

```python
# src/pipeline/services/processor.py
from typing import List, Callable
from pipeline.models import DataRecord, PipelineResult
import time
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    """Process data through transformation pipeline."""

    def __init__(self):
        self.transformers: List[Callable] = []
        self.validators: List[Callable] = []

    def add_transformer(self, func: Callable) -> "DataProcessor":
        """Add a transformation function."""
        self.transformers.append(func)
        return self

    def add_validator(self, func: Callable) -> "DataProcessor":
        """Add a validation function."""
        self.validators.append(func)
        return self

    def process(self, records: List[DataRecord]) -> PipelineResult:
        """Process all records through the pipeline."""
        start_time = time.time()
        processed = 0
        failed = 0
        errors = []

        for record in records:
            try:
                # Validate
                for validator in self.validators:
                    if not validator(record):
                        raise ValueError(f"Validation failed for {record.id}")

                # Transform
                for transformer in self.transformers:
                    record = transformer(record)

                record.processed_at = datetime.now()
                processed += 1

            except Exception as e:
                failed += 1
                errors.append(f"{record.id}: {str(e)}")
                logger.error(f"Failed to process {record.id}: {e}")

        return PipelineResult(
            records_processed=processed,
            records_failed=failed,
            duration_seconds=time.time() - start_time,
            errors=errors
        )
```

---

## Week 37: Testing and Refinement

### Comprehensive Testing

```python
# tests/test_processor.py
import pytest
from datetime import datetime
from pipeline.models import DataRecord
from pipeline.services.processor import DataProcessor

@pytest.fixture
def sample_records():
    return [
        DataRecord(
            id="1",
            source="test",
            data={"value": 100},
            created_at=datetime.now()
        ),
        DataRecord(
            id="2",
            source="test",
            data={"value": 200},
            created_at=datetime.now()
        ),
    ]

@pytest.fixture
def processor():
    return DataProcessor()

class TestDataProcessor:

    def test_empty_pipeline(self, processor, sample_records):
        result = processor.process(sample_records)
        assert result.records_processed == 2
        assert result.records_failed == 0

    def test_with_transformer(self, processor, sample_records):
        def double_value(record):
            record.data["value"] *= 2
            return record

        processor.add_transformer(double_value)
        processor.process(sample_records)

        assert sample_records[0].data["value"] == 200

    def test_validation_failure(self, processor, sample_records):
        def reject_all(record):
            return False

        processor.add_validator(reject_all)
        result = processor.process(sample_records)

        assert result.records_failed == 2
        assert result.records_processed == 0

    def test_partial_failure(self, processor, sample_records):
        def fail_on_id_2(record):
            if record.id == "2":
                raise ValueError("Intentional failure")
            return record

        processor.add_transformer(fail_on_id_2)
        result = processor.process(sample_records)

        assert result.records_processed == 1
        assert result.records_failed == 1
```

### Add Integration Tests

```python
# tests/integration/test_full_pipeline.py
import pytest
from pipeline import create_pipeline
from pipeline.connectors import CSVSource, JSONSink

class TestFullPipeline:

    @pytest.fixture
    def test_data_file(self, tmp_path):
        csv_file = tmp_path / "input.csv"
        csv_file.write_text("id,value\n1,100\n2,200\n")
        return csv_file

    def test_csv_to_json_pipeline(self, test_data_file, tmp_path):
        output_file = tmp_path / "output.json"

        pipeline = create_pipeline(
            source=CSVSource(test_data_file),
            sink=JSONSink(output_file)
        )

        result = pipeline.run()

        assert result.records_processed == 2
        assert output_file.exists()
```

---

## Week 38: Documentation and Deployment

### Write README

```markdown
# My Capstone Project

A data processing pipeline for transforming and validating records.

## Features

- Flexible transformation pipeline
- Custom validators
- Multiple input/output formats
- Comprehensive logging

## Installation

\`\`\`bash
pip install my-capstone
\`\`\`

## Quick Start

\`\`\`python
from pipeline import create_pipeline

pipeline = create_pipeline()
pipeline.add_transformer(my_transform)
result = pipeline.run()
\`\`\`

## CLI Usage

\`\`\`bash
# Process a file
myapp process input.csv -o output.json

# Validate only
myapp validate input.csv

# Show stats
myapp stats
\`\`\`

## Configuration

Create a `.env` file:

\`\`\`
LOG_LEVEL=INFO
OUTPUT_FORMAT=json
\`\`\`

## Development

\`\`\`bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src tests

# Type check
mypy src
\`\`\`

## License

MIT License
```

### Create Deployment Script

```python
#!/usr/bin/env python3
# scripts/deploy.py
import subprocess
import sys

def run(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        sys.exit(1)

def main():
    # Run tests
    run("pytest --cov=my_project --cov-fail-under=80")

    # Format check
    run("black --check src tests")

    # Type check
    run("mypy src")

    # Build
    run("python -m build")

    print("Ready for deployment!")

if __name__ == "__main__":
    main()
```

---

## Example Capstone Ideas

### 1. Web Dashboard with Data Pipeline
- Scrape data from APIs
- Store in database
- Create Flask dashboard
- Schedule daily updates
- Send email alerts

### 2. Personal Finance Tracker
- CLI for adding transactions
- SQLite database
- Category analysis
- Monthly reports
- Budget alerts

### 3. Document Processing System
- PDF/Word parsing
- Text extraction and analysis
- Keyword search
- Export to multiple formats
- Web interface

### 4. Automated Testing Framework
- Discover and run tests
- Generate reports
- Compare results over time
- Email notifications

---

## Evaluation Checklist

### Code Quality
- [ ] PEP 8 compliant
- [ ] Type hints throughout
- [ ] Meaningful variable names
- [ ] No code duplication

### Testing
- [ ] Unit tests for all modules
- [ ] Integration tests
- [ ] 80%+ coverage
- [ ] Edge cases covered

### Documentation
- [ ] Comprehensive README
- [ ] API documentation
- [ ] Usage examples
- [ ] Installation guide

### Project Structure
- [ ] Proper package structure
- [ ] Configuration separated
- [ ] Dependencies specified
- [ ] Git history clean

### Functionality
- [ ] Core features work
- [ ] Error handling complete
- [ ] Logging implemented
- [ ] CLI/interface polished

---

## Key Takeaways

1. **Plan before coding**
2. **Build incrementally**
3. **Test as you go**
4. **Refactor regularly**
5. **Document everything**
6. **Get feedback**
7. **Iterate and improve**

---

## Next Week Preview
Week 39 covers polish and deployment.
