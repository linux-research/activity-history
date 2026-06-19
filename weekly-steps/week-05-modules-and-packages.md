# Week 5: Modules and Packages

## Overview
This week you'll learn how to organize code into modules, work with Python's standard library, and use powerful built-in modules like os, sys, random, and datetime.

---

## Part 1: What are Modules?

A module is simply a Python file containing code (functions, classes, variables) that can be imported and reused.

### Creating a Module

Create a file called `mymath.py`:

```python
# mymath.py
PI = 3.14159

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def circle_area(radius):
    return PI * radius ** 2
```

### Using Your Module

Create another file in the same directory:

```python
# main.py
import mymath

print(mymath.PI)              # 3.14159
print(mymath.add(5, 3))       # 8
print(mymath.circle_area(5))  # 78.53975
```

---

## Part 2: Import Variations

```python
# Import entire module
import mymath
result = mymath.add(5, 3)

# Import with alias
import mymath as mm
result = mm.add(5, 3)

# Import specific items
from mymath import add, PI
result = add(5, 3)
print(PI)

# Import with alias
from mymath import circle_area as area
result = area(5)

# Import everything (generally avoided)
from mymath import *
result = add(5, 3)
```

### Best Practices

```python
# Good - clear where functions come from
import mymath
result = mymath.add(5, 3)

# Good - specific imports
from mymath import add
result = add(5, 3)

# Avoid - unclear origins, potential conflicts
from mymath import *
```

---

## Part 3: The Standard Library

Python comes with many useful built-in modules. Here are the most important ones:

### os Module - Operating System Interface

```python
import os

# Current working directory
cwd = os.getcwd()
print(f"Current directory: {cwd}")

# List directory contents
files = os.listdir(".")
print(files)

# Create directories
os.mkdir("new_folder")           # Single directory
os.makedirs("path/to/folder")    # Nested directories

# Remove directories
os.rmdir("new_folder")           # Empty directory only
os.removedirs("path/to/folder")  # Nested empty directories

# Check existence
print(os.path.exists("file.txt"))
print(os.path.isfile("file.txt"))
print(os.path.isdir("folder"))

# Path manipulation
path = os.path.join("folder", "subfolder", "file.txt")
print(path)  # folder/subfolder/file.txt (or \ on Windows)

dirname = os.path.dirname("/path/to/file.txt")   # /path/to
basename = os.path.basename("/path/to/file.txt") # file.txt
name, ext = os.path.splitext("file.txt")         # ('file', '.txt')

# Environment variables
home = os.environ.get("HOME")
path = os.environ.get("PATH")

# Rename/move files
os.rename("old.txt", "new.txt")
```

### sys Module - System-Specific Parameters

```python
import sys

# Python version
print(sys.version)
print(sys.version_info)

# Command line arguments
# python script.py arg1 arg2
print(sys.argv)  # ['script.py', 'arg1', 'arg2']

# Exit the program
sys.exit(0)      # 0 = success
sys.exit(1)      # Non-zero = error
sys.exit("Error message")

# Module search path
print(sys.path)

# Platform
print(sys.platform)  # 'linux', 'darwin', 'win32'
```

### math Module - Mathematical Functions

```python
import math

# Constants
print(math.pi)   # 3.141592653589793
print(math.e)    # 2.718281828459045

# Basic functions
print(math.sqrt(16))    # 4.0
print(math.pow(2, 3))   # 8.0
print(math.abs(-5))     # 5 (also built-in)

# Rounding
print(math.floor(3.7))  # 3
print(math.ceil(3.2))   # 4
print(math.trunc(3.7))  # 3

# Trigonometry (radians)
print(math.sin(math.pi / 2))  # 1.0
print(math.cos(0))            # 1.0

# Logarithms
print(math.log(10))     # Natural log
print(math.log10(100))  # 2.0
print(math.log2(8))     # 3.0

# Factorial and combinations
print(math.factorial(5))     # 120
print(math.comb(5, 2))       # 10 (5 choose 2)
print(math.gcd(48, 18))      # 6
```

### random Module - Random Number Generation

```python
import random

# Random float [0.0, 1.0)
print(random.random())

# Random float in range
print(random.uniform(1, 10))

# Random integer in range (inclusive)
print(random.randint(1, 100))

# Random choice from sequence
colors = ["red", "green", "blue"]
print(random.choice(colors))

# Multiple random choices
print(random.choices(colors, k=5))  # With replacement
print(random.sample(colors, k=2))   # Without replacement

# Shuffle list in place
deck = list(range(1, 53))
random.shuffle(deck)
print(deck[:5])

# Seed for reproducibility
random.seed(42)
print(random.randint(1, 100))  # Always same result with seed 42
```

### datetime Module - Date and Time

```python
from datetime import datetime, date, time, timedelta

# Current date and time
now = datetime.now()
print(now)  # 2024-01-15 14:30:45.123456

today = date.today()
print(today)  # 2024-01-15

# Creating specific dates/times
d = date(2024, 12, 25)
t = time(14, 30, 0)
dt = datetime(2024, 12, 25, 14, 30, 0)

# Accessing components
print(now.year)
print(now.month)
print(now.day)
print(now.hour)
print(now.minute)
print(now.second)
print(now.weekday())  # 0=Monday, 6=Sunday

# Formatting dates
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print(formatted)  # 2024-01-15 14:30:45

formatted = now.strftime("%B %d, %Y")
print(formatted)  # January 15, 2024

# Common format codes:
# %Y - 4-digit year    %m - month (01-12)    %d - day (01-31)
# %H - hour (00-23)    %M - minute (00-59)   %S - second (00-59)
# %A - weekday name    %B - month name       %I - hour (01-12)
# %p - AM/PM

# Parsing dates from strings
date_str = "2024-12-25"
parsed = datetime.strptime(date_str, "%Y-%m-%d")

# Time differences
delta = timedelta(days=7, hours=3)
future = now + delta
past = now - delta

# Difference between dates
d1 = date(2024, 1, 1)
d2 = date(2024, 12, 31)
diff = d2 - d1
print(diff.days)  # 365
```

---

## Part 4: Creating Your Own Packages

A package is a directory containing modules and a special `__init__.py` file.

```
mypackage/
    __init__.py
    module1.py
    module2.py
    subpackage/
        __init__.py
        module3.py
```

### Example Package Structure

```
calculator/
    __init__.py
    basic.py
    advanced.py
```

`calculator/__init__.py`:
```python
from .basic import add, subtract
from .advanced import power, sqrt
```

`calculator/basic.py`:
```python
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
```

`calculator/advanced.py`:
```python
import math

def power(base, exp):
    return base ** exp

def sqrt(n):
    return math.sqrt(n)
```

Using the package:
```python
from calculator import add, sqrt
print(add(5, 3))
print(sqrt(16))

# Or
import calculator
print(calculator.add(5, 3))
```

---

## Part 5: The __name__ Variable

Every Python file has a special `__name__` variable:
- When run directly: `__name__ == "__main__"`
- When imported: `__name__ == "module_name"`

```python
# mymodule.py

def main():
    print("Running as main program")

def helper():
    print("Helper function")

if __name__ == "__main__":
    # This only runs when file is executed directly
    # Not when imported
    main()
```

This pattern allows a file to be both a module and a standalone script.

---

## Part 6: Practice Exercises

### Exercise 1: File Statistics

```python
import os

def get_directory_stats(path="."):
    """Get statistics about files in a directory."""
    stats = {
        "total_files": 0,
        "total_dirs": 0,
        "total_size": 0,
        "extensions": {}
    }

    for item in os.listdir(path):
        full_path = os.path.join(path, item)

        if os.path.isfile(full_path):
            stats["total_files"] += 1
            stats["total_size"] += os.path.getsize(full_path)

            _, ext = os.path.splitext(item)
            ext = ext.lower() if ext else "no extension"
            stats["extensions"][ext] = stats["extensions"].get(ext, 0) + 1

        elif os.path.isdir(full_path):
            stats["total_dirs"] += 1

    return stats

if __name__ == "__main__":
    stats = get_directory_stats()
    print(f"Files: {stats['total_files']}")
    print(f"Directories: {stats['total_dirs']}")
    print(f"Total size: {stats['total_size']:,} bytes")
    print("Extensions:", stats['extensions'])
```

---

## Week 5 Project: Password Generator

Build a secure random password generator:

```python
import random
import string
import sys

def generate_password(length=16,
                      use_uppercase=True,
                      use_lowercase=True,
                      use_digits=True,
                      use_special=True,
                      exclude_ambiguous=False):
    """
    Generate a random password.

    Args:
        length: Password length (minimum 4)
        use_uppercase: Include uppercase letters
        use_lowercase: Include lowercase letters
        use_digits: Include digits
        use_special: Include special characters
        exclude_ambiguous: Exclude ambiguous characters (0, O, l, 1, I)

    Returns:
        Generated password string
    """
    if length < 4:
        raise ValueError("Password length must be at least 4")

    # Build character pool
    chars = ""
    required = []

    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    special = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    # Remove ambiguous characters if requested
    if exclude_ambiguous:
        uppercase = uppercase.replace("O", "").replace("I", "")
        lowercase = lowercase.replace("l", "")
        digits = digits.replace("0", "").replace("1", "")

    if use_uppercase:
        chars += uppercase
        required.append(random.choice(uppercase))

    if use_lowercase:
        chars += lowercase
        required.append(random.choice(lowercase))

    if use_digits:
        chars += digits
        required.append(random.choice(digits))

    if use_special:
        chars += special
        required.append(random.choice(special))

    if not chars:
        raise ValueError("At least one character type must be selected")

    # Generate remaining characters
    remaining_length = length - len(required)
    password_chars = required + [random.choice(chars) for _ in range(remaining_length)]

    # Shuffle to randomize position of required characters
    random.shuffle(password_chars)

    return "".join(password_chars)


def get_yes_no(prompt):
    """Get yes/no input from user."""
    while True:
        response = input(prompt).strip().lower()
        if response in ['y', 'yes']:
            return True
        if response in ['n', 'no']:
            return False
        print("Please enter 'y' or 'n'")


def get_positive_int(prompt, minimum=1):
    """Get positive integer from user."""
    while True:
        try:
            value = int(input(prompt))
            if value >= minimum:
                return value
            print(f"Please enter a number >= {minimum}")
        except ValueError:
            print("Please enter a valid number")


def main():
    """Main program with interactive menu."""
    print("=" * 50)
    print("SECURE PASSWORD GENERATOR")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("1. Generate with default settings (16 chars, all types)")
        print("2. Custom password")
        print("3. Generate multiple passwords")
        print("4. Exit")

        choice = input("\nEnter choice (1-4): ").strip()

        if choice == "1":
            password = generate_password()
            print(f"\nGenerated password: {password}")
            print(f"Length: {len(password)} characters")

        elif choice == "2":
            print("\nCustom password settings:")
            length = get_positive_int("Length (min 4): ", 4)
            use_upper = get_yes_no("Include uppercase? (y/n): ")
            use_lower = get_yes_no("Include lowercase? (y/n): ")
            use_digits = get_yes_no("Include digits? (y/n): ")
            use_special = get_yes_no("Include special characters? (y/n): ")
            exclude_ambiguous = get_yes_no("Exclude ambiguous (0,O,l,1,I)? (y/n): ")

            try:
                password = generate_password(
                    length=length,
                    use_uppercase=use_upper,
                    use_lowercase=use_lower,
                    use_digits=use_digits,
                    use_special=use_special,
                    exclude_ambiguous=exclude_ambiguous
                )
                print(f"\nGenerated password: {password}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "3":
            count = get_positive_int("How many passwords? ")
            length = get_positive_int("Length (min 4): ", 4)

            print(f"\n{count} passwords of length {length}:")
            for i in range(count):
                password = generate_password(length=length)
                print(f"  {i+1}. {password}")

        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    main()
```

### Command-line Version

```python
import argparse
import random
import string

def generate_password(length, chars):
    return ''.join(random.choice(chars) for _ in range(length))

def main():
    parser = argparse.ArgumentParser(description="Generate random passwords")
    parser.add_argument("-l", "--length", type=int, default=16,
                        help="Password length (default: 16)")
    parser.add_argument("-n", "--number", type=int, default=1,
                        help="Number of passwords (default: 1)")
    parser.add_argument("--no-upper", action="store_true",
                        help="Exclude uppercase letters")
    parser.add_argument("--no-lower", action="store_true",
                        help="Exclude lowercase letters")
    parser.add_argument("--no-digits", action="store_true",
                        help="Exclude digits")
    parser.add_argument("--no-special", action="store_true",
                        help="Exclude special characters")

    args = parser.parse_args()

    chars = ""
    if not args.no_upper:
        chars += string.ascii_uppercase
    if not args.no_lower:
        chars += string.ascii_lowercase
    if not args.no_digits:
        chars += string.digits
    if not args.no_special:
        chars += "!@#$%^&*"

    if not chars:
        print("Error: At least one character type required")
        return

    for _ in range(args.number):
        print(generate_password(args.length, chars))

if __name__ == "__main__":
    main()
```

---

## Key Takeaways

1. **Modules** are Python files that can be imported
2. Use `import module` or `from module import item`
3. **Standard library** has many useful modules (os, sys, math, random, datetime)
4. **Packages** are directories containing modules with `__init__.py`
5. Use `if __name__ == "__main__":` for code that runs only when executed directly
6. **os** module for file/directory operations
7. **datetime** for date and time handling
8. **random** for random number generation

---

## Next Week Preview
Week 6 introduces Object-Oriented Programming (OOP) with classes, objects, and methods.
