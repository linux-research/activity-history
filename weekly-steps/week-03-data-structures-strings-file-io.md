# Week 3: Data Structures, Strings, and File I/O

## Overview
This week covers Python's built-in data structures (lists, tuples, dictionaries, sets), advanced string manipulation, and reading/writing files.

---

## Part 1: Lists

### Creating Lists
```python
# Empty list
empty = []

# List with items
numbers = [1, 2, 3, 4, 5]
fruits = ["apple", "banana", "cherry"]
mixed = [1, "hello", 3.14, True]

# List from range
nums = list(range(1, 6))  # [1, 2, 3, 4, 5]
```

### Accessing Elements
```python
fruits = ["apple", "banana", "cherry", "date"]

# Indexing (0-based)
print(fruits[0])   # apple
print(fruits[2])   # cherry
print(fruits[-1])  # date (last item)
print(fruits[-2])  # cherry (second to last)

# Slicing [start:stop:step]
print(fruits[1:3])   # ['banana', 'cherry']
print(fruits[:2])    # ['apple', 'banana']
print(fruits[2:])    # ['cherry', 'date']
print(fruits[::2])   # ['apple', 'cherry'] (every 2nd)
print(fruits[::-1])  # Reversed list
```

### Modifying Lists
```python
fruits = ["apple", "banana", "cherry"]

# Change an item
fruits[1] = "blueberry"

# Add items
fruits.append("date")           # Add to end
fruits.insert(1, "apricot")     # Insert at index
fruits.extend(["fig", "grape"]) # Add multiple items

# Remove items
fruits.remove("apple")  # Remove by value
popped = fruits.pop()   # Remove and return last
popped = fruits.pop(0)  # Remove and return at index
del fruits[0]           # Delete by index
fruits.clear()          # Remove all items
```

### List Methods
```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

# Sorting
numbers.sort()              # Sort in place
numbers.sort(reverse=True)  # Sort descending
sorted_nums = sorted(numbers)  # Return new sorted list

# Other methods
numbers.reverse()           # Reverse in place
count = numbers.count(1)    # Count occurrences
index = numbers.index(5)    # Find index of value
length = len(numbers)       # Number of items

# Copy a list
copy = numbers.copy()
copy = numbers[:]
copy = list(numbers)
```

### List Comprehensions (Preview)
```python
# Create a list of squares
squares = [x**2 for x in range(1, 6)]  # [1, 4, 9, 16, 25]

# Filter with condition
evens = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]
```

---

## Part 2: Tuples

Tuples are immutable (cannot be changed after creation).

```python
# Creating tuples
point = (3, 4)
colors = ("red", "green", "blue")
single = (42,)  # Note the comma for single item

# Accessing (same as lists)
print(colors[0])    # red
print(colors[-1])   # blue
print(colors[1:])   # ('green', 'blue')

# Tuple unpacking
x, y = point
print(x, y)  # 3 4

# Multiple assignment
a, b, c = 1, 2, 3

# Swap variables
a, b = b, a

# Tuples are immutable
# colors[0] = "yellow"  # Error!

# But you can create new tuples
new_colors = colors + ("yellow",)
```

### When to Use Tuples
- Data that shouldn't change (coordinates, RGB values)
- Dictionary keys (lists can't be keys)
- Function return values
- Slightly more memory efficient than lists

---

## Part 3: Dictionaries

Key-value pairs for fast lookups.

```python
# Creating dictionaries
empty = {}
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

# Accessing values
print(person["name"])      # Alice
print(person.get("age"))   # 30
print(person.get("job"))   # None (no error)
print(person.get("job", "Unknown"))  # "Unknown" (default)

# Modifying
person["age"] = 31                # Update value
person["email"] = "a@test.com"    # Add new key
del person["city"]                # Delete key
email = person.pop("email")       # Remove and return

# Check if key exists
if "name" in person:
    print("Name exists!")
```

### Dictionary Methods
```python
person = {"name": "Alice", "age": 30}

# Get all keys, values, items
keys = person.keys()      # dict_keys(['name', 'age'])
values = person.values()  # dict_values(['Alice', 30])
items = person.items()    # dict_items([('name', 'Alice'), ('age', 30)])

# Iterate
for key in person:
    print(f"{key}: {person[key]}")

for key, value in person.items():
    print(f"{key}: {value}")

# Update with another dict
person.update({"city": "Boston", "age": 31})

# Copy
copy = person.copy()
```

### Nested Dictionaries
```python
users = {
    "alice": {
        "email": "alice@test.com",
        "age": 30
    },
    "bob": {
        "email": "bob@test.com",
        "age": 25
    }
}

print(users["alice"]["email"])  # alice@test.com
```

---

## Part 4: Sets

Unordered collections of unique items.

```python
# Creating sets
empty = set()
numbers = {1, 2, 3, 4, 5}
letters = set("hello")  # {'h', 'e', 'l', 'o'}

# Adding and removing
numbers.add(6)
numbers.remove(1)     # Error if not found
numbers.discard(10)   # No error if not found
popped = numbers.pop()  # Remove arbitrary item

# Set operations
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

union = a | b           # {1, 2, 3, 4, 5, 6}
intersection = a & b    # {3, 4}
difference = a - b      # {1, 2}
symmetric = a ^ b       # {1, 2, 5, 6}

# Check membership (very fast!)
if 3 in a:
    print("Found!")

# Remove duplicates from list
numbers = [1, 2, 2, 3, 3, 3, 4]
unique = list(set(numbers))  # [1, 2, 3, 4]
```

---

## Part 5: String Methods

```python
text = "  Hello, World!  "

# Case conversion
print(text.lower())      # "  hello, world!  "
print(text.upper())      # "  HELLO, WORLD!  "
print(text.title())      # "  Hello, World!  "
print(text.capitalize()) # "  hello, world!  "
print(text.swapcase())   # "  hELLO, wORLD!  "

# Whitespace
print(text.strip())      # "Hello, World!"
print(text.lstrip())     # "Hello, World!  "
print(text.rstrip())     # "  Hello, World!"

# Finding and replacing
text = "Hello, World!"
print(text.find("World"))     # 7 (index)
print(text.find("Python"))    # -1 (not found)
print(text.replace("World", "Python"))  # "Hello, Python!"
print(text.count("l"))        # 3

# Checking content
print("hello".isalpha())      # True
print("123".isdigit())        # True
print("hello123".isalnum())   # True
print("  ".isspace())         # True
print("Hello".startswith("He"))  # True
print("Hello".endswith("lo"))    # True

# Splitting and joining
sentence = "apple,banana,cherry"
fruits = sentence.split(",")      # ['apple', 'banana', 'cherry']
joined = "-".join(fruits)         # "apple-banana-cherry"

words = "Hello World".split()     # ['Hello', 'World']
lines = "line1\nline2".splitlines()  # ['line1', 'line2']
```

### f-strings (Formatted String Literals)
```python
name = "Alice"
age = 30
price = 19.99

# Basic formatting
print(f"Name: {name}, Age: {age}")

# Expressions inside braces
print(f"Next year: {age + 1}")

# Formatting numbers
print(f"Price: ${price:.2f}")        # $19.99
print(f"Percentage: {0.856:.1%}")    # 85.6%
print(f"Padded: {42:05d}")           # 00042

# Alignment
print(f"{'left':<10}")   # "left      "
print(f"{'right':>10}")  # "     right"
print(f"{'center':^10}") # "  center  "
```

---

## Part 6: File I/O

### Reading Files
```python
# Method 1: Basic (must close manually)
file = open("data.txt", "r")
content = file.read()
file.close()

# Method 2: With statement (auto-closes) - PREFERRED
with open("data.txt", "r") as file:
    content = file.read()

# Read all lines as list
with open("data.txt", "r") as file:
    lines = file.readlines()

# Read line by line (memory efficient)
with open("data.txt", "r") as file:
    for line in file:
        print(line.strip())
```

### Writing Files
```python
# Write (overwrites existing content)
with open("output.txt", "w") as file:
    file.write("Hello, World!\n")
    file.write("Second line\n")

# Append to existing file
with open("output.txt", "a") as file:
    file.write("Appended line\n")

# Write multiple lines
lines = ["Line 1\n", "Line 2\n", "Line 3\n"]
with open("output.txt", "w") as file:
    file.writelines(lines)
```

### File Modes
| Mode | Description |
|------|-------------|
| `r`  | Read (default) |
| `w`  | Write (overwrites) |
| `a`  | Append |
| `r+` | Read and write |
| `rb` | Read binary |
| `wb` | Write binary |

### Working with Paths
```python
import os

# Current directory
cwd = os.getcwd()

# Check if file exists
if os.path.exists("data.txt"):
    print("File exists!")

# Join paths (cross-platform)
path = os.path.join("folder", "subfolder", "file.txt")

# Get filename and directory
filename = os.path.basename("/path/to/file.txt")  # file.txt
directory = os.path.dirname("/path/to/file.txt")  # /path/to
```

---

## Week 3 Project: Contact Book

Build a contact book that saves to a file:

```python
import os

CONTACTS_FILE = "contacts.txt"

def load_contacts():
    """Load contacts from file into a dictionary."""
    contacts = {}
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split("|")
                    if len(parts) == 3:
                        name, phone, email = parts
                        contacts[name] = {"phone": phone, "email": email}
    return contacts

def save_contacts(contacts):
    """Save contacts dictionary to file."""
    with open(CONTACTS_FILE, "w") as file:
        for name, info in contacts.items():
            file.write(f"{name}|{info['phone']}|{info['email']}\n")

def add_contact(contacts):
    """Add a new contact."""
    name = input("Enter name: ").strip()
    if name in contacts:
        print("Contact already exists!")
        return
    phone = input("Enter phone: ").strip()
    email = input("Enter email: ").strip()
    contacts[name] = {"phone": phone, "email": email}
    save_contacts(contacts)
    print(f"Contact '{name}' added!")

def view_contacts(contacts):
    """Display all contacts."""
    if not contacts:
        print("No contacts found.")
        return
    print("\n" + "=" * 50)
    print(f"{'Name':<15} {'Phone':<15} {'Email':<20}")
    print("=" * 50)
    for name, info in sorted(contacts.items()):
        print(f"{name:<15} {info['phone']:<15} {info['email']:<20}")
    print("=" * 50)

def search_contact(contacts):
    """Search for a contact by name."""
    name = input("Enter name to search: ").strip()
    if name in contacts:
        info = contacts[name]
        print(f"\nName: {name}")
        print(f"Phone: {info['phone']}")
        print(f"Email: {info['email']}")
    else:
        print("Contact not found.")

def delete_contact(contacts):
    """Delete a contact."""
    name = input("Enter name to delete: ").strip()
    if name in contacts:
        del contacts[name]
        save_contacts(contacts)
        print(f"Contact '{name}' deleted!")
    else:
        print("Contact not found.")

def main():
    """Main program loop."""
    contacts = load_contacts()

    while True:
        print("\n--- Contact Book ---")
        print("1. Add contact")
        print("2. View all contacts")
        print("3. Search contact")
        print("4. Delete contact")
        print("5. Exit")

        choice = input("\nEnter choice (1-5): ").strip()

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            view_contacts(contacts)
        elif choice == "3":
            search_contact(contacts)
        elif choice == "4":
            delete_contact(contacts)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
```

---

## Key Takeaways

1. **Lists** are ordered, mutable collections with indexing and slicing
2. **Tuples** are immutable lists, good for fixed data
3. **Dictionaries** store key-value pairs for fast lookups
4. **Sets** store unique items with fast membership testing
5. **String methods** provide powerful text manipulation
6. **f-strings** are the modern way to format strings
7. **File I/O** with `with` statements auto-closes files
8. Always use `with open()` for file operations

---

## Next Week Preview
Week 4 covers error handling with try/except to make your programs more robust.
