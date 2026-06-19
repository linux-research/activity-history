# Week 4: Error Handling

## Overview
This week you'll learn how to handle errors gracefully using try/except blocks, understand common exception types, and make your programs more robust.

---

## Part 1: Why Error Handling?

Without error handling, programs crash when something unexpected happens:

```python
# This crashes if user enters non-numeric input
age = int(input("Enter your age: "))  # User types "abc" -> CRASH!

# This crashes if file doesn't exist
with open("nonexistent.txt") as f:    # -> CRASH!
    content = f.read()

# This crashes on division by zero
result = 10 / 0                        # -> CRASH!
```

With error handling, you can catch these problems and respond appropriately.

---

## Part 2: Basic try/except

```python
# Catch any error
try:
    number = int(input("Enter a number: "))
    print(f"You entered: {number}")
except:
    print("That's not a valid number!")

# Catch specific exception
try:
    number = int(input("Enter a number: "))
except ValueError:
    print("Please enter a valid integer!")
```

### Multiple except Blocks

```python
try:
    x = int(input("Enter a number: "))
    result = 10 / x
    print(f"Result: {result}")
except ValueError:
    print("That's not a valid number!")
except ZeroDivisionError:
    print("Cannot divide by zero!")
```

### Catching Multiple Exceptions Together

```python
try:
    # some code
    pass
except (ValueError, TypeError):
    print("Value or Type error occurred!")
```

---

## Part 3: The else and finally Clauses

### else - Runs if no exception occurred

```python
try:
    number = int(input("Enter a number: "))
except ValueError:
    print("Invalid input!")
else:
    print(f"Success! You entered {number}")
```

### finally - Always runs (cleanup code)

```python
try:
    file = open("data.txt", "r")
    content = file.read()
except FileNotFoundError:
    print("File not found!")
finally:
    print("This always runs!")
    # Good place for cleanup
```

### Complete Structure

```python
try:
    # Code that might raise an exception
    result = risky_operation()
except SomeError:
    # Handle specific error
    handle_error()
except AnotherError:
    # Handle another error
    handle_other_error()
else:
    # Runs only if no exception
    process_result(result)
finally:
    # Always runs (cleanup)
    cleanup()
```

---

## Part 4: Common Exception Types

| Exception | When it occurs |
|-----------|----------------|
| `ValueError` | Wrong value type (e.g., `int("abc")`) |
| `TypeError` | Wrong data type in operation |
| `ZeroDivisionError` | Division by zero |
| `FileNotFoundError` | File doesn't exist |
| `KeyError` | Dictionary key not found |
| `IndexError` | List index out of range |
| `AttributeError` | Object doesn't have attribute |
| `NameError` | Variable not defined |
| `ImportError` | Module import fails |
| `IOError` | I/O operation fails |

### Examples

```python
# ValueError
int("hello")

# TypeError
"hello" + 5

# ZeroDivisionError
10 / 0

# FileNotFoundError
open("nonexistent.txt")

# KeyError
d = {"a": 1}
d["b"]

# IndexError
lst = [1, 2, 3]
lst[10]

# AttributeError
"hello".non_existent_method()

# NameError
print(undefined_variable)
```

---

## Part 5: Getting Exception Information

```python
try:
    number = int(input("Enter number: "))
except ValueError as e:
    print(f"Error: {e}")
    print(f"Error type: {type(e).__name__}")
```

### The Exception Object

```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error message: {e}")
    print(f"Error type: {type(e)}")
    print(f"Error args: {e.args}")
```

---

## Part 6: Raising Exceptions

You can raise exceptions intentionally:

```python
def set_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative!")
    if age > 150:
        raise ValueError("Age seems unrealistic!")
    return age

try:
    age = set_age(-5)
except ValueError as e:
    print(f"Invalid age: {e}")
```

### Re-raising Exceptions

```python
try:
    risky_operation()
except Exception as e:
    print(f"Logging error: {e}")
    raise  # Re-raise the same exception
```

---

## Part 7: Custom Exceptions

```python
class InsufficientFundsError(Exception):
    """Raised when account has insufficient funds."""
    pass

class InvalidAmountError(Exception):
    """Raised when amount is invalid."""
    pass

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive!")
        if amount > self.balance:
            raise InsufficientFundsError(
                f"Cannot withdraw ${amount}. Balance: ${self.balance}"
            )
        self.balance -= amount
        return self.balance

# Using custom exceptions
account = BankAccount(100)

try:
    account.withdraw(150)
except InsufficientFundsError as e:
    print(f"Error: {e}")
except InvalidAmountError as e:
    print(f"Error: {e}")
```

---

## Part 8: Best Practices

### 1. Be Specific with Exceptions

```python
# Bad - catches everything
try:
    do_something()
except:
    pass

# Good - catch specific exceptions
try:
    do_something()
except ValueError:
    handle_value_error()
except FileNotFoundError:
    handle_file_error()
```

### 2. Don't Silence Exceptions

```python
# Bad - silently ignores errors
try:
    important_operation()
except:
    pass

# Good - at least log the error
try:
    important_operation()
except Exception as e:
    print(f"Error occurred: {e}")
    # or log to file
```

### 3. Use try/except Close to the Source

```python
# Bad - too broad
try:
    data = load_data()
    process_data(data)
    save_results()
except:
    print("Something went wrong")

# Good - specific handling
try:
    data = load_data()
except FileNotFoundError:
    print("Data file not found")
    data = []

try:
    process_data(data)
except ValueError as e:
    print(f"Processing error: {e}")
```

### 4. Clean Up Resources in finally

```python
file = None
try:
    file = open("data.txt")
    process(file)
except FileNotFoundError:
    print("File not found")
finally:
    if file:
        file.close()

# Or better, use context manager:
try:
    with open("data.txt") as file:
        process(file)
except FileNotFoundError:
    print("File not found")
```

---

## Part 9: Input Validation Pattern

A common pattern for getting valid input:

```python
def get_integer(prompt, min_val=None, max_val=None):
    """Get a valid integer from user."""
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Value must be at least {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"Value must be at most {max_val}")
                continue
            return value
        except ValueError:
            print("Please enter a valid integer!")

# Usage
age = get_integer("Enter your age (1-120): ", 1, 120)
print(f"Your age is {age}")
```

---

## Week 4 Project: Hardened Contact Book

Take your Week 3 contact book and add error handling:

```python
import os

CONTACTS_FILE = "contacts.txt"

def load_contacts():
    """Load contacts from file with error handling."""
    contacts = {}
    try:
        with open(CONTACTS_FILE, "r") as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    parts = line.split("|")
                    if len(parts) != 3:
                        print(f"Warning: Skipping malformed line {line_num}")
                        continue
                    name, phone, email = parts
                    contacts[name] = {"phone": phone, "email": email}
                except Exception as e:
                    print(f"Warning: Error parsing line {line_num}: {e}")
    except FileNotFoundError:
        print("No existing contacts file. Starting fresh.")
    except PermissionError:
        print("Error: Cannot read contacts file (permission denied)")
    except Exception as e:
        print(f"Error loading contacts: {e}")
    return contacts

def save_contacts(contacts):
    """Save contacts to file with error handling."""
    try:
        with open(CONTACTS_FILE, "w") as file:
            for name, info in contacts.items():
                file.write(f"{name}|{info['phone']}|{info['email']}\n")
        return True
    except PermissionError:
        print("Error: Cannot write to contacts file (permission denied)")
        return False
    except Exception as e:
        print(f"Error saving contacts: {e}")
        return False

def get_non_empty_input(prompt):
    """Get non-empty input from user."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty!")

def validate_email(email):
    """Basic email validation."""
    if "@" not in email or "." not in email:
        raise ValueError("Invalid email format")
    return email

def validate_phone(phone):
    """Basic phone validation."""
    # Remove common separators
    cleaned = phone.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
    if not cleaned.replace("+", "").isdigit():
        raise ValueError("Phone should contain only digits and common separators")
    return phone

def add_contact(contacts):
    """Add a new contact with validation."""
    try:
        name = get_non_empty_input("Enter name: ")
        if name in contacts:
            overwrite = input("Contact exists. Overwrite? (y/n): ").lower()
            if overwrite != 'y':
                print("Cancelled.")
                return

        # Get and validate phone
        while True:
            phone = input("Enter phone: ").strip()
            try:
                phone = validate_phone(phone)
                break
            except ValueError as e:
                print(f"Invalid phone: {e}")

        # Get and validate email
        while True:
            email = input("Enter email: ").strip()
            try:
                email = validate_email(email)
                break
            except ValueError as e:
                print(f"Invalid email: {e}")

        contacts[name] = {"phone": phone, "email": email}
        if save_contacts(contacts):
            print(f"Contact '{name}' added successfully!")

    except KeyboardInterrupt:
        print("\nCancelled.")

def view_contacts(contacts):
    """Display all contacts."""
    if not contacts:
        print("No contacts found.")
        return

    print("\n" + "=" * 60)
    print(f"{'Name':<20} {'Phone':<15} {'Email':<25}")
    print("=" * 60)
    for name, info in sorted(contacts.items()):
        print(f"{name:<20} {info['phone']:<15} {info['email']:<25}")
    print("=" * 60)
    print(f"Total: {len(contacts)} contact(s)")

def search_contact(contacts):
    """Search for contacts."""
    if not contacts:
        print("No contacts to search.")
        return

    query = input("Enter search term: ").strip().lower()
    if not query:
        print("Search term cannot be empty.")
        return

    results = []
    for name, info in contacts.items():
        if (query in name.lower() or
            query in info['phone'].lower() or
            query in info['email'].lower()):
            results.append((name, info))

    if results:
        print(f"\nFound {len(results)} result(s):")
        for name, info in results:
            print(f"  {name}: {info['phone']}, {info['email']}")
    else:
        print("No contacts found matching your search.")

def delete_contact(contacts):
    """Delete a contact with confirmation."""
    if not contacts:
        print("No contacts to delete.")
        return

    name = input("Enter name to delete: ").strip()
    if name not in contacts:
        print("Contact not found.")
        return

    confirm = input(f"Delete '{name}'? (y/n): ").lower()
    if confirm == 'y':
        del contacts[name]
        if save_contacts(contacts):
            print(f"Contact '{name}' deleted.")
    else:
        print("Cancelled.")

def get_menu_choice():
    """Get valid menu choice from user."""
    while True:
        print("\n--- Contact Book ---")
        print("1. Add contact")
        print("2. View all contacts")
        print("3. Search contacts")
        print("4. Delete contact")
        print("5. Exit")

        choice = input("\nEnter choice (1-5): ").strip()
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        print("Invalid choice. Please enter 1-5.")

def main():
    """Main program loop with error handling."""
    print("Welcome to Contact Book!")
    contacts = load_contacts()

    try:
        while True:
            choice = get_menu_choice()

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

    except KeyboardInterrupt:
        print("\n\nExiting... Goodbye!")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print("Please report this bug.")

if __name__ == "__main__":
    main()
```

---

## Key Takeaways

1. **try/except** catches and handles exceptions gracefully
2. **Catch specific exceptions** instead of bare `except:`
3. **else** runs if no exception, **finally** always runs
4. **Common exceptions**: ValueError, TypeError, FileNotFoundError, KeyError
5. **raise** to intentionally raise exceptions
6. **Custom exceptions** for domain-specific errors
7. **Validate input** close to where it's received
8. **Never silently ignore** exceptions

---

## Next Week Preview
Week 5 covers modules and packages - organizing code and using Python's standard library.
