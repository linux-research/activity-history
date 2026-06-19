# Week 9: Working with CSV and JSON

## Overview
This week covers reading and writing structured data formats: CSV (Comma-Separated Values) for tabular data and JSON (JavaScript Object Notation) for hierarchical data.

---

## Part 1: CSV Basics

CSV files store tabular data in plain text:

```
name,age,city
Alice,30,New York
Bob,25,Los Angeles
Charlie,35,Chicago
```

### Reading CSV Files

```python
import csv

# Method 1: csv.reader (returns lists)
with open("data.csv", "r") as file:
    reader = csv.reader(file)
    header = next(reader)  # Skip header row
    for row in reader:
        name, age, city = row
        print(f"{name} is {age} years old")

# Method 2: csv.DictReader (returns dictionaries)
with open("data.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(f"{row['name']} lives in {row['city']}")
```

### Writing CSV Files

```python
import csv

# Method 1: csv.writer
data = [
    ["name", "age", "city"],
    ["Alice", 30, "New York"],
    ["Bob", 25, "Los Angeles"]
]

with open("output.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(data)  # Write all rows
    # Or: writer.writerow(row) for single row

# Method 2: csv.DictWriter
data = [
    {"name": "Alice", "age": 30, "city": "New York"},
    {"name": "Bob", "age": 25, "city": "Los Angeles"}
]

with open("output.csv", "w", newline="") as file:
    fieldnames = ["name", "age", "city"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
```

### CSV Options

```python
import csv

# Custom delimiter (e.g., tab-separated)
with open("data.tsv", "r") as file:
    reader = csv.reader(file, delimiter="\t")
    for row in reader:
        print(row)

# Handle quotes and special characters
with open("data.csv", "w", newline="") as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    writer.writerow(["Name", "Description"])
    writer.writerow(["Widget", 'Has "special" chars, and commas'])

# Different quote character
reader = csv.reader(file, quotechar="'")
```

---

## Part 2: JSON Basics

JSON stores structured data with nesting support:

```json
{
    "name": "Alice",
    "age": 30,
    "hobbies": ["reading", "coding"],
    "address": {
        "city": "New York",
        "zip": "10001"
    }
}
```

### Reading JSON Files

```python
import json

# From file
with open("data.json", "r") as file:
    data = json.load(file)

print(data["name"])
print(data["hobbies"][0])
print(data["address"]["city"])

# From string
json_string = '{"name": "Alice", "age": 30}'
data = json.loads(json_string)
```

### Writing JSON Files

```python
import json

data = {
    "name": "Alice",
    "age": 30,
    "hobbies": ["reading", "coding"],
    "active": True,
    "balance": None
}

# To file
with open("output.json", "w") as file:
    json.dump(data, file)

# Pretty-printed
with open("output.json", "w") as file:
    json.dump(data, file, indent=2)

# To string
json_string = json.dumps(data, indent=2)
print(json_string)
```

### JSON Options

```python
import json

data = {"name": "Alice", "created": "2024-01-15"}

# Sort keys
json.dumps(data, sort_keys=True)

# Compact output
json.dumps(data, separators=(",", ":"))

# Ensure ASCII (escape non-ASCII characters)
json.dumps({"name": "日本"}, ensure_ascii=False)  # "日本"
json.dumps({"name": "日本"}, ensure_ascii=True)   # "\u65e5\u672c"
```

---

## Part 3: Working with Complex Data

### Lists of Objects

```python
import json

# JSON array of objects
users = [
    {"id": 1, "name": "Alice", "active": True},
    {"id": 2, "name": "Bob", "active": False},
    {"id": 3, "name": "Charlie", "active": True}
]

# Write
with open("users.json", "w") as file:
    json.dump(users, file, indent=2)

# Read and process
with open("users.json", "r") as file:
    users = json.load(file)

active_users = [u for u in users if u["active"]]
print(f"Active users: {len(active_users)}")
```

### Nested Structures

```python
import json

company = {
    "name": "TechCorp",
    "departments": {
        "engineering": {
            "head": "Alice",
            "employees": ["Bob", "Charlie", "Diana"]
        },
        "marketing": {
            "head": "Eve",
            "employees": ["Frank", "Grace"]
        }
    },
    "locations": ["New York", "San Francisco"]
}

# Access nested data
eng_head = company["departments"]["engineering"]["head"]
all_engineers = company["departments"]["engineering"]["employees"]

# Modify nested data
company["departments"]["engineering"]["employees"].append("Henry")
```

---

## Part 4: Custom JSON Encoding

Python objects need custom encoding for JSON:

```python
import json
from datetime import datetime, date
from decimal import Decimal

# Custom encoder class
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)

data = {
    "timestamp": datetime.now(),
    "date": date.today(),
    "price": Decimal("19.99"),
    "tags": {"python", "coding"}
}

# Use custom encoder
json_string = json.dumps(data, cls=CustomEncoder, indent=2)
print(json_string)
```

### Custom Decoding

```python
import json
from datetime import datetime

def custom_decoder(dct):
    """Convert ISO format strings back to datetime."""
    for key, value in dct.items():
        if isinstance(value, str):
            try:
                dct[key] = datetime.fromisoformat(value)
            except ValueError:
                pass
    return dct

json_string = '{"created": "2024-01-15T10:30:00"}'
data = json.loads(json_string, object_hook=custom_decoder)
print(data["created"])  # datetime object
```

---

## Part 5: Converting Between CSV and JSON

### CSV to JSON

```python
import csv
import json

def csv_to_json(csv_file, json_file):
    """Convert CSV file to JSON."""
    data = []

    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Convert numeric strings to numbers
            for key, value in row.items():
                try:
                    row[key] = int(value)
                except ValueError:
                    try:
                        row[key] = float(value)
                    except ValueError:
                        pass
            data.append(row)

    with open(json_file, "w") as file:
        json.dump(data, file, indent=2)

    return len(data)

# Usage
count = csv_to_json("data.csv", "data.json")
print(f"Converted {count} records")
```

### JSON to CSV

```python
import csv
import json

def json_to_csv(json_file, csv_file):
    """Convert JSON array to CSV."""
    with open(json_file, "r") as file:
        data = json.load(file)

    if not data:
        return 0

    # Get field names from first record
    fieldnames = list(data[0].keys())

    with open(csv_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    return len(data)

# Usage
count = json_to_csv("data.json", "data.csv")
print(f"Converted {count} records")
```

---

## Part 6: Data Validation

```python
import json

def validate_user(user):
    """Validate user data structure."""
    required_fields = ["name", "email", "age"]
    errors = []

    # Check required fields
    for field in required_fields:
        if field not in user:
            errors.append(f"Missing required field: {field}")

    # Validate types
    if "name" in user and not isinstance(user["name"], str):
        errors.append("'name' must be a string")

    if "age" in user:
        if not isinstance(user["age"], int):
            errors.append("'age' must be an integer")
        elif user["age"] < 0 or user["age"] > 150:
            errors.append("'age' must be between 0 and 150")

    if "email" in user:
        if not isinstance(user["email"], str):
            errors.append("'email' must be a string")
        elif "@" not in user["email"]:
            errors.append("'email' must contain @")

    return errors

# Usage
user_data = {"name": "Alice", "age": -5, "email": "invalid"}
errors = validate_user(user_data)
if errors:
    print("Validation errors:")
    for error in errors:
        print(f"  - {error}")
```

---

## Part 7: Working with Large Files

### Reading Large CSV Files

```python
import csv

def process_large_csv(filename, chunk_size=1000):
    """Process large CSV in chunks."""
    with open(filename, "r") as file:
        reader = csv.DictReader(file)

        chunk = []
        for i, row in enumerate(reader):
            chunk.append(row)

            if len(chunk) >= chunk_size:
                yield chunk
                chunk = []

        # Yield remaining rows
        if chunk:
            yield chunk

# Usage
for chunk in process_large_csv("big_data.csv"):
    print(f"Processing {len(chunk)} rows")
    # Process chunk...
```

### Streaming JSON

```python
import json

def stream_json_array(filename):
    """Stream large JSON array."""
    with open(filename, "r") as file:
        # Skip opening bracket
        file.read(1)

        buffer = ""
        depth = 0

        for char in iter(lambda: file.read(1), ""):
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1

            if depth > 0 or char == "}":
                buffer += char

            if depth == 0 and buffer:
                if buffer.strip():
                    yield json.loads(buffer)
                buffer = ""
```

---

## Week 9 Project: CSV to JSON Converter Tool

```python
import csv
import json
import os
import sys
from datetime import datetime

def detect_type(value):
    """Detect and convert value to appropriate type."""
    if value == "":
        return None

    # Try boolean
    if value.lower() in ("true", "yes", "1"):
        return True
    if value.lower() in ("false", "no", "0"):
        return False

    # Try integer
    try:
        return int(value)
    except ValueError:
        pass

    # Try float
    try:
        return float(value)
    except ValueError:
        pass

    # Keep as string
    return value


def read_csv(filename, delimiter=",", convert_types=True):
    """Read CSV file into list of dictionaries."""
    data = []

    with open(filename, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file, delimiter=delimiter)

        for row in reader:
            if convert_types:
                row = {k: detect_type(v) for k, v in row.items()}
            data.append(row)

    return data


def write_json(data, filename, pretty=True):
    """Write data to JSON file."""
    with open(filename, "w", encoding="utf-8") as file:
        if pretty:
            json.dump(data, file, indent=2, ensure_ascii=False)
        else:
            json.dump(data, file, ensure_ascii=False)


def read_json(filename):
    """Read JSON file."""
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


def write_csv(data, filename, delimiter=","):
    """Write data to CSV file."""
    if not data:
        print("No data to write")
        return

    fieldnames = list(data[0].keys())

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()

        for row in data:
            # Convert non-string values
            csv_row = {}
            for key, value in row.items():
                if value is None:
                    csv_row[key] = ""
                elif isinstance(value, bool):
                    csv_row[key] = str(value).lower()
                elif isinstance(value, (list, dict)):
                    csv_row[key] = json.dumps(value)
                else:
                    csv_row[key] = value
            writer.writerow(csv_row)


def summarize_data(data):
    """Generate summary statistics for data."""
    if not data:
        return {"count": 0}

    summary = {
        "count": len(data),
        "fields": list(data[0].keys()),
        "field_types": {},
        "sample": data[0] if data else None
    }

    # Detect field types
    for field in summary["fields"]:
        types = set()
        for row in data:
            value = row.get(field)
            if value is not None:
                types.add(type(value).__name__)
        summary["field_types"][field] = list(types)

    return summary


def filter_data(data, conditions):
    """Filter data based on conditions.

    Args:
        data: List of dictionaries
        conditions: Dict of {field: value} or {field: (operator, value)}
    """
    result = data

    for field, condition in conditions.items():
        if isinstance(condition, tuple):
            op, value = condition
            if op == "eq":
                result = [r for r in result if r.get(field) == value]
            elif op == "ne":
                result = [r for r in result if r.get(field) != value]
            elif op == "gt":
                result = [r for r in result if r.get(field, 0) > value]
            elif op == "lt":
                result = [r for r in result if r.get(field, 0) < value]
            elif op == "contains":
                result = [r for r in result if value in str(r.get(field, ""))]
        else:
            result = [r for r in result if r.get(field) == condition]

    return result


def aggregate_data(data, group_by, aggregations):
    """Aggregate data by field.

    Args:
        data: List of dictionaries
        group_by: Field to group by
        aggregations: Dict of {new_field: (agg_func, source_field)}
                     agg_func: 'count', 'sum', 'avg', 'min', 'max'
    """
    groups = {}

    for row in data:
        key = row.get(group_by)
        if key not in groups:
            groups[key] = []
        groups[key].append(row)

    result = []
    for key, rows in groups.items():
        agg_row = {group_by: key}

        for new_field, (func, source_field) in aggregations.items():
            values = [r.get(source_field, 0) for r in rows if r.get(source_field) is not None]

            if func == "count":
                agg_row[new_field] = len(rows)
            elif func == "sum" and values:
                agg_row[new_field] = sum(values)
            elif func == "avg" and values:
                agg_row[new_field] = sum(values) / len(values)
            elif func == "min" and values:
                agg_row[new_field] = min(values)
            elif func == "max" and values:
                agg_row[new_field] = max(values)

        result.append(agg_row)

    return result


def main():
    """Interactive data converter."""
    print("=" * 50)
    print("CSV/JSON Data Converter")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("1. Convert CSV to JSON")
        print("2. Convert JSON to CSV")
        print("3. View file summary")
        print("4. Filter and export")
        print("5. Aggregate data")
        print("6. Exit")

        choice = input("\nEnter choice (1-6): ").strip()

        if choice == "1":
            csv_file = input("CSV file path: ").strip()
            if not os.path.exists(csv_file):
                print("File not found!")
                continue

            json_file = input("Output JSON file: ").strip()
            delimiter = input("Delimiter (default ','): ").strip() or ","

            try:
                data = read_csv(csv_file, delimiter)
                write_json(data, json_file)
                print(f"Converted {len(data)} records to {json_file}")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "2":
            json_file = input("JSON file path: ").strip()
            if not os.path.exists(json_file):
                print("File not found!")
                continue

            csv_file = input("Output CSV file: ").strip()

            try:
                data = read_json(json_file)
                if not isinstance(data, list):
                    data = [data]
                write_csv(data, csv_file)
                print(f"Converted {len(data)} records to {csv_file}")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "3":
            file_path = input("File path (CSV or JSON): ").strip()
            if not os.path.exists(file_path):
                print("File not found!")
                continue

            try:
                if file_path.endswith(".json"):
                    data = read_json(file_path)
                    if not isinstance(data, list):
                        data = [data]
                else:
                    data = read_csv(file_path)

                summary = summarize_data(data)
                print(f"\nSummary for {file_path}:")
                print(f"  Records: {summary['count']}")
                print(f"  Fields: {', '.join(summary['fields'])}")
                print(f"  Field types:")
                for field, types in summary['field_types'].items():
                    print(f"    {field}: {', '.join(types)}")
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "4":
            file_path = input("File path: ").strip()
            if not os.path.exists(file_path):
                print("File not found!")
                continue

            try:
                if file_path.endswith(".json"):
                    data = read_json(file_path)
                else:
                    data = read_csv(file_path)

                print("Enter filter conditions (field=value), empty to finish:")
                conditions = {}
                while True:
                    condition = input("  Filter: ").strip()
                    if not condition:
                        break
                    if "=" in condition:
                        field, value = condition.split("=", 1)
                        conditions[field.strip()] = detect_type(value.strip())

                filtered = filter_data(data, conditions)
                print(f"Filtered: {len(filtered)} records (from {len(data)})")

                output = input("Output file (or empty to skip): ").strip()
                if output:
                    if output.endswith(".json"):
                        write_json(filtered, output)
                    else:
                        write_csv(filtered, output)
                    print(f"Saved to {output}")

            except Exception as e:
                print(f"Error: {e}")

        elif choice == "5":
            file_path = input("File path: ").strip()
            if not os.path.exists(file_path):
                print("File not found!")
                continue

            try:
                if file_path.endswith(".json"):
                    data = read_json(file_path)
                else:
                    data = read_csv(file_path)

                group_by = input("Group by field: ").strip()

                print("Aggregations (func:field, e.g., sum:amount):")
                aggregations = {}
                while True:
                    agg = input("  Aggregation: ").strip()
                    if not agg:
                        break
                    if ":" in agg:
                        func, field = agg.split(":", 1)
                        new_name = f"{func}_{field}"
                        aggregations[new_name] = (func.strip(), field.strip())

                if aggregations:
                    result = aggregate_data(data, group_by, aggregations)
                    print(f"\nAggregated: {len(result)} groups")
                    for row in result[:10]:
                        print(f"  {row}")

                    output = input("Output file (or empty to skip): ").strip()
                    if output:
                        if output.endswith(".json"):
                            write_json(result, output)
                        else:
                            write_csv(result, output)

            except Exception as e:
                print(f"Error: {e}")

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
```

---

## Key Takeaways

1. **csv.reader** for lists, **csv.DictReader** for dictionaries
2. **json.load()** reads files, **json.loads()** parses strings
3. **json.dump()** writes files, **json.dumps()** creates strings
4. Use `indent=2` for readable JSON output
5. Always use `newline=""` when writing CSV files
6. Custom encoders handle non-standard types (datetime, Decimal)
7. Validate data structure before processing
8. Process large files in chunks for memory efficiency

---

## Next Week Preview
Week 10 covers pip, virtual environments, and using third-party packages.
