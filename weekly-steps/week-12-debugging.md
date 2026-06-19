# Week 12: Debugging

## Overview
This week covers debugging techniques: using Python's built-in debugger (pdb), IDE debugging, reading tracebacks, and systematic debugging strategies.

---

## Part 1: Reading Tracebacks

### Understanding Tracebacks

```python
# buggy_code.py
def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)

def process_data(data):
    values = data["values"]
    return calculate_average(values)

def main():
    data = {"values": []}
    result = process_data(data)
    print(result)

main()
```

```
Traceback (most recent call last):
  File "buggy_code.py", line 13, in <module>
    main()
  File "buggy_code.py", line 11, in main
    result = process_data(data)
  File "buggy_code.py", line 7, in process_data
    return calculate_average(values)
  File "buggy_code.py", line 4, in calculate_average
    return total / len(numbers)
ZeroDivisionError: division by zero
```

### Reading from Bottom to Top
1. **Last line**: The actual error (`ZeroDivisionError`)
2. **Stack frames**: Show the call chain (most recent at bottom)
3. **File/line info**: Where each call occurred

### Common Error Types

| Error | Meaning |
|-------|---------|
| `SyntaxError` | Invalid Python syntax |
| `NameError` | Variable not defined |
| `TypeError` | Wrong type for operation |
| `ValueError` | Right type, wrong value |
| `IndexError` | List index out of range |
| `KeyError` | Dictionary key not found |
| `AttributeError` | Object doesn't have attribute |
| `ZeroDivisionError` | Division by zero |
| `FileNotFoundError` | File doesn't exist |
| `ImportError` | Module import failed |

---

## Part 2: Basic Debugging Techniques

### Print Debugging

```python
def buggy_function(data):
    print(f"DEBUG: data = {data}")
    print(f"DEBUG: type(data) = {type(data)}")

    result = []
    for item in data:
        print(f"DEBUG: processing item = {item}")
        processed = item * 2
        print(f"DEBUG: processed = {processed}")
        result.append(processed)

    print(f"DEBUG: final result = {result}")
    return result
```

### Better Print Debugging

```python
import sys

def debug(*args, **kwargs):
    """Print debug info with file/line info."""
    import inspect
    frame = inspect.currentframe().f_back
    filename = frame.f_code.co_filename.split("/")[-1]
    lineno = frame.f_lineno
    print(f"[{filename}:{lineno}]", *args, **kwargs, file=sys.stderr)

# Usage
debug("value =", some_value)
debug(f"list length: {len(my_list)}")
```

### Assert Statements

```python
def divide(a, b):
    assert b != 0, "Divisor cannot be zero"
    assert isinstance(a, (int, float)), f"Expected number, got {type(a)}"
    return a / b

def process_list(items):
    assert items, "List cannot be empty"
    assert all(isinstance(x, int) for x in items), "All items must be integers"
    return sum(items)
```

---

## Part 3: Using pdb (Python Debugger)

### Starting pdb

```python
# Method 1: Insert breakpoint in code
def my_function(x):
    import pdb; pdb.set_trace()  # Breakpoint
    result = x * 2
    return result

# Method 2: Python 3.7+ built-in
def my_function(x):
    breakpoint()  # Same as above
    result = x * 2
    return result

# Method 3: Run script with pdb
# python -m pdb script.py
```

### pdb Commands

| Command | Short | Description |
|---------|-------|-------------|
| `help` | `h` | Show help |
| `next` | `n` | Execute next line |
| `step` | `s` | Step into function |
| `continue` | `c` | Continue until next breakpoint |
| `return` | `r` | Continue until function returns |
| `quit` | `q` | Quit debugger |
| `print expr` | `p expr` | Print expression |
| `pp expr` | | Pretty print expression |
| `list` | `l` | Show current code |
| `longlist` | `ll` | Show entire function |
| `where` | `w` | Show stack trace |
| `up` | `u` | Move up in stack |
| `down` | `d` | Move down in stack |
| `break` | `b` | Set breakpoint |
| `clear` | `cl` | Clear breakpoint |
| `args` | `a` | Show function arguments |

### pdb Example Session

```python
# debug_example.py
def factorial(n):
    breakpoint()
    if n <= 1:
        return 1
    return n * factorial(n - 1)

result = factorial(5)
print(result)
```

```
$ python debug_example.py
> debug_example.py(3)factorial()
-> if n <= 1:
(Pdb) p n
5
(Pdb) n
> debug_example.py(5)factorial()
-> return n * factorial(n - 1)
(Pdb) s
> debug_example.py(2)factorial()
-> breakpoint()
(Pdb) p n
4
(Pdb) c  # Continue to next breakpoint
> debug_example.py(3)factorial()
-> if n <= 1:
(Pdb) c
...
120
```

### Conditional Breakpoints

```python
def process_items(items):
    for i, item in enumerate(items):
        # Only break when we reach item 50
        if i == 50:
            breakpoint()
        process(item)

# Or using pdb command
# (Pdb) b 10, i == 50    # Break at line 10 when i equals 50
```

---

## Part 4: Advanced pdb Features

### Post-mortem Debugging

```python
# Debug after an exception
import pdb

try:
    buggy_function()
except Exception:
    pdb.post_mortem()

# Or from command line:
# python -m pdb -c continue script.py
# (Runs until exception, then drops into debugger)
```

### Debugging in Interactive Mode

```python
>>> import pdb
>>> import my_module
>>> pdb.run("my_module.my_function()")
```

### pdb++ (Enhanced pdb)

```bash
pip install pdbpp
```

```python
# Automatically uses pdb++ when you call breakpoint()
# Features: syntax highlighting, tab completion, sticky mode
```

---

## Part 5: IDE Debugging (VS Code)

### Setting Up VS Code

1. Install Python extension
2. Open your Python file
3. Click left of line numbers to set breakpoints (red dots)
4. Press F5 or Run → Start Debugging

### VS Code Debug Features

- **Breakpoints**: Click line gutter
- **Conditional breakpoints**: Right-click breakpoint
- **Watch expressions**: Add variables to watch
- **Call stack**: See function call hierarchy
- **Variables panel**: Inspect all variables
- **Debug console**: Run expressions during debugging

### launch.json Configuration

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        },
        {
            "name": "Python: Debug Tests",
            "type": "python",
            "request": "launch",
            "module": "pytest",
            "args": ["-v", "${file}"]
        }
    ]
}
```

---

## Part 6: Debugging Strategies

### The Scientific Method

1. **Observe**: What is the bug? What did you expect?
2. **Hypothesize**: What might cause this?
3. **Predict**: If hypothesis is true, what should I see?
4. **Test**: Add debugging code or breakpoints
5. **Analyze**: Was the hypothesis correct?
6. **Repeat**: Try new hypothesis if needed

### Binary Search Debugging

```python
def complex_function(data):
    step1_result = step1(data)     # Is bug before here?

    # Add checkpoint
    print(f"After step1: {step1_result}")
    # If correct, bug is later

    step2_result = step2(step1_result)

    # Add checkpoint
    print(f"After step2: {step2_result}")
    # If wrong, bug is in step2

    return step3(step2_result)
```

### Rubber Duck Debugging

Explain your code line by line, as if to someone else (or a rubber duck). Often, the act of explaining reveals the bug.

### Minimal Reproducible Example

```python
# Instead of debugging entire application:

# Isolate the bug
def test_bug():
    # Minimal setup
    data = {"key": [1, 2, 3]}

    # Minimal code that triggers bug
    result = problematic_function(data)

    # Expected vs actual
    print(f"Expected: X, Got: {result}")

test_bug()
```

---

## Part 7: Common Bug Patterns

### Off-by-One Errors

```python
# Bug: Excludes last element
for i in range(len(items) - 1):  # Should be range(len(items))
    process(items[i])

# Bug: Index out of range
for i in range(len(items) + 1):  # Should be range(len(items))
    process(items[i])

# Bug: Wrong slice
items[1:3]  # Gets items at index 1 and 2, not 1, 2, and 3
```

### Mutable Default Arguments

```python
# BUG!
def add_item(item, items=[]):
    items.append(item)
    return items

print(add_item("a"))  # ['a']
print(add_item("b"))  # ['a', 'b'] - Shared list!

# Fix
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### Variable Scope Issues

```python
# Bug: UnboundLocalError
count = 0

def increment():
    count += 1  # Error! Python sees assignment, thinks it's local
    return count

# Fix
def increment():
    global count
    count += 1
    return count

# Better fix: Avoid globals
def increment(count):
    return count + 1
```

### Type Confusion

```python
# Bug: String instead of number
age = input("Enter age: ")  # Returns string!
next_year = age + 1  # TypeError!

# Fix
age = int(input("Enter age: "))
next_year = age + 1

# Bug: None returned unexpectedly
def find_item(items, target):
    for item in items:
        if item == target:
            return item
    # Implicitly returns None!

result = find_item([1, 2, 3], 4)
result.do_something()  # AttributeError: 'NoneType'

# Fix: Check for None
result = find_item([1, 2, 3], 4)
if result is not None:
    result.do_something()
```

### Reference vs Copy

```python
# Bug: Modifying shared reference
original = [1, 2, 3]
copy = original
copy.append(4)
print(original)  # [1, 2, 3, 4] - Original modified!

# Fix: Make actual copy
copy = original.copy()
# or
copy = original[:]
# or
import copy
deep_copy = copy.deepcopy(original)
```

---

## Part 8: Logging Instead of Print

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def process_data(data):
    logger.debug(f"Input data: {data}")

    try:
        result = complex_operation(data)
        logger.info(f"Operation successful: {result}")
        return result
    except ValueError as e:
        logger.error(f"Invalid value: {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error")  # Includes traceback
        raise

# Log levels: DEBUG < INFO < WARNING < ERROR < CRITICAL
```

---

## Week 12 Project: Debug a Buggy Application

Here's a buggy contact manager. Find and fix all the bugs:

```python
# buggy_contacts.py - Contains multiple bugs!

def load_contacts(filename):
    """Load contacts from file."""
    contacts = {}
    with open(filename, "r") as f:
        for line in f:
            name, phone, email = line.split(",")
            contacts[name] = {"phone": phone, "email": email}
    return contacts

def save_contacts(contacts, filename):
    """Save contacts to file."""
    with open(filename, "w") as f:
        for name, info in contacts:
            f.write(f"{name},{info['phone']},{info['email']}")

def add_contact(contacts, name, phone, email):
    """Add a new contact."""
    contacts[name] = {"phone": phone, "email": email}

def find_contact(contacts, search_term):
    """Find contacts matching search term."""
    results = []
    for name in contacts:
        if search_term in name:
            results.append(name, contacts[name])
    return results

def delete_contact(contacts, name):
    """Delete a contact."""
    del contacts[name]

def display_contacts(contacts):
    """Display all contacts."""
    for name, info in contacts.items():
        print(f"Name: {name}")
        print(f"  Phone: {info["phone"]}")
        print(f"  Email: {info["email"]}")

def main():
    contacts = {}

    # Try to load existing contacts
    contacts = load_contacts("contacts.txt")

    while True:
        print("\n1. Add contact")
        print("2. Find contact")
        print("3. Delete contact")
        print("4. Display all")
        print("5. Save and exit")

        choice = input("Choice: ")

        if choice == "1":
            name = input("Name: ")
            phone = input("Phone: ")
            email = input("Email: ")
            add_contact(contacts, name, phone, email)

        elif choice == "2":
            term = input("Search: ")
            results = find_contact(contacts, term)
            for r in results:
                print(r)

        elif choice == "3":
            name = input("Name to delete: ")
            delete_contact(contacts, name)

        elif choice == "4":
            display_contacts(contacts)

        elif choice == "5":
            save_contacts(contacts, "contacts.txt")
            print("Saved!")
            break

if __name__ == "__main__":
    main()
```

### Fixed Version

```python
# fixed_contacts.py

import os

def load_contacts(filename):
    """Load contacts from file."""
    contacts = {}

    # Bug fix: Handle missing file
    if not os.path.exists(filename):
        return contacts

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()  # Bug fix: Remove whitespace/newlines
            if not line:
                continue

            parts = line.split(",")
            if len(parts) != 3:  # Bug fix: Validate format
                continue

            name, phone, email = parts
            contacts[name] = {"phone": phone, "email": email}

    return contacts

def save_contacts(contacts, filename):
    """Save contacts to file."""
    with open(filename, "w") as f:
        # Bug fix: Use .items() for dict iteration
        for name, info in contacts.items():
            # Bug fix: Add newline at end
            f.write(f"{name},{info['phone']},{info['email']}\n")

def add_contact(contacts, name, phone, email):
    """Add a new contact."""
    # Bug fix: Validate input
    if not name or not phone or not email:
        raise ValueError("All fields required")
    contacts[name] = {"phone": phone, "email": email}

def find_contact(contacts, search_term):
    """Find contacts matching search term."""
    results = []
    search_lower = search_term.lower()
    for name, info in contacts.items():  # Bug fix: Use .items()
        if search_lower in name.lower():
            # Bug fix: Use tuple, not multiple args
            results.append((name, info))
    return results

def delete_contact(contacts, name):
    """Delete a contact."""
    # Bug fix: Check if exists first
    if name not in contacts:
        raise KeyError(f"Contact '{name}' not found")
    del contacts[name]

def display_contacts(contacts):
    """Display all contacts."""
    if not contacts:
        print("No contacts found.")
        return

    for name, info in contacts.items():
        print(f"Name: {name}")
        # Bug fix: Use single quotes inside f-string
        print(f"  Phone: {info['phone']}")
        print(f"  Email: {info['email']}")

def main():
    contacts = {}
    filename = "contacts.txt"

    # Try to load existing contacts
    try:
        contacts = load_contacts(filename)
        print(f"Loaded {len(contacts)} contacts.")
    except Exception as e:
        print(f"Could not load contacts: {e}")

    while True:
        print("\n1. Add contact")
        print("2. Find contact")
        print("3. Delete contact")
        print("4. Display all")
        print("5. Save and exit")

        choice = input("Choice: ").strip()

        if choice == "1":
            try:
                name = input("Name: ").strip()
                phone = input("Phone: ").strip()
                email = input("Email: ").strip()
                add_contact(contacts, name, phone, email)
                print(f"Added {name}!")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            term = input("Search: ").strip()
            results = find_contact(contacts, term)
            if results:
                for name, info in results:
                    print(f"  {name}: {info['phone']}, {info['email']}")
            else:
                print("No matches found.")

        elif choice == "3":
            name = input("Name to delete: ").strip()
            try:
                delete_contact(contacts, name)
                print(f"Deleted {name}!")
            except KeyError as e:
                print(f"Error: {e}")

        elif choice == "4":
            display_contacts(contacts)

        elif choice == "5":
            try:
                save_contacts(contacts, filename)
                print(f"Saved {len(contacts)} contacts!")
            except Exception as e:
                print(f"Could not save: {e}")
            break

        else:
            print("Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()
```

### Bugs Found and Fixed

1. **load_contacts**: File might not exist (FileNotFoundError)
2. **load_contacts**: Didn't strip whitespace/newlines from lines
3. **save_contacts**: Used `contacts` directly instead of `.items()`
4. **save_contacts**: Missing newline at end of each line
5. **find_contact**: Used `.append(name, info)` instead of `.append((name, info))`
6. **delete_contact**: No check if contact exists (KeyError)
7. **display_contacts**: Used double quotes inside f-string incorrectly
8. **main**: No error handling for any operations

---

## Key Takeaways

1. **Read tracebacks** from bottom to top
2. **pdb** is Python's built-in debugger
3. **breakpoint()** is the modern way to start debugging
4. **IDE debuggers** provide visual debugging
5. **Use logging** instead of print for production
6. **Binary search** to locate bugs faster
7. Know **common bug patterns** (off-by-one, mutable defaults, etc.)
8. **Minimal reproducible examples** isolate bugs

---

## Next Week Preview
Week 13 begins the Web Track with Flask basics: routes, templates, and forms.
