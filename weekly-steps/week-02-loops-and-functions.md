# Week 2: Loops and Functions

## Overview
This week you'll learn how to repeat actions with loops and organize code into reusable functions. These are essential building blocks for any program.

---

## Part 1: For Loops

### Basic for Loop
Iterate over a sequence of items.

```python
# Looping through a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Looping through a string
for char in "Hello":
    print(char)
```

### range() Function
Generate a sequence of numbers.

```python
# range(stop) - 0 to stop-1
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# range(start, stop) - start to stop-1
for i in range(2, 6):
    print(i)  # 2, 3, 4, 5

# range(start, stop, step)
for i in range(0, 10, 2):
    print(i)  # 0, 2, 4, 6, 8

# Counting backwards
for i in range(5, 0, -1):
    print(i)  # 5, 4, 3, 2, 1
```

### Practical Examples

```python
# Sum of numbers 1-100
total = 0
for i in range(1, 101):
    total += i
print(f"Sum: {total}")  # 5050

# Multiplication table
num = 7
for i in range(1, 11):
    print(f"{num} x {i} = {num * i}")

# Loop with index using enumerate()
colors = ["red", "green", "blue"]
for index, color in enumerate(colors):
    print(f"{index}: {color}")
```

---

## Part 2: While Loops

### Basic while Loop
Repeat while a condition is True.

```python
count = 0
while count < 5:
    print(count)
    count += 1  # Don't forget to update!
```

### Practical Examples

```python
# User input validation
password = ""
while password != "secret123":
    password = input("Enter password: ")
print("Access granted!")

# Menu system
choice = ""
while choice != "quit":
    print("\n1. Say hello")
    print("2. Say goodbye")
    print("Type 'quit' to exit")
    choice = input("Enter choice: ")

    if choice == "1":
        print("Hello!")
    elif choice == "2":
        print("Goodbye!")
```

### Infinite Loops (and how to avoid them)
```python
# This would run forever - DON'T DO THIS
# while True:
#     print("Forever!")

# Proper infinite loop with exit condition
while True:
    user_input = input("Enter 'exit' to quit: ")
    if user_input == "exit":
        break
    print(f"You entered: {user_input}")
```

---

## Part 3: Loop Control Statements

### break - Exit the loop immediately
```python
# Find first even number
numbers = [1, 3, 5, 8, 9, 10]
for num in numbers:
    if num % 2 == 0:
        print(f"First even number: {num}")
        break
```

### continue - Skip to next iteration
```python
# Print only odd numbers
for i in range(10):
    if i % 2 == 0:
        continue
    print(i)  # 1, 3, 5, 7, 9
```

### else with loops
The else block runs if the loop completes without break.

```python
# Search for a value
numbers = [1, 3, 5, 7, 9]
target = 4

for num in numbers:
    if num == target:
        print("Found!")
        break
else:
    print("Not found!")  # This runs because no break occurred
```

---

## Part 4: Nested Loops

```python
# Multiplication table
for i in range(1, 6):
    for j in range(1, 6):
        print(f"{i*j:3}", end=" ")
    print()  # New line after each row

# Output:
#   1   2   3   4   5
#   2   4   6   8  10
#   3   6   9  12  15
#   4   8  12  16  20
#   5  10  15  20  25

# Pattern printing
for i in range(1, 6):
    print("*" * i)
# *
# **
# ***
# ****
# *****
```

---

## Part 5: Functions Basics

### Defining and Calling Functions

```python
# Basic function
def greet():
    print("Hello, World!")

greet()  # Call the function

# Function with parameter
def greet_person(name):
    print(f"Hello, {name}!")

greet_person("Alice")
greet_person("Bob")
```

### Parameters and Arguments

```python
# Multiple parameters
def describe_pet(name, animal_type):
    print(f"{name} is a {animal_type}.")

describe_pet("Buddy", "dog")
describe_pet("Whiskers", "cat")

# Keyword arguments (order doesn't matter)
describe_pet(animal_type="hamster", name="Squeaky")

# Default parameter values
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Alice")              # Hello, Alice!
greet("Bob", "Hi")          # Hi, Bob!
greet("Charlie", "Hey")     # Hey, Charlie!
```

### Return Values

```python
# Returning a single value
def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # 8

# Returning multiple values
def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers)

low, high, total = get_stats([1, 2, 3, 4, 5])
print(f"Min: {low}, Max: {high}, Sum: {total}")

# Early return
def is_even(n):
    if n % 2 == 0:
        return True
    return False

# Shorter version
def is_even(n):
    return n % 2 == 0
```

---

## Part 6: Variable Scope

### Local vs Global Scope

```python
# Global variable
message = "Hello"

def greet():
    # Local variable (only exists inside function)
    name = "Alice"
    print(f"{message}, {name}!")

greet()
print(message)  # Works
# print(name)   # Error! name is not defined outside function
```

### The global Keyword

```python
counter = 0

def increment():
    global counter
    counter += 1

increment()
increment()
print(counter)  # 2
```

### Best Practice
Avoid global variables when possible. Pass values as parameters and return results.

```python
# Better approach
def increment(counter):
    return counter + 1

count = 0
count = increment(count)
count = increment(count)
print(count)  # 2
```

---

## Part 7: Practice Exercises

### Exercise 1: FizzBuzz
```python
def fizzbuzz(n):
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)

fizzbuzz(20)
```

### Exercise 2: Factorial
```python
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

print(factorial(5))  # 120 (5 * 4 * 3 * 2 * 1)
```

### Exercise 3: Prime Checker
```python
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# Test it
for num in range(1, 20):
    if is_prime(num):
        print(f"{num} is prime")
```

---

## Week 2 Project: Temperature Converter

Build a temperature converter with multiple functions:

```python
def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32

def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5/9

def celsius_to_kelvin(celsius):
    """Convert Celsius to Kelvin."""
    return celsius + 273.15

def kelvin_to_celsius(kelvin):
    """Convert Kelvin to Celsius."""
    return kelvin - 273.15

def display_menu():
    """Display the conversion menu."""
    print("\n" + "=" * 40)
    print("Temperature Converter")
    print("=" * 40)
    print("1. Celsius to Fahrenheit")
    print("2. Fahrenheit to Celsius")
    print("3. Celsius to Kelvin")
    print("4. Kelvin to Celsius")
    print("5. Exit")
    print("=" * 40)

def main():
    """Main program loop."""
    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == "5":
            print("Goodbye!")
            break

        if choice not in ["1", "2", "3", "4"]:
            print("Invalid choice. Please try again.")
            continue

        temp = float(input("Enter temperature: "))

        if choice == "1":
            result = celsius_to_fahrenheit(temp)
            print(f"{temp}°C = {result:.2f}°F")
        elif choice == "2":
            result = fahrenheit_to_celsius(temp)
            print(f"{temp}°F = {result:.2f}°C")
        elif choice == "3":
            result = celsius_to_kelvin(temp)
            print(f"{temp}°C = {result:.2f}K")
        elif choice == "4":
            result = kelvin_to_celsius(temp)
            print(f"{temp}K = {result:.2f}°C")

# Run the program
main()
```

### FizzBuzz Solution

```python
def fizzbuzz():
    """Print FizzBuzz from 1 to 100."""
    for i in range(1, 101):
        output = ""
        if i % 3 == 0:
            output += "Fizz"
        if i % 5 == 0:
            output += "Buzz"
        print(output if output else i)

fizzbuzz()
```

---

## Key Takeaways

1. **for loops** iterate over sequences (lists, strings, range)
2. **while loops** repeat while a condition is True
3. **break** exits a loop, **continue** skips to next iteration
4. **Functions** organize code into reusable blocks
5. **Parameters** pass data into functions
6. **return** sends data back from functions
7. **Scope** determines where variables are accessible
8. Use **descriptive names** for functions and variables

---

## Next Week Preview
Week 3 covers data structures (lists, tuples, dictionaries, sets), string methods, and file I/O.
