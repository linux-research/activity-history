# Week 6: Object-Oriented Programming (OOP) Part 1

## Overview
This week introduces Object-Oriented Programming - a paradigm for organizing code around "objects" that combine data and behavior. You'll learn about classes, objects, attributes, and methods.

---

## Part 1: Why OOP?

### The Problem with Procedural Code

```python
# Managing bank accounts without OOP
account1_balance = 1000
account1_owner = "Alice"

account2_balance = 500
account2_owner = "Bob"

def deposit(balance, amount):
    return balance + amount

def withdraw(balance, amount):
    if amount <= balance:
        return balance - amount
    return balance

# Awkward to manage multiple accounts
account1_balance = deposit(account1_balance, 200)
account2_balance = withdraw(account2_balance, 100)
```

### The OOP Solution

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount

# Clean and organized
account1 = BankAccount("Alice", 1000)
account2 = BankAccount("Bob", 500)

account1.deposit(200)
account2.withdraw(100)
```

---

## Part 2: Classes and Objects

### Basic Terminology
- **Class**: A blueprint/template for creating objects
- **Object**: An instance of a class
- **Attribute**: Data stored in an object
- **Method**: A function that belongs to a class

### Creating a Class

```python
class Dog:
    # Class attribute (shared by all instances)
    species = "Canis familiaris"

    # Constructor (initializer)
    def __init__(self, name, age):
        # Instance attributes (unique to each instance)
        self.name = name
        self.age = age

    # Instance method
    def bark(self):
        print(f"{self.name} says woof!")

    # Instance method
    def description(self):
        return f"{self.name} is {self.age} years old"

# Creating objects (instances)
buddy = Dog("Buddy", 3)
max = Dog("Max", 5)

# Accessing attributes
print(buddy.name)      # Buddy
print(max.age)         # 5
print(buddy.species)   # Canis familiaris

# Calling methods
buddy.bark()           # Buddy says woof!
print(max.description())  # Max is 5 years old
```

---

## Part 3: The __init__ Method

The `__init__` method is called automatically when creating an object:

```python
class Person:
    def __init__(self, name, age, email=None):
        """Initialize a new Person.

        Args:
            name: Person's name (required)
            age: Person's age (required)
            email: Person's email (optional)
        """
        self.name = name
        self.age = age
        self.email = email
        self.created_at = datetime.now()  # Set automatically

# Different ways to create
p1 = Person("Alice", 30)
p2 = Person("Bob", 25, "bob@email.com")
p3 = Person(name="Charlie", age=35, email="c@test.com")
```

### Default Values and Validation

```python
class Product:
    def __init__(self, name, price, quantity=0):
        # Validation in __init__
        if not name:
            raise ValueError("Name cannot be empty")
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")

        self.name = name
        self.price = price
        self.quantity = quantity

# Validation happens on creation
try:
    p = Product("Widget", -10)  # Raises ValueError
except ValueError as e:
    print(f"Error: {e}")
```

---

## Part 4: Instance Methods

Methods are functions that operate on an instance:

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        """Calculate the area."""
        return self.width * self.height

    def perimeter(self):
        """Calculate the perimeter."""
        return 2 * (self.width + self.height)

    def is_square(self):
        """Check if rectangle is a square."""
        return self.width == self.height

    def scale(self, factor):
        """Scale the rectangle by a factor."""
        self.width *= factor
        self.height *= factor

    def describe(self):
        """Return a description of the rectangle."""
        shape = "square" if self.is_square() else "rectangle"
        return f"A {shape} of {self.width}x{self.height}"

# Using methods
rect = Rectangle(10, 5)
print(rect.area())       # 50
print(rect.perimeter())  # 30
print(rect.is_square())  # False

rect.scale(2)
print(rect.describe())   # A rectangle of 20x10
```

### The self Parameter

`self` refers to the current instance:

```python
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1  # self.count refers to this instance's count

    def get_count(self):
        return self.count

c1 = Counter()
c2 = Counter()

c1.increment()
c1.increment()
c2.increment()

print(c1.get_count())  # 2
print(c2.get_count())  # 1
```

---

## Part 5: Class vs Instance Attributes

```python
class Employee:
    # Class attribute - shared by all instances
    company = "TechCorp"
    employee_count = 0

    def __init__(self, name, salary):
        # Instance attributes - unique to each instance
        self.name = name
        self.salary = salary
        Employee.employee_count += 1  # Modify class attribute

    def display(self):
        print(f"{self.name} works at {self.company}")

# Create employees
e1 = Employee("Alice", 50000)
e2 = Employee("Bob", 60000)

# Class attribute is shared
print(e1.company)  # TechCorp
print(e2.company)  # TechCorp
print(Employee.employee_count)  # 2

# Changing class attribute affects all instances
Employee.company = "NewTech"
print(e1.company)  # NewTech
print(e2.company)  # NewTech

# But assigning to instance creates instance attribute
e1.company = "OtherCorp"
print(e1.company)  # OtherCorp (instance attribute)
print(e2.company)  # NewTech (still class attribute)
```

---

## Part 6: Encapsulation (Private Attributes)

Python uses naming conventions for "private" attributes:

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance        # Convention: "protected"
        self.__pin = "1234"            # Name mangling: "private"

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        return False

    def withdraw(self, amount, pin):
        if pin != self.__pin:
            raise ValueError("Invalid PIN")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        return amount

    def get_balance(self):
        return self._balance

account = BankAccount("Alice", 1000)

# Can access (but shouldn't by convention)
print(account._balance)  # 1000

# Name-mangled attributes are harder to access
# print(account.__pin)  # AttributeError
print(account._BankAccount__pin)  # "1234" (still accessible but discouraged)

# Proper way - use methods
print(account.get_balance())  # 1000
```

### Properties (Getters and Setters)

```python
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self):
        """Get temperature in Celsius."""
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        """Set temperature in Celsius."""
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value

    @property
    def fahrenheit(self):
        """Get temperature in Fahrenheit."""
        return self._celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        """Set temperature in Fahrenheit."""
        self.celsius = (value - 32) * 5/9

# Using properties like attributes
temp = Temperature(25)
print(temp.celsius)     # 25
print(temp.fahrenheit)  # 77.0

temp.fahrenheit = 100
print(temp.celsius)     # 37.77...

# Validation happens automatically
try:
    temp.celsius = -300  # ValueError
except ValueError as e:
    print(e)
```

---

## Part 7: Practice Exercises

### Exercise 1: Simple Class

```python
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
        self.current_page = 1

    def read(self, pages):
        self.current_page += pages
        if self.current_page > self.pages:
            self.current_page = self.pages

    def progress(self):
        return (self.current_page / self.pages) * 100

    def __str__(self):
        return f"'{self.title}' by {self.author}"

book = Book("Python Basics", "John Smith", 300)
book.read(50)
print(f"Progress: {book.progress():.1f}%")  # 17.0%
```

---

## Week 6 Project: Bank Account Class

Build a complete BankAccount class:

```python
from datetime import datetime

class Transaction:
    """Represents a single transaction."""

    def __init__(self, trans_type, amount, balance_after):
        self.type = trans_type
        self.amount = amount
        self.balance_after = balance_after
        self.timestamp = datetime.now()

    def __str__(self):
        time_str = self.timestamp.strftime("%Y-%m-%d %H:%M")
        return f"{time_str} | {self.type:10} | ${self.amount:>10.2f} | Balance: ${self.balance_after:>10.2f}"


class BankAccount:
    """A bank account with transaction history."""

    # Class attribute - shared interest rate
    interest_rate = 0.02  # 2% annual

    def __init__(self, owner, account_number, initial_balance=0):
        """
        Initialize a new bank account.

        Args:
            owner: Account owner's name
            account_number: Unique account identifier
            initial_balance: Starting balance (default 0)
        """
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")

        self.owner = owner
        self.account_number = account_number
        self._balance = initial_balance
        self._transactions = []
        self._is_active = True
        self._created_at = datetime.now()

        if initial_balance > 0:
            self._record_transaction("DEPOSIT", initial_balance)

    @property
    def balance(self):
        """Get current balance (read-only)."""
        return self._balance

    @property
    def is_active(self):
        """Check if account is active."""
        return self._is_active

    def _record_transaction(self, trans_type, amount):
        """Record a transaction (internal method)."""
        trans = Transaction(trans_type, amount, self._balance)
        self._transactions.append(trans)

    def deposit(self, amount):
        """
        Deposit money into the account.

        Args:
            amount: Amount to deposit (must be positive)

        Returns:
            New balance after deposit
        """
        if not self._is_active:
            raise ValueError("Account is not active")
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        self._balance += amount
        self._record_transaction("DEPOSIT", amount)
        return self._balance

    def withdraw(self, amount):
        """
        Withdraw money from the account.

        Args:
            amount: Amount to withdraw

        Returns:
            Amount withdrawn
        """
        if not self._is_active:
            raise ValueError("Account is not active")
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise ValueError(f"Insufficient funds. Available: ${self._balance:.2f}")

        self._balance -= amount
        self._record_transaction("WITHDRAWAL", amount)
        return amount

    def transfer(self, other_account, amount):
        """
        Transfer money to another account.

        Args:
            other_account: Destination BankAccount
            amount: Amount to transfer
        """
        if not isinstance(other_account, BankAccount):
            raise TypeError("Can only transfer to another BankAccount")

        self.withdraw(amount)
        other_account.deposit(amount)

        # Update transaction types
        self._transactions[-1].type = "TRANSFER OUT"
        other_account._transactions[-1].type = "TRANSFER IN"

    def apply_interest(self):
        """Apply annual interest to the account."""
        if self._balance > 0:
            interest = self._balance * self.interest_rate
            self._balance += interest
            self._record_transaction("INTEREST", interest)
            return interest
        return 0

    def get_statement(self, num_transactions=10):
        """
        Get recent transaction history.

        Args:
            num_transactions: Number of recent transactions to show

        Returns:
            Formatted statement string
        """
        lines = [
            "=" * 70,
            f"Account Statement - {self.owner}",
            f"Account Number: {self.account_number}",
            f"Current Balance: ${self._balance:.2f}",
            "=" * 70,
            "",
            "Recent Transactions:",
            "-" * 70
        ]

        recent = self._transactions[-num_transactions:]
        for trans in recent:
            lines.append(str(trans))

        lines.append("-" * 70)
        return "\n".join(lines)

    def close_account(self):
        """Close the account and return remaining balance."""
        if not self._is_active:
            raise ValueError("Account is already closed")

        final_balance = self._balance
        self._balance = 0
        self._is_active = False
        self._record_transaction("ACCOUNT CLOSED", final_balance)
        return final_balance

    def __str__(self):
        status = "Active" if self._is_active else "Closed"
        return f"Account({self.account_number}) - {self.owner} - ${self._balance:.2f} [{status}]"

    def __repr__(self):
        return f"BankAccount('{self.owner}', '{self.account_number}', {self._balance})"


def main():
    """Demo the BankAccount class."""

    # Create accounts
    alice = BankAccount("Alice Smith", "ACC001", 1000)
    bob = BankAccount("Bob Jones", "ACC002", 500)

    print("Initial accounts:")
    print(alice)
    print(bob)
    print()

    # Perform transactions
    alice.deposit(500)
    alice.withdraw(200)
    bob.deposit(1000)

    # Transfer between accounts
    print("Transferring $300 from Alice to Bob...")
    alice.transfer(bob, 300)

    # Apply interest
    alice.apply_interest()
    bob.apply_interest()

    # Print statements
    print("\n" + alice.get_statement())
    print("\n" + bob.get_statement())

    # Test error handling
    print("\nTesting error handling:")

    try:
        alice.withdraw(10000)
    except ValueError as e:
        print(f"Withdrawal error: {e}")

    try:
        alice.deposit(-100)
    except ValueError as e:
        print(f"Deposit error: {e}")


if __name__ == "__main__":
    main()
```

---

## Key Takeaways

1. **Classes** are blueprints for creating objects
2. **__init__** initializes new objects with attributes
3. **self** refers to the current instance
4. **Instance attributes** are unique to each object
5. **Class attributes** are shared by all instances
6. **Methods** are functions that belong to a class
7. Use **_underscore** for "protected" attributes (convention)
8. Use **@property** for controlled attribute access

---

## Next Week Preview
Week 7 covers OOP Part 2: inheritance, super(), method overriding, and dunder methods.
