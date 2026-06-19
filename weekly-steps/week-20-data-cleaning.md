# Week 20: Data Cleaning

## Overview
This week covers data cleaning with Pandas: handling missing values, removing duplicates, fixing data types, and standardizing data.

---

## Part 1: Understanding Messy Data

Common data quality issues:
- **Missing values**: Empty cells, NaN, null
- **Duplicates**: Repeated rows
- **Inconsistent formatting**: "NYC", "New York", "new york"
- **Wrong data types**: Numbers stored as strings
- **Outliers**: Extreme or invalid values
- **Mixed data**: "25 years" instead of 25

---

## Part 2: Finding Missing Values

```python
import pandas as pd
import numpy as np

# Check for missing values
df.isnull()             # Boolean DataFrame
df.isnull().sum()       # Count per column
df.isnull().sum().sum() # Total count

# Percentage missing
(df.isnull().sum() / len(df) * 100).round(2)

# Rows with any missing value
df[df.isnull().any(axis=1)]

# Columns with missing values
df.columns[df.isnull().any()]

# Visualize missing data pattern
import seaborn as sns
sns.heatmap(df.isnull(), cbar=True)
```

---

## Part 3: Handling Missing Values

### Drop Missing Values

```python
# Drop rows with any NaN
df_clean = df.dropna()

# Drop rows where specific column is NaN
df_clean = df.dropna(subset=["name", "email"])

# Drop if all values are NaN
df_clean = df.dropna(how="all")

# Drop if threshold not met (keep rows with at least 3 non-NaN)
df_clean = df.dropna(thresh=3)

# Drop columns with missing values
df_clean = df.dropna(axis=1)
```

### Fill Missing Values

```python
# Fill with specific value
df["column"] = df["column"].fillna(0)
df["column"] = df["column"].fillna("Unknown")

# Fill with statistics
df["age"] = df["age"].fillna(df["age"].mean())
df["age"] = df["age"].fillna(df["age"].median())
df["city"] = df["city"].fillna(df["city"].mode()[0])

# Forward/backward fill
df["value"] = df["value"].fillna(method="ffill")  # Use previous value
df["value"] = df["value"].fillna(method="bfill")  # Use next value

# Fill with grouped statistics
df["age"] = df.groupby("city")["age"].transform(
    lambda x: x.fillna(x.mean())
)

# Interpolation (for numeric data)
df["value"] = df["value"].interpolate()
df["value"] = df["value"].interpolate(method="linear")
```

---

## Part 4: Handling Duplicates

```python
# Find duplicates
df.duplicated()                    # Boolean mask
df.duplicated().sum()              # Count
df[df.duplicated()]                # View duplicates
df[df.duplicated(keep=False)]      # All duplicate rows

# Check specific columns
df.duplicated(subset=["name", "email"])

# Remove duplicates
df_clean = df.drop_duplicates()
df_clean = df.drop_duplicates(subset=["email"])
df_clean = df.drop_duplicates(keep="first")  # Keep first occurrence
df_clean = df.drop_duplicates(keep="last")   # Keep last occurrence
df_clean = df.drop_duplicates(keep=False)    # Remove all duplicates
```

---

## Part 5: Data Type Conversion

```python
# Check data types
df.dtypes

# Convert types
df["age"] = df["age"].astype(int)
df["price"] = df["price"].astype(float)
df["name"] = df["name"].astype(str)

# Convert to datetime
df["date"] = pd.to_datetime(df["date"])
df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
df["date"] = pd.to_datetime(df["date"], errors="coerce")  # Invalid -> NaT

# Convert to numeric
df["value"] = pd.to_numeric(df["value"], errors="coerce")  # Invalid -> NaN

# Convert to category (memory efficient for repeated strings)
df["status"] = df["status"].astype("category")

# Boolean conversion
df["active"] = df["active"].map({"yes": True, "no": False})
```

---

## Part 6: String Cleaning

```python
# Strip whitespace
df["name"] = df["name"].str.strip()
df["name"] = df["name"].str.lstrip()
df["name"] = df["name"].str.rstrip()

# Case conversion
df["name"] = df["name"].str.lower()
df["name"] = df["name"].str.upper()
df["name"] = df["name"].str.title()
df["name"] = df["name"].str.capitalize()

# Replace patterns
df["phone"] = df["phone"].str.replace("-", "")
df["phone"] = df["phone"].str.replace(r"\D", "", regex=True)  # Remove non-digits

# Extract patterns
df["area_code"] = df["phone"].str.extract(r"(\d{3})")

# Split strings
df[["first", "last"]] = df["name"].str.split(" ", n=1, expand=True)

# Contains
df["has_gmail"] = df["email"].str.contains("@gmail.com")

# Length
df["name_length"] = df["name"].str.len()
```

---

## Part 7: Standardizing Values

```python
# Map values
df["gender"] = df["gender"].map({
    "M": "Male", "m": "Male", "male": "Male",
    "F": "Female", "f": "Female", "female": "Female"
})

# Replace values
df["city"] = df["city"].replace({
    "NYC": "New York",
    "LA": "Los Angeles",
    "SF": "San Francisco"
})

# Standardize with function
def clean_city(city):
    if pd.isna(city):
        return "Unknown"
    city = city.strip().title()
    mapping = {"Nyc": "New York", "La": "Los Angeles"}
    return mapping.get(city, city)

df["city"] = df["city"].apply(clean_city)
```

---

## Part 8: Handling Outliers

```python
import numpy as np

# Identify outliers with IQR
Q1 = df["value"].quantile(0.25)
Q3 = df["value"].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df["value"] < lower_bound) | (df["value"] > upper_bound)]

# Remove outliers
df_clean = df[(df["value"] >= lower_bound) & (df["value"] <= upper_bound)]

# Cap outliers
df["value"] = df["value"].clip(lower=lower_bound, upper=upper_bound)

# Z-score method
from scipy import stats
z_scores = np.abs(stats.zscore(df["value"]))
df_clean = df[z_scores < 3]
```

---

## Part 9: Renaming and Reordering

```python
# Rename columns
df = df.rename(columns={"old_name": "new_name"})
df = df.rename(columns=str.lower)
df = df.rename(columns=lambda x: x.strip().replace(" ", "_"))

# Rename all columns
df.columns = ["col1", "col2", "col3"]

# Reorder columns
df = df[["name", "age", "city", "email"]]

# Move column to front
cols = df.columns.tolist()
cols = ["id"] + [c for c in cols if c != "id"]
df = df[cols]

# Sort columns alphabetically
df = df.reindex(sorted(df.columns), axis=1)
```

---

## Part 10: Complete Cleaning Pipeline

```python
import pandas as pd
import numpy as np

def clean_dataset(df):
    """Clean a messy dataset."""
    df = df.copy()

    # 1. Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # 2. Remove completely empty rows/columns
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")

    # 3. Remove duplicates
    df = df.drop_duplicates()

    # 4. Handle missing values
    # Numeric: fill with median
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    # Categorical: fill with mode or "Unknown"
    object_cols = df.select_dtypes(include=["object"]).columns
    for col in object_cols:
        df[col] = df[col].fillna("Unknown")

    # 5. Clean string columns
    for col in object_cols:
        df[col] = df[col].str.strip()

    # 6. Convert data types
    # (Add specific conversions as needed)

    # 7. Reset index
    df = df.reset_index(drop=True)

    return df

# Usage
df_clean = clean_dataset(df_messy)
```

---

## Week 20 Project: Clean a Messy Dataset

```python
import pandas as pd
import numpy as np

# Create messy sample data
data = {
    "Name": ["  John Smith  ", "Jane Doe", "JOHN SMITH", "Bob Wilson", None, "jane doe"],
    "Email": ["john@test.com", "jane@test.com", "john@test.com", "bob@test", "alice@test.com", "jane@test.com"],
    "Age": ["25", "30", "25", "abc", "28", "30"],
    "Salary": [50000, 60000, 50000, 70000, None, 60000],
    "City": ["NYC", "new york", "NYC", "LA", "la", "New York"],
    "Join Date": ["2020-01-15", "2020-02-20", "2020-01-15", "invalid", "2020-03-10", "2020-02-20"]
}
df = pd.DataFrame(data)

print("Original data:")
print(df)
print("\nData types:")
print(df.dtypes)
print("\nMissing values:")
print(df.isnull().sum())

# Clean the data
df_clean = df.copy()

# 1. Clean names
df_clean["Name"] = df_clean["Name"].str.strip().str.title()
df_clean["Name"] = df_clean["Name"].fillna("Unknown")

# 2. Clean emails (validate and lowercase)
df_clean["Email"] = df_clean["Email"].str.lower()
df_clean["Email"] = df_clean["Email"].apply(
    lambda x: x if "@" in str(x) and "." in str(x) else None
)

# 3. Convert age to numeric
df_clean["Age"] = pd.to_numeric(df_clean["Age"], errors="coerce")
df_clean["Age"] = df_clean["Age"].fillna(df_clean["Age"].median())
df_clean["Age"] = df_clean["Age"].astype(int)

# 4. Fill missing salary
df_clean["Salary"] = df_clean["Salary"].fillna(df_clean["Salary"].median())

# 5. Standardize city names
city_mapping = {
    "nyc": "New York",
    "new york": "New York",
    "la": "Los Angeles",
    "los angeles": "Los Angeles"
}
df_clean["City"] = df_clean["City"].str.lower().map(city_mapping)

# 6. Parse dates
df_clean["Join Date"] = pd.to_datetime(df_clean["Join Date"], errors="coerce")

# 7. Remove duplicates
df_clean = df_clean.drop_duplicates(subset=["Name", "Email"], keep="first")

print("\nCleaned data:")
print(df_clean)
print("\nData types:")
print(df_clean.dtypes)
print("\nMissing values:")
print(df_clean.isnull().sum())

# Save
df_clean.to_csv("cleaned_data.csv", index=False)
```

---

## Key Takeaways

1. Always **explore data** before cleaning
2. **Document** your cleaning decisions
3. Handle **missing values** appropriately (drop vs fill)
4. **Remove duplicates** based on business logic
5. **Standardize** strings (case, whitespace, formats)
6. **Validate** and convert data types
7. **Handle outliers** based on domain knowledge
8. Create **reusable cleaning functions**

---

## Next Week Preview
Week 21 covers data visualization with Matplotlib and Seaborn.
