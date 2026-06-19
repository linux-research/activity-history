# Week 1: Basics and Control Flow

## Overview
This week you'll set up your Python environment and learn the fundamental building blocks: variables, data types, input/output, and decision-making with conditionals.

---

## Part 1: Setting Up Python

### Installation
1. Download Python from [python.org](https://python.org) (version 3.10+)
2. During installation, check "Add Python to PATH"
3. Verify installation:
```bash
python --version
# or
python3 --version
```

### Choose an Editor
- **Beginner-friendly:** VS Code with Python extension
- **Lightweight:** Sublime Text, Atom
- **Full IDE:** PyCharm Community Edition

### Your First Program
Create a file called `hello.py`:
```python
print("Hello, World!")
```

Run it:
```bash
python hello.py
```

---

## Part 2: Variables and Data Types

### Variables
Variables store data. Python is dynamically typed - no need to declare types.

```python
# Creating variables
name = "Alice"
age = 25
height = 1.75
is_student = True

# Variable naming rules
# - Must start with letter or underscore
# - Can contain letters, numbers, underscores
# - Case-sensitive (age and Age are different)
# - Use snake_case for readability

user_name = "bob"      # Good
userName = "bob"       # Works but not Pythonic
2name = "bob"          # Error! Can't start with number
```

### Data Types

#### Integers (int)
Whole numbers, positive or negative.
```python
count = 42
negative = -10
big_number = 1_000_000  # Underscores for readability

print(type(count))  # <class 'int'>
```

#### Floats (float)
Decimal numbers.
```python
price = 19.99
pi = 3.14159
scientific = 2.5e6  # 2,500,000

print(type(price))  # <class 'float'>
```

#### Strings (str)
Text data, enclosed in quotes.
```python
single = 'Hello'
double = "World"
multi_line = """This is
a multi-line
string"""

# String operations
greeting = "Hello" + " " + "World"  # Concatenation
repeated = "Ha" * 3                  # "HaHaHa"
length = len(greeting)               # 11
```

#### Booleans (bool)
True or False values.
```python
is_active = True
is_deleted = False

print(type(is_active))  # <class 'bool'>
```

#### None
Represents absence of value.
```python
result = None
```

---

## Part 3: print() and input()

### print() Function
Output data to the console.

```python
# Basic printing
print("Hello!")
print(42)
print(3.14)

# Printing multiple values
name = "Alice"
age = 25
print("Name:", name, "Age:", age)

# Using sep and end parameters
print("A", "B", "C", sep="-")      # A-B-C
print("Hello", end=" ")
print("World")                      # Hello World (same line)

# f-strings (formatted strings) - IMPORTANT!
name = "Bob"
age = 30
print(f"My name is {name} and I'm {age} years old.")
print(f"Next year I'll be {age + 1}.")
```

### input() Function
Get data from the user.

```python
# Basic input (always returns a string!)
name = input("Enter your name: ")
print(f"Hello, {name}!")

# Converting input to numbers
age_str = input("Enter your age: ")
age = int(age_str)                    # Convert to integer
print(f"Next year you'll be {age + 1}")

# Shorter version
age = int(input("Enter your age: "))

# For decimal numbers
price = float(input("Enter price: "))
```

---

## Part 4: Operators

### Arithmetic Operators
```python
a = 10
b = 3

print(a + b)   # 13  Addition
print(a - b)   # 7   Subtraction
print(a * b)   # 30  Multiplication
print(a / b)   # 3.333...  Division (always float)
print(a // b)  # 3   Floor division (integer)
print(a % b)   # 1   Modulo (remainder)
print(a ** b)  # 1000  Exponentiation
```

### Comparison Operators
Return True or False.
```python
x = 5
y = 10

print(x == y)   # False  Equal to
print(x != y)   # True   Not equal to
print(x < y)    # True   Less than
print(x > y)    # False  Greater than
print(x <= y)   # True   Less than or equal
print(x >= y)   # False  Greater than or equal
```

### Logical Operators
Combine boolean expressions.
```python
a = True
b = False

print(a and b)  # False - both must be True
print(a or b)   # True  - at least one True
print(not a)    # False - inverts the value

# Practical example
age = 25
has_license = True
can_drive = age >= 18 and has_license  # True
```

---

## Part 5: Control Flow (if/elif/else)

### Basic if Statement
```python
age = 20

if age >= 18:
    print("You are an adult.")
```

### if-else Statement
```python
age = 15

if age >= 18:
    print("You are an adult.")
else:
    print("You are a minor.")
```

### if-elif-else Statement
```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Your grade is {grade}")
```

### Nested Conditions
```python
age = 25
has_ticket = True

if age >= 18:
    if has_ticket:
        print("You can enter the concert.")
    else:
        print("You need a ticket.")
else:
    print("You must be 18 or older.")
```

### Combining Conditions
```python
age = 25
is_member = True

# Using 'and'
if age >= 18 and is_member:
    print("Welcome, member!")

# Using 'or'
if age < 12 or age >= 65:
    print("You get a discount!")

# Using 'not'
is_banned = False
if not is_banned:
    print("Access granted.")
```

---

## Part 6: Practice Exercises

### Exercise 1: Personal Info
```python
# Get user info and display it formatted
name = input("What is your name? ")
age = int(input("How old are you? "))
city = input("Where do you live? ")

print(f"\nHello {name}!")
print(f"You are {age} years old and live in {city}.")
print(f"In 10 years, you'll be {age + 10}.")
```

### Exercise 2: Simple Calculator
```python
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

print(f"\n{num1} + {num2} = {num1 + num2}")
print(f"{num1} - {num2} = {num1 - num2}")
print(f"{num1} * {num2} = {num1 * num2}")
print(f"{num1} / {num2} = {num1 / num2}")
```

### Exercise 3: Age Checker
```python
age = int(input("Enter your age: "))

if age < 0:
    print("Invalid age!")
elif age < 13:
    print("You are a child.")
elif age < 20:
    print("You are a teenager.")
elif age < 60:
    print("You are an adult.")
else:
    print("You are a senior.")
```

---

## Week 1 Project: Number Guessing Game

Build a simple number guessing game:

```python
# Number Guessing Game
import random

# Generate a random number between 1 and 100
secret_number = random.randint(1, 100)

print("=" * 40)
print("Welcome to the Number Guessing Game!")
print("I'm thinking of a number between 1 and 100.")
print("=" * 40)

# Get the player's guess
guess = int(input("\nEnter your guess: "))

# Check the guess
if guess == secret_number:
    print("Congratulations! You got it!")
elif guess < secret_number:
    print(f"Too low! The number was {secret_number}.")
else:
    print(f"Too high! The number was {secret_number}.")

print("\nThanks for playing!")
```

### Challenge Extensions
1. Add input validation (check if guess is 1-100)
2. Tell the user if they were "very close" (within 5)
3. Add multiple difficulty levels (1-50, 1-100, 1-1000)

---

## Key Takeaways

1. **Variables** store data and don't need type declarations
2. **Data types**: int, float, str, bool, None
3. **print()** outputs data, **input()** gets user input (always as string)
4. **f-strings** are the modern way to format strings
5. **Comparison operators** return True/False
6. **if/elif/else** control program flow based on conditions
7. **Indentation matters** - Python uses it to define code blocks

---

## Next Week Preview
Week 2 covers loops (for, while) and functions - the building blocks for more complex programs.
