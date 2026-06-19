# Week 19: Pandas Basics

## Overview
This week begins the Data Track. You'll learn Pandas, Python's most popular data analysis library, including DataFrames, Series, and basic data operations.

---

## Part 1: Introduction to Pandas

### Installation

```bash
pip install pandas
```

### Basic Imports

```python
import pandas as pd
import numpy as np
```

### Why Pandas?
- Handle tabular data efficiently
- Read/write many file formats (CSV, Excel, JSON, SQL)
- Powerful data manipulation and analysis
- Handles missing data gracefully
- Fast operations on large datasets

---

## Part 2: Series

A Series is a one-dimensional labeled array.

```python
import pandas as pd

# Create from list
s = pd.Series([1, 2, 3, 4, 5])
print(s)

# With custom index
s = pd.Series([10, 20, 30], index=["a", "b", "c"])
print(s["a"])  # 10

# From dictionary
data = {"apple": 100, "banana": 50, "orange": 75}
s = pd.Series(data)

# Access elements
print(s["apple"])    # 100
print(s[0])          # 100
print(s[1:3])        # banana and orange

# Operations
print(s * 2)         # Multiply all values
print(s > 60)        # Boolean mask
print(s[s > 60])     # Filtered values
```

---

## Part 3: DataFrames

A DataFrame is a 2D labeled data structure (like a spreadsheet).

### Creating DataFrames

```python
import pandas as pd

# From dictionary
data = {
    "name": ["Alice", "Bob", "Charlie"],
    "age": [25, 30, 35],
    "city": ["NYC", "LA", "Chicago"]
}
df = pd.DataFrame(data)

# From list of dictionaries
data = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
    {"name": "Charlie", "age": 35}
]
df = pd.DataFrame(data)

# With custom index
df = pd.DataFrame(data, index=["a", "b", "c"])

# From NumPy array
import numpy as np
arr = np.array([[1, 2], [3, 4], [5, 6]])
df = pd.DataFrame(arr, columns=["A", "B"])
```

### Reading Files

```python
# CSV
df = pd.read_csv("data.csv")

# With options
df = pd.read_csv(
    "data.csv",
    sep=",",                    # Delimiter
    header=0,                   # Row for column names
    index_col="id",             # Column to use as index
    usecols=["name", "age"],    # Columns to read
    nrows=100,                  # Number of rows
    skiprows=1,                 # Skip first row
    na_values=["NA", "N/A"],    # Values to treat as NaN
    dtype={"age": int}          # Column data types
)

# Excel
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")

# JSON
df = pd.read_json("data.json")

# SQL
import sqlite3
conn = sqlite3.connect("database.db")
df = pd.read_sql("SELECT * FROM users", conn)
```

### Writing Files

```python
# CSV
df.to_csv("output.csv", index=False)

# Excel
df.to_excel("output.xlsx", index=False)

# JSON
df.to_json("output.json", orient="records")
```

---

## Part 4: Exploring DataFrames

```python
import pandas as pd

df = pd.read_csv("data.csv")

# Basic info
print(df.head())        # First 5 rows
print(df.tail())        # Last 5 rows
print(df.shape)         # (rows, columns)
print(df.columns)       # Column names
print(df.dtypes)        # Data types
print(df.info())        # Summary info
print(df.describe())    # Statistics

# Unique values
print(df["column"].unique())
print(df["column"].nunique())
print(df["column"].value_counts())
```

---

## Part 5: Selecting Data

### Column Selection

```python
# Single column (returns Series)
df["name"]
df.name

# Multiple columns (returns DataFrame)
df[["name", "age"]]
```

### Row Selection

```python
# By index position (iloc)
df.iloc[0]           # First row
df.iloc[0:3]         # First 3 rows
df.iloc[[0, 2, 4]]   # Specific rows

# By label (loc)
df.loc["a"]          # Row with label "a"
df.loc["a":"c"]      # Rows from "a" to "c"

# Both rows and columns
df.iloc[0:3, 0:2]    # Rows 0-2, columns 0-1
df.loc["a":"c", ["name", "age"]]
```

### Boolean Selection

```python
# Filter rows
df[df["age"] > 25]
df[df["city"] == "NYC"]

# Multiple conditions
df[(df["age"] > 25) & (df["city"] == "NYC")]
df[(df["age"] < 25) | (df["age"] > 35)]

# isin
df[df["city"].isin(["NYC", "LA"])]

# Query string
df.query("age > 25 and city == 'NYC'")
```

---

## Part 6: Modifying DataFrames

### Adding Columns

```python
# New column
df["country"] = "USA"

# Calculated column
df["age_in_months"] = df["age"] * 12

# From function
df["name_upper"] = df["name"].apply(str.upper)

# Conditional
df["adult"] = df["age"].apply(lambda x: "Yes" if x >= 18 else "No")
df["adult"] = np.where(df["age"] >= 18, "Yes", "No")
```

### Modifying Values

```python
# Set single value
df.loc[0, "name"] = "Alexandra"
df.iloc[0, 0] = "Alexandra"

# Set multiple values
df.loc[df["city"] == "NYC", "state"] = "NY"

# Replace values
df["city"] = df["city"].replace("NYC", "New York City")
df["city"].replace({"NYC": "New York", "LA": "Los Angeles"}, inplace=True)
```

### Removing Data

```python
# Drop columns
df = df.drop("column_name", axis=1)
df = df.drop(["col1", "col2"], axis=1)

# Drop rows
df = df.drop(0)          # By index
df = df.drop([0, 1, 2])  # Multiple

# Drop by condition
df = df[df["age"] >= 18]  # Keep only adults

# Drop duplicates
df = df.drop_duplicates()
df = df.drop_duplicates(subset=["name", "email"])
df = df.drop_duplicates(keep="last")
```

---

## Part 7: Sorting

```python
# Sort by values
df = df.sort_values("age")
df = df.sort_values("age", ascending=False)
df = df.sort_values(["city", "age"])

# Sort by index
df = df.sort_index()

# Reset index
df = df.reset_index(drop=True)
```

---

## Part 8: Basic Statistics

```python
# Numeric columns
df["age"].sum()
df["age"].mean()
df["age"].median()
df["age"].std()
df["age"].min()
df["age"].max()

# Multiple stats
df["age"].describe()

# All numeric columns
df.describe()

# Counts
df["city"].value_counts()
df["city"].value_counts(normalize=True)  # Percentages

# Correlation
df.corr()
```

---

## Part 9: Grouping

```python
# Group by single column
grouped = df.groupby("city")

# Aggregations
grouped["age"].mean()
grouped["age"].agg(["mean", "min", "max"])

# Multiple columns
df.groupby(["city", "gender"])["age"].mean()

# Multiple aggregations
df.groupby("city").agg({
    "age": ["mean", "count"],
    "salary": "sum"
})

# Custom aggregation
df.groupby("city")["age"].apply(lambda x: x.max() - x.min())
```

---

## Part 10: Practice with Real Data

```python
import pandas as pd

# Create sample dataset
data = {
    "date": pd.date_range("2024-01-01", periods=100, freq="D"),
    "product": np.random.choice(["A", "B", "C"], 100),
    "quantity": np.random.randint(1, 50, 100),
    "price": np.random.uniform(10, 100, 100).round(2),
    "region": np.random.choice(["North", "South", "East", "West"], 100)
}
df = pd.DataFrame(data)

# Calculate revenue
df["revenue"] = df["quantity"] * df["price"]

# Explore
print(df.head())
print(df.info())
print(df.describe())

# Analysis
print("\nSales by product:")
print(df.groupby("product")["revenue"].sum())

print("\nSales by region:")
print(df.groupby("region")["revenue"].sum().sort_values(ascending=False))

print("\nDaily average:")
print(df.groupby("date")["revenue"].sum().mean())

# Top selling days
top_days = df.groupby("date")["revenue"].sum().nlargest(5)
print("\nTop 5 days:")
print(top_days)
```

---

## Week 19 Project: Explore a Kaggle Dataset

```python
import pandas as pd
import numpy as np

# Download a dataset from Kaggle (e.g., Titanic, or any CSV)
# For this example, we'll create a similar dataset

# Load your dataset
df = pd.read_csv("your_dataset.csv")

# 1. Basic exploration
print("Shape:", df.shape)
print("\nColumn types:")
print(df.dtypes)
print("\nFirst 5 rows:")
print(df.head())
print("\nBasic statistics:")
print(df.describe())
print("\nMissing values:")
print(df.isnull().sum())

# 2. Data questions to answer:
# - What are the unique values in categorical columns?
# - What's the distribution of numeric columns?
# - Are there patterns between columns?

# 3. Clean the data
# - Handle missing values
# - Fix data types
# - Remove duplicates

# 4. Analyze
# - Group by categories
# - Calculate aggregations
# - Find correlations

# 5. Save cleaned data
df.to_csv("cleaned_dataset.csv", index=False)
```

---

## Key Takeaways

1. **Series** is 1D, **DataFrame** is 2D
2. Use **read_csv()** to load data, **to_csv()** to save
3. **iloc** for position-based indexing, **loc** for label-based
4. **Boolean indexing** for filtering rows
5. **groupby()** for aggregating data
6. **describe()** gives quick statistics
7. Always explore data before analysis
8. Handle missing values appropriately

---

## Next Week Preview
Week 20 covers data cleaning: handling nulls, duplicates, and type conversions.
