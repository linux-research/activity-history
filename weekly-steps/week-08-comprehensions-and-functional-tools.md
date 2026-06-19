# Week 8: Comprehensions and Functional Tools

## Overview
This week covers Python's powerful comprehension syntax and functional programming tools: list/dict/set comprehensions, map(), filter(), lambda, and reduce().

---

## Part 1: List Comprehensions

List comprehensions create lists concisely from existing iterables.

### Basic Syntax

```python
# Traditional way
squares = []
for x in range(10):
    squares.append(x ** 2)

# List comprehension
squares = [x ** 2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

### With Conditions

```python
# Even numbers only
evens = [x for x in range(20) if x % 2 == 0]
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# Multiple conditions
filtered = [x for x in range(50) if x % 2 == 0 if x % 3 == 0]
# [0, 6, 12, 18, 24, 30, 36, 42, 48]

# if-else in expression (ternary)
labels = ["even" if x % 2 == 0 else "odd" for x in range(5)]
# ['even', 'odd', 'even', 'odd', 'even']
```

### Working with Strings

```python
words = ["hello", "world", "python"]

# Uppercase
upper = [word.upper() for word in words]
# ['HELLO', 'WORLD', 'PYTHON']

# Lengths
lengths = [len(word) for word in words]
# [5, 5, 6]

# Filter by length
long_words = [word for word in words if len(word) > 5]
# ['python']

# First letters
initials = [word[0] for word in words]
# ['h', 'w', 'p']
```

### Nested Loops

```python
# Flatten a 2D list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Create pairs
pairs = [(x, y) for x in range(3) for y in range(3)]
# [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]

# Multiplication table
table = [[i * j for j in range(1, 6)] for i in range(1, 6)]
```

---

## Part 2: Dictionary Comprehensions

```python
# Basic dict comprehension
squares = {x: x**2 for x in range(6)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# From two lists
names = ["alice", "bob", "charlie"]
ages = [25, 30, 35]
people = {name: age for name, age in zip(names, ages)}
# {'alice': 25, 'bob': 30, 'charlie': 35}

# With condition
even_squares = {x: x**2 for x in range(10) if x % 2 == 0}
# {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}

# Swap keys and values
original = {"a": 1, "b": 2, "c": 3}
swapped = {v: k for k, v in original.items()}
# {1: 'a', 2: 'b', 3: 'c'}

# Transform keys or values
prices = {"apple": 1.5, "banana": 0.75, "orange": 2.0}
discounted = {k: v * 0.9 for k, v in prices.items()}
upper_prices = {k.upper(): v for k, v in prices.items()}
```

---

## Part 3: Set Comprehensions

```python
# Basic set comprehension (no duplicates)
unique_squares = {x**2 for x in range(-5, 6)}
# {0, 1, 4, 9, 16, 25}

# From string (unique characters)
text = "hello world"
unique_chars = {char for char in text if char.isalpha()}
# {'h', 'e', 'l', 'o', 'w', 'r', 'd'}

# Word lengths
words = ["apple", "banana", "cherry", "date", "elderberry"]
lengths = {len(word) for word in words}
# {4, 5, 6, 10}
```

---

## Part 4: Generator Expressions

Like list comprehensions but create generators (memory efficient).

```python
# Generator expression (note: parentheses, not brackets)
squares_gen = (x**2 for x in range(1000000))

# Memory efficient - values computed on demand
print(next(squares_gen))  # 0
print(next(squares_gen))  # 1

# Convert to list when needed
first_10 = list(x**2 for x in range(10))

# Often used directly in functions
total = sum(x**2 for x in range(100))
maximum = max(len(word) for word in words)
any_long = any(len(word) > 10 for word in words)
```

---

## Part 5: Lambda Functions

Anonymous (unnamed) functions for simple operations.

```python
# Traditional function
def add(x, y):
    return x + y

# Lambda equivalent
add = lambda x, y: x + y

print(add(5, 3))  # 8

# Common uses
square = lambda x: x ** 2
is_even = lambda x: x % 2 == 0
full_name = lambda first, last: f"{first} {last}"
```

### Lambda with Sorting

```python
# Sort by custom key
students = [
    {"name": "Alice", "grade": 85},
    {"name": "Bob", "grade": 92},
    {"name": "Charlie", "grade": 78}
]

# Sort by grade
by_grade = sorted(students, key=lambda s: s["grade"])

# Sort by name
by_name = sorted(students, key=lambda s: s["name"])

# Sort by grade descending
by_grade_desc = sorted(students, key=lambda s: s["grade"], reverse=True)

# Sort tuples by second element
pairs = [(1, 'b'), (2, 'a'), (3, 'c')]
sorted_pairs = sorted(pairs, key=lambda x: x[1])
# [(2, 'a'), (1, 'b'), (3, 'c')]
```

---

## Part 6: map() Function

Apply a function to every item in an iterable.

```python
# Basic map
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
# [1, 4, 9, 16, 25]

# With named function
def double(x):
    return x * 2

doubled = list(map(double, numbers))
# [2, 4, 6, 8, 10]

# Multiple iterables
a = [1, 2, 3]
b = [4, 5, 6]
sums = list(map(lambda x, y: x + y, a, b))
# [5, 7, 9]

# Convert types
str_numbers = ["1", "2", "3", "4"]
int_numbers = list(map(int, str_numbers))
# [1, 2, 3, 4]
```

### map() vs Comprehension

```python
# These are equivalent:
result1 = list(map(lambda x: x**2, range(10)))
result2 = [x**2 for x in range(10)]

# Comprehension is usually preferred for readability
# map() is useful when you have an existing function
```

---

## Part 7: filter() Function

Filter items based on a condition.

```python
# Basic filter
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = list(filter(lambda x: x % 2 == 0, numbers))
# [2, 4, 6, 8, 10]

# With named function
def is_positive(x):
    return x > 0

mixed = [-2, -1, 0, 1, 2, 3]
positives = list(filter(is_positive, mixed))
# [1, 2, 3]

# Filter None values
data = [1, None, 2, None, 3, None]
clean = list(filter(None, data))  # None as function filters falsy values
# [1, 2, 3]

# Filter strings
words = ["", "hello", "", "world", "  ", "python"]
non_empty = list(filter(lambda s: s.strip(), words))
# ['hello', 'world', 'python']
```

### filter() vs Comprehension

```python
# These are equivalent:
result1 = list(filter(lambda x: x % 2 == 0, range(10)))
result2 = [x for x in range(10) if x % 2 == 0]

# Comprehension is usually more readable
```

---

## Part 8: reduce() Function

Reduce an iterable to a single value.

```python
from functools import reduce

# Sum of numbers
numbers = [1, 2, 3, 4, 5]
total = reduce(lambda acc, x: acc + x, numbers)
# 15

# Product of numbers
product = reduce(lambda acc, x: acc * x, numbers)
# 120

# Find maximum
maximum = reduce(lambda a, b: a if a > b else b, numbers)
# 5

# Concatenate strings
words = ["Hello", " ", "World", "!"]
sentence = reduce(lambda acc, w: acc + w, words)
# "Hello World!"

# With initial value
numbers = [1, 2, 3]
total = reduce(lambda acc, x: acc + x, numbers, 100)
# 106 (100 + 1 + 2 + 3)
```

### When to Use reduce()

```python
# Usually, built-in functions are better:
numbers = [1, 2, 3, 4, 5]

# Don't do this:
total = reduce(lambda a, b: a + b, numbers)

# Do this instead:
total = sum(numbers)

# reduce() is useful for custom accumulation:
# Building nested structure
data = [("a", 1), ("b", 2), ("c", 3)]
result = reduce(lambda d, kv: {**d, kv[0]: kv[1]}, data, {})
# {'a': 1, 'b': 2, 'c': 3}
```

---

## Part 9: Combining Functions

```python
# Chain operations
numbers = range(1, 21)

# Get sum of squares of even numbers
result = sum(
    x**2
    for x in numbers
    if x % 2 == 0
)
# 220

# Using map/filter
result = sum(
    map(lambda x: x**2,
        filter(lambda x: x % 2 == 0, numbers))
)

# Process data pipeline
data = ["  Alice  ", "BOB", "  charlie", "DIANA  "]

# Clean and normalize names
cleaned = [name.strip().title() for name in data]
# ['Alice', 'Bob', 'Charlie', 'Diana']

# Or with map
cleaned = list(map(lambda s: s.strip().title(), data))
```

---

## Part 10: Practice Exercises

### Exercise 1: Data Processing

```python
students = [
    {"name": "Alice", "scores": [85, 90, 88]},
    {"name": "Bob", "scores": [72, 68, 75]},
    {"name": "Charlie", "scores": [95, 92, 98]},
    {"name": "Diana", "scores": [60, 65, 70]}
]

# Calculate average for each student
averages = {
    s["name"]: sum(s["scores"]) / len(s["scores"])
    for s in students
}
# {'Alice': 87.67, 'Bob': 71.67, 'Charlie': 95.0, 'Diana': 65.0}

# Students with average > 80
high_achievers = [
    s["name"] for s in students
    if sum(s["scores"]) / len(s["scores"]) > 80
]
# ['Alice', 'Charlie']

# Flatten all scores
all_scores = [score for s in students for score in s["scores"]]
# [85, 90, 88, 72, 68, 75, 95, 92, 98, 60, 65, 70]
```

---

## Week 8 Project: Data Cleaner

Build a tool to clean messy string data:

```python
import re

def clean_strings(data, operations=None):
    """
    Clean a list of messy strings.

    Args:
        data: List of strings to clean
        operations: List of cleaning operations to apply
                   Options: 'strip', 'lower', 'upper', 'title',
                           'remove_numbers', 'remove_special',
                           'collapse_spaces', 'remove_empty'

    Returns:
        Cleaned list of strings
    """
    if operations is None:
        operations = ['strip', 'collapse_spaces', 'remove_empty']

    result = data.copy()

    for op in operations:
        if op == 'strip':
            result = [s.strip() for s in result]

        elif op == 'lower':
            result = [s.lower() for s in result]

        elif op == 'upper':
            result = [s.upper() for s in result]

        elif op == 'title':
            result = [s.title() for s in result]

        elif op == 'remove_numbers':
            result = [re.sub(r'\d', '', s) for s in result]

        elif op == 'remove_special':
            result = [re.sub(r'[^a-zA-Z0-9\s]', '', s) for s in result]

        elif op == 'collapse_spaces':
            result = [re.sub(r'\s+', ' ', s) for s in result]

        elif op == 'remove_empty':
            result = [s for s in result if s.strip()]

    return result


def analyze_strings(data):
    """
    Analyze a list of strings.

    Returns dictionary with statistics.
    """
    non_empty = [s for s in data if s.strip()]

    return {
        'total_count': len(data),
        'non_empty_count': len(non_empty),
        'empty_count': len(data) - len(non_empty),
        'avg_length': sum(len(s) for s in non_empty) / len(non_empty) if non_empty else 0,
        'max_length': max((len(s) for s in non_empty), default=0),
        'min_length': min((len(s) for s in non_empty), default=0),
        'unique_count': len(set(s.lower().strip() for s in non_empty)),
        'has_numbers': any(any(c.isdigit() for c in s) for s in data),
        'all_alpha': all(s.isalpha() for s in non_empty if s),
    }


def transform_data(data, transformations):
    """
    Apply custom transformations using map/filter/reduce patterns.

    Args:
        data: List of strings
        transformations: List of (operation, function) tuples
                        operation: 'map', 'filter', 'sort'

    Returns:
        Transformed data
    """
    result = data

    for operation, func in transformations:
        if operation == 'map':
            result = list(map(func, result))
        elif operation == 'filter':
            result = list(filter(func, result))
        elif operation == 'sort':
            result = sorted(result, key=func)

    return result


def extract_patterns(data, pattern):
    """
    Extract matching patterns from strings.

    Args:
        data: List of strings
        pattern: Regex pattern to extract

    Returns:
        List of all matches found
    """
    return [
        match
        for s in data
        for match in re.findall(pattern, s)
    ]


def main():
    """Demonstrate the data cleaner."""

    # Messy data
    messy_data = [
        "  John Smith  ",
        "JANE   DOE",
        "bob123 wilson",
        "",
        "  alice    jones  ",
        "Charlie@Brown!",
        "   ",
        "diana prince 42",
        "EVE williams"
    ]

    print("Original data:")
    for i, s in enumerate(messy_data):
        print(f"  {i}: '{s}'")

    # Clean the data
    cleaned = clean_strings(
        messy_data,
        ['strip', 'remove_numbers', 'remove_special',
         'collapse_spaces', 'title', 'remove_empty']
    )

    print("\nCleaned data:")
    for i, s in enumerate(cleaned):
        print(f"  {i}: '{s}'")

    # Analyze
    print("\nAnalysis:")
    stats = analyze_strings(messy_data)
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Custom transformations
    print("\nCustom transformations:")

    transformed = transform_data(
        messy_data,
        [
            ('filter', lambda s: s.strip()),  # Remove empty
            ('map', lambda s: s.strip().lower()),  # Normalize
            ('filter', lambda s: len(s) > 5),  # Min length
            ('sort', lambda s: s),  # Alphabetical
        ]
    )

    for s in transformed:
        print(f"  '{s}'")

    # Extract emails
    data_with_emails = [
        "Contact: john@example.com",
        "Email me at jane.doe@company.org",
        "No email here",
        "Two emails: a@b.com and c@d.net"
    ]

    email_pattern = r'[\w.+-]+@[\w-]+\.[\w.-]+'
    emails = extract_patterns(data_with_emails, email_pattern)

    print("\nExtracted emails:")
    for email in emails:
        print(f"  {email}")


if __name__ == "__main__":
    main()
```

---

## Key Takeaways

1. **List comprehensions**: `[expr for item in iterable if condition]`
2. **Dict comprehensions**: `{key: value for item in iterable}`
3. **Set comprehensions**: `{expr for item in iterable}`
4. **Generator expressions**: Memory-efficient, lazy evaluation
5. **Lambda**: Anonymous functions for simple operations
6. **map()**: Apply function to all items
7. **filter()**: Keep items matching condition
8. **reduce()**: Accumulate values into one result
9. Comprehensions are usually more readable than map/filter

---

## Next Week Preview
Week 9 covers working with CSV and JSON files for data interchange.
