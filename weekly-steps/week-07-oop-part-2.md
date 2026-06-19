# Week 7: Object-Oriented Programming (OOP) Part 2

## Overview
This week covers advanced OOP concepts: inheritance, the super() function, method overriding, and special "dunder" methods that customize object behavior.

---

## Part 1: Inheritance Basics

Inheritance allows a class to inherit attributes and methods from another class.

```python
# Parent class (base class, superclass)
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def speak(self):
        print("Some sound")

    def describe(self):
        return f"{self.name} is {self.age} years old"

# Child class (derived class, subclass)
class Dog(Animal):
    def speak(self):
        print(f"{self.name} says Woof!")

class Cat(Animal):
    def speak(self):
        print(f"{self.name} says Meow!")

# Using inheritance
dog = Dog("Buddy", 3)
cat = Cat("Whiskers", 5)

print(dog.describe())  # Inherited from Animal
dog.speak()            # Overridden in Dog

print(cat.describe())  # Inherited from Animal
cat.speak()            # Overridden in Cat
```

### Key Concepts
- **Parent/Base class**: The class being inherited from
- **Child/Derived class**: The class that inherits
- Child classes inherit all attributes and methods
- Child classes can override (replace) inherited methods

---

## Part 2: The super() Function

`super()` calls the parent class's methods:

```python
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def describe(self):
        return f"{self.name} is {self.age} years old"

class Dog(Animal):
    def __init__(self, name, age, breed):
        # Call parent's __init__
        super().__init__(name, age)
        # Add child-specific attribute
        self.breed = breed

    def describe(self):
        # Extend parent's method
        base = super().describe()
        return f"{base} and is a {self.breed}"

dog = Dog("Buddy", 3, "Golden Retriever")
print(dog.name)       # Buddy (inherited)
print(dog.breed)      # Golden Retriever (Dog-specific)
print(dog.describe()) # Buddy is 3 years old and is a Golden Retriever
```

### Why Use super()?
1. **Avoid repetition**: Don't copy parent's initialization code
2. **Maintainability**: Changes to parent automatically apply
3. **Multiple inheritance**: Properly handles complex hierarchies

---

## Part 3: Method Overriding

Child classes can replace inherited methods:

```python
class Shape:
    def area(self):
        return 0

    def describe(self):
        return f"A shape with area {self.area()}"

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        import math
        return math.pi * self.radius ** 2

# Polymorphism - same method, different behavior
shapes = [Rectangle(10, 5), Circle(7), Rectangle(3, 3)]

for shape in shapes:
    print(shape.describe())
```

### Polymorphism
Objects of different classes can be used interchangeably if they share a common interface:

```python
def print_area(shape):
    # Works with any object that has an area() method
    print(f"Area: {shape.area()}")

print_area(Rectangle(10, 5))  # Area: 50
print_area(Circle(7))          # Area: 153.93...
```

---

## Part 4: Checking Inheritance

```python
class Animal:
    pass

class Dog(Animal):
    pass

class Cat(Animal):
    pass

buddy = Dog()

# isinstance() - is object an instance of class?
print(isinstance(buddy, Dog))     # True
print(isinstance(buddy, Animal))  # True (Dog inherits Animal)
print(isinstance(buddy, Cat))     # False

# issubclass() - is class a subclass of another?
print(issubclass(Dog, Animal))    # True
print(issubclass(Cat, Animal))    # True
print(issubclass(Dog, Cat))       # False

# type() - exact type
print(type(buddy))                # <class '__main__.Dog'>
print(type(buddy) == Dog)         # True
print(type(buddy) == Animal)      # False (exact type is Dog)
```

---

## Part 5: Dunder (Magic) Methods

Dunder methods (`__name__`) customize object behavior:

### String Representation

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        """Human-readable string (for print, str())"""
        return f"{self.name}: ${self.price:.2f}"

    def __repr__(self):
        """Developer-readable string (for debugging, repr())"""
        return f"Product('{self.name}', {self.price})"

p = Product("Widget", 29.99)
print(p)        # Widget: $29.99 (uses __str__)
print(repr(p))  # Product('Widget', 29.99) (uses __repr__)
print([p])      # [Product('Widget', 29.99)] (lists use __repr__)
```

### Comparison Methods

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __eq__(self, other):
        """Equal: =="""
        if not isinstance(other, Person):
            return False
        return self.age == other.age

    def __lt__(self, other):
        """Less than: <"""
        return self.age < other.age

    def __le__(self, other):
        """Less than or equal: <="""
        return self.age <= other.age

    def __gt__(self, other):
        """Greater than: >"""
        return self.age > other.age

    def __ge__(self, other):
        """Greater than or equal: >="""
        return self.age >= other.age

alice = Person("Alice", 30)
bob = Person("Bob", 25)

print(alice > bob)   # True (30 > 25)
print(alice == bob)  # False

# Can now sort!
people = [alice, bob, Person("Charlie", 35)]
people.sort()  # Sorts by age using __lt__
```

### Arithmetic Methods

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        """Addition: +"""
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Subtraction: -"""
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        """Multiplication: *"""
        return Vector(self.x * scalar, self.y * scalar)

    def __neg__(self):
        """Negation: -obj"""
        return Vector(-self.x, -self.y)

    def __abs__(self):
        """Absolute value: abs()"""
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(v1 + v2)    # Vector(4, 6)
print(v1 - v2)    # Vector(2, 2)
print(v1 * 3)     # Vector(9, 12)
print(abs(v1))    # 5.0
print(-v1)        # Vector(-3, -4)
```

### Container Methods

```python
class Playlist:
    def __init__(self, name):
        self.name = name
        self._songs = []

    def add(self, song):
        self._songs.append(song)

    def __len__(self):
        """Length: len()"""
        return len(self._songs)

    def __getitem__(self, index):
        """Indexing: obj[index]"""
        return self._songs[index]

    def __setitem__(self, index, value):
        """Assignment: obj[index] = value"""
        self._songs[index] = value

    def __delitem__(self, index):
        """Deletion: del obj[index]"""
        del self._songs[index]

    def __contains__(self, item):
        """Membership: item in obj"""
        return item in self._songs

    def __iter__(self):
        """Iteration: for item in obj"""
        return iter(self._songs)

playlist = Playlist("My Mix")
playlist.add("Song A")
playlist.add("Song B")
playlist.add("Song C")

print(len(playlist))          # 3
print(playlist[0])            # Song A
print("Song B" in playlist)   # True

for song in playlist:
    print(song)
```

### Other Useful Dunders

```python
class Resource:
    def __init__(self, name):
        self.name = name
        print(f"Opening {name}")

    def __enter__(self):
        """Context manager entry: with obj as x"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        print(f"Closing {self.name}")
        return False  # Don't suppress exceptions

    def __call__(self, *args):
        """Make object callable: obj()"""
        print(f"Called with {args}")

    def __bool__(self):
        """Boolean conversion: bool(), if obj:"""
        return True

    def __hash__(self):
        """Hash for dict keys, sets"""
        return hash(self.name)

# Using __enter__ and __exit__
with Resource("file.txt") as r:
    print("Working with resource")
# Automatically calls __exit__

# Using __call__
r = Resource("test")
r("arg1", "arg2")  # Called with ('arg1', 'arg2')
```

---

## Part 6: Common Dunder Methods Reference

| Method | Purpose | Example Usage |
|--------|---------|---------------|
| `__init__` | Initialize object | `obj = Class()` |
| `__str__` | Human-readable string | `print(obj)` |
| `__repr__` | Developer string | `repr(obj)` |
| `__len__` | Length | `len(obj)` |
| `__getitem__` | Index access | `obj[key]` |
| `__setitem__` | Index assignment | `obj[key] = val` |
| `__delitem__` | Index deletion | `del obj[key]` |
| `__contains__` | Membership test | `item in obj` |
| `__iter__` | Iteration | `for x in obj` |
| `__next__` | Iterator next | `next(obj)` |
| `__eq__` | Equality | `obj == other` |
| `__lt__` | Less than | `obj < other` |
| `__add__` | Addition | `obj + other` |
| `__sub__` | Subtraction | `obj - other` |
| `__mul__` | Multiplication | `obj * other` |
| `__call__` | Call as function | `obj()` |
| `__enter__` | Context manager start | `with obj:` |
| `__exit__` | Context manager end | (automatic) |
| `__hash__` | Hash value | `hash(obj)` |
| `__bool__` | Boolean value | `bool(obj)` |

---

## Week 7 Project: Extended Bank Account with Inheritance

```python
from datetime import datetime

class Account:
    """Base class for all account types."""

    account_count = 0

    def __init__(self, owner, balance=0):
        if balance < 0:
            raise ValueError("Initial balance cannot be negative")

        Account.account_count += 1
        self.account_number = f"ACC{Account.account_count:06d}"
        self.owner = owner
        self._balance = balance
        self._created_at = datetime.now()
        self._transactions = []

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self._balance += amount
        self._log_transaction("DEPOSIT", amount)
        return self._balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        self._log_transaction("WITHDRAWAL", amount)
        return amount

    def _log_transaction(self, trans_type, amount):
        self._transactions.append({
            "type": trans_type,
            "amount": amount,
            "balance": self._balance,
            "timestamp": datetime.now()
        })

    def __str__(self):
        return f"{self.__class__.__name__}({self.account_number}) - {self.owner}: ${self._balance:.2f}"

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.owner}', {self._balance})"

    def __eq__(self, other):
        if not isinstance(other, Account):
            return False
        return self.account_number == other.account_number

    def __lt__(self, other):
        return self._balance < other._balance

    def __add__(self, other):
        """Combine balances (returns total, doesn't merge accounts)."""
        if isinstance(other, Account):
            return self._balance + other._balance
        elif isinstance(other, (int, float)):
            return self._balance + other
        raise TypeError(f"Cannot add Account and {type(other)}")


class SavingsAccount(Account):
    """Savings account with interest."""

    def __init__(self, owner, balance=0, interest_rate=0.02):
        super().__init__(owner, balance)
        self.interest_rate = interest_rate
        self._min_balance = 100  # Minimum balance requirement

    def withdraw(self, amount):
        """Override: enforce minimum balance."""
        if self._balance - amount < self._min_balance:
            raise ValueError(
                f"Cannot withdraw. Minimum balance of ${self._min_balance} required."
            )
        return super().withdraw(amount)

    def apply_interest(self):
        """Apply monthly interest."""
        if self._balance > 0:
            interest = self._balance * (self.interest_rate / 12)
            self._balance += interest
            self._log_transaction("INTEREST", interest)
            return interest
        return 0

    def __str__(self):
        return f"{super().__str__()} (Savings, {self.interest_rate:.1%} APR)"


class CheckingAccount(Account):
    """Checking account with overdraft protection."""

    def __init__(self, owner, balance=0, overdraft_limit=500):
        super().__init__(owner, balance)
        self.overdraft_limit = overdraft_limit
        self._overdraft_fee = 35

    def withdraw(self, amount):
        """Override: allow overdraft up to limit."""
        if amount <= 0:
            raise ValueError("Amount must be positive")

        available = self._balance + self.overdraft_limit
        if amount > available:
            raise ValueError(
                f"Exceeds overdraft limit. Available: ${available:.2f}"
            )

        self._balance -= amount

        # Apply overdraft fee if balance goes negative
        if self._balance < 0:
            self._balance -= self._overdraft_fee
            self._log_transaction("OVERDRAFT_FEE", self._overdraft_fee)

        self._log_transaction("WITHDRAWAL", amount)
        return amount

    @property
    def available_balance(self):
        """Total available including overdraft."""
        return self._balance + self.overdraft_limit

    def __str__(self):
        return f"{super().__str__()} (Checking, ${self.overdraft_limit} overdraft)"


class JointAccount(CheckingAccount):
    """Joint account with multiple owners."""

    def __init__(self, owners, balance=0, overdraft_limit=1000):
        if not owners or len(owners) < 2:
            raise ValueError("Joint account requires at least 2 owners")

        # Use first owner for base class, store all owners
        super().__init__(owners[0], balance, overdraft_limit)
        self.owners = list(owners)

    def add_owner(self, owner):
        if owner not in self.owners:
            self.owners.append(owner)

    def remove_owner(self, owner):
        if len(self.owners) <= 2:
            raise ValueError("Joint account must have at least 2 owners")
        self.owners.remove(owner)

    def __str__(self):
        owners_str = " & ".join(self.owners)
        return f"JointAccount({self.account_number}) - {owners_str}: ${self._balance:.2f}"


def main():
    """Demonstrate inheritance hierarchy."""

    # Create different account types
    savings = SavingsAccount("Alice", 1000, 0.03)
    checking = CheckingAccount("Bob", 500, 200)
    joint = JointAccount(["Charlie", "Diana"], 2000)

    accounts = [savings, checking, joint]

    print("=== All Accounts ===")
    for acc in accounts:
        print(acc)

    print("\n=== Testing SavingsAccount ===")
    savings.deposit(500)
    print(f"After deposit: ${savings.balance}")

    savings.apply_interest()
    print(f"After interest: ${savings.balance:.2f}")

    try:
        savings.withdraw(1400)  # Would go below minimum
    except ValueError as e:
        print(f"Withdrawal failed: {e}")

    print("\n=== Testing CheckingAccount ===")
    checking.withdraw(600)  # Uses overdraft
    print(f"After overdraft withdrawal: ${checking.balance}")
    print(f"Available balance: ${checking.available_balance}")

    print("\n=== Testing JointAccount ===")
    print(f"Owners: {joint.owners}")
    joint.add_owner("Eve")
    print(f"After adding Eve: {joint.owners}")

    print("\n=== Comparing Accounts ===")
    print(f"savings + checking = ${savings + checking:.2f}")

    # Sort by balance
    accounts.sort()
    print("\nSorted by balance:")
    for acc in accounts:
        print(f"  ${acc.balance:.2f} - {acc.owner if hasattr(acc, 'owner') else acc.owners}")


if __name__ == "__main__":
    main()
```

---

## Key Takeaways

1. **Inheritance** lets classes share code and behavior
2. **super()** calls parent class methods
3. **Method overriding** replaces inherited methods
4. **Polymorphism** allows interchangeable use of objects
5. **Dunder methods** customize built-in operations
6. `__str__` for users, `__repr__` for developers
7. Implement `__eq__` and `__lt__` for comparison/sorting
8. Implement `__len__`, `__getitem__` for container-like behavior

---

## Next Week Preview
Week 8 covers list comprehensions and functional programming tools: map(), filter(), and lambda.
