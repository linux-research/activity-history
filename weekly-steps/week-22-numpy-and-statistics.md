# Week 22: NumPy and Statistics

## Overview
This week covers NumPy for numerical computing and descriptive statistics for data analysis.

---

## Part 1: NumPy Basics

### Installation

```bash
pip install numpy
```

### Creating Arrays

```python
import numpy as np

# From list
arr = np.array([1, 2, 3, 4, 5])

# 2D array
arr2d = np.array([[1, 2, 3], [4, 5, 6]])

# Special arrays
zeros = np.zeros((3, 4))        # 3x4 zeros
ones = np.ones((2, 3))          # 2x3 ones
full = np.full((2, 2), 7)       # 2x2 filled with 7
eye = np.eye(3)                  # 3x3 identity matrix
empty = np.empty((2, 3))        # Uninitialized

# Ranges
arr = np.arange(0, 10, 2)       # [0, 2, 4, 6, 8]
arr = np.linspace(0, 1, 5)      # [0, 0.25, 0.5, 0.75, 1]

# Random
arr = np.random.rand(3, 4)      # Uniform [0, 1)
arr = np.random.randn(3, 4)     # Standard normal
arr = np.random.randint(0, 10, (3, 4))  # Random integers
```

---

## Part 2: Array Properties and Reshaping

```python
import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6]])

# Properties
print(arr.shape)      # (2, 3)
print(arr.ndim)       # 2
print(arr.size)       # 6
print(arr.dtype)      # int64

# Reshaping
reshaped = arr.reshape(3, 2)
reshaped = arr.reshape(-1)      # Flatten
reshaped = arr.flatten()        # Flatten (copy)
reshaped = arr.ravel()          # Flatten (view)

# Transpose
transposed = arr.T
transposed = arr.transpose()

# Stacking
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

np.vstack([a, b])     # Vertical stack
np.hstack([a, b])     # Horizontal stack
np.concatenate([a, b])  # Concatenate

# Splitting
arr = np.arange(9)
np.split(arr, 3)      # Split into 3 parts
```

---

## Part 3: Indexing and Slicing

```python
import numpy as np

arr = np.array([[1, 2, 3, 4],
                [5, 6, 7, 8],
                [9, 10, 11, 12]])

# Basic indexing
arr[0, 0]         # 1
arr[1, 2]         # 7
arr[-1, -1]       # 12

# Slicing
arr[0, :]         # First row
arr[:, 0]         # First column
arr[0:2, 1:3]     # Subarray

# Boolean indexing
arr[arr > 5]      # Elements > 5

# Fancy indexing
arr[[0, 2], [1, 3]]  # Elements at (0,1) and (2,3)

# Assignment
arr[0, 0] = 100
arr[arr < 5] = 0
```

---

## Part 4: Array Operations

```python
import numpy as np

a = np.array([1, 2, 3, 4])
b = np.array([5, 6, 7, 8])

# Element-wise operations
a + b         # Addition
a - b         # Subtraction
a * b         # Multiplication
a / b         # Division
a ** 2        # Power
np.sqrt(a)    # Square root

# Scalar operations
a + 10
a * 2

# Comparison
a > 2         # [False, False, True, True]
a == b        # Element-wise comparison

# Aggregate functions
np.sum(a)
np.mean(a)
np.std(a)
np.var(a)
np.min(a)
np.max(a)
np.argmin(a)  # Index of min
np.argmax(a)  # Index of max

# Along axis
arr = np.array([[1, 2], [3, 4]])
np.sum(arr, axis=0)   # Sum columns
np.sum(arr, axis=1)   # Sum rows
```

---

## Part 5: Broadcasting

```python
import numpy as np

# Broadcasting allows operations on arrays of different shapes
a = np.array([[1, 2, 3],
              [4, 5, 6]])

b = np.array([10, 20, 30])

# b is broadcast to match a's shape
result = a + b
# [[11, 22, 33],
#  [14, 25, 36]]

# Scalar broadcasting
a * 2
# [[2, 4, 6],
#  [8, 10, 12]]
```

---

## Part 6: Linear Algebra

```python
import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# Matrix multiplication
np.dot(A, B)
A @ B

# Transpose
A.T

# Determinant
np.linalg.det(A)

# Inverse
np.linalg.inv(A)

# Eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(A)

# Solve linear system Ax = b
b = np.array([1, 2])
x = np.linalg.solve(A, b)
```

---

## Part 7: Descriptive Statistics

```python
import numpy as np
import pandas as pd

data = np.array([23, 45, 67, 34, 56, 78, 89, 12, 34, 56])

# Central tendency
mean = np.mean(data)
median = np.median(data)
# Mode (use scipy or pandas)
from scipy import stats
mode = stats.mode(data)

# Spread
std = np.std(data)
var = np.var(data)
range_val = np.max(data) - np.min(data)

# Quartiles
q1 = np.percentile(data, 25)
q2 = np.percentile(data, 50)  # Median
q3 = np.percentile(data, 75)
iqr = q3 - q1

# Five number summary
print(f"Min: {np.min(data)}")
print(f"Q1: {q1}")
print(f"Median: {q2}")
print(f"Q3: {q3}")
print(f"Max: {np.max(data)}")
```

---

## Part 8: Statistical Analysis with Pandas

```python
import pandas as pd
import numpy as np

# Sample data
np.random.seed(42)
df = pd.DataFrame({
    "group": np.random.choice(["A", "B", "C"], 100),
    "value": np.random.normal(50, 10, 100),
    "score": np.random.randint(0, 100, 100)
})

# Descriptive statistics
print(df.describe())

# By group
print(df.groupby("group").agg({
    "value": ["mean", "std", "min", "max"],
    "score": ["mean", "median"]
}))

# Correlation
print(df[["value", "score"]].corr())

# Covariance
print(df[["value", "score"]].cov())
```

---

## Part 9: Probability Distributions

```python
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Normal distribution
mu, sigma = 100, 15
x = np.linspace(50, 150, 100)
pdf = stats.norm.pdf(x, mu, sigma)
cdf = stats.norm.cdf(x, mu, sigma)

plt.figure(figsize=(12, 4))
plt.subplot(1, 2, 1)
plt.plot(x, pdf)
plt.title("Normal PDF")

plt.subplot(1, 2, 2)
plt.plot(x, cdf)
plt.title("Normal CDF")
plt.show()

# Generate random samples
samples = np.random.normal(mu, sigma, 1000)

# Other distributions
uniform = np.random.uniform(0, 1, 1000)
exponential = np.random.exponential(1, 1000)
poisson = np.random.poisson(5, 1000)
binomial = np.random.binomial(10, 0.5, 1000)
```

---

## Part 10: Statistical Tests

```python
from scipy import stats
import numpy as np

# T-test (compare means)
group1 = np.random.normal(50, 10, 30)
group2 = np.random.normal(55, 10, 30)

t_stat, p_value = stats.ttest_ind(group1, group2)
print(f"T-statistic: {t_stat:.4f}, P-value: {p_value:.4f}")

if p_value < 0.05:
    print("Significant difference between groups")
else:
    print("No significant difference")

# Chi-square test (categorical data)
observed = np.array([30, 40, 30])
expected = np.array([33.3, 33.3, 33.3])
chi2, p_value = stats.chisquare(observed, expected)

# Correlation test
r, p_value = stats.pearsonr(group1, group2)
print(f"Correlation: {r:.4f}, P-value: {p_value:.4f}")
```

---

## Week 22 Project: Statistical Analysis Report

```python
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Generate sample dataset
np.random.seed(42)
n = 200

df = pd.DataFrame({
    "age": np.random.randint(18, 65, n),
    "income": np.random.normal(50000, 15000, n).clip(min=20000),
    "education_years": np.random.randint(8, 22, n),
    "satisfaction": np.random.randint(1, 11, n),
    "region": np.random.choice(["North", "South", "East", "West"], n)
})

print("=" * 60)
print("STATISTICAL ANALYSIS REPORT")
print("=" * 60)

# 1. Basic Statistics
print("\n1. DESCRIPTIVE STATISTICS")
print("-" * 40)
print(df.describe())

# 2. Distribution Analysis
print("\n2. DISTRIBUTION ANALYSIS")
print("-" * 40)
for col in ["age", "income", "satisfaction"]:
    skewness = stats.skew(df[col])
    kurtosis = stats.kurtosis(df[col])
    print(f"{col}:")
    print(f"  Skewness: {skewness:.3f}")
    print(f"  Kurtosis: {kurtosis:.3f}")

# 3. Correlation Analysis
print("\n3. CORRELATION MATRIX")
print("-" * 40)
numeric_cols = ["age", "income", "education_years", "satisfaction"]
corr_matrix = df[numeric_cols].corr()
print(corr_matrix.round(3))

# 4. Group Comparison
print("\n4. REGIONAL COMPARISON")
print("-" * 40)
regional_stats = df.groupby("region").agg({
    "income": ["mean", "std"],
    "satisfaction": ["mean", "std"]
}).round(2)
print(regional_stats)

# ANOVA test for income across regions
regions = [group["income"].values for name, group in df.groupby("region")]
f_stat, p_value = stats.f_oneway(*regions)
print(f"\nANOVA Test (Income ~ Region):")
print(f"  F-statistic: {f_stat:.3f}")
print(f"  P-value: {p_value:.4f}")

# 5. Visualizations
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Income distribution
axes[0, 0].hist(df["income"], bins=20, edgecolor="black", alpha=0.7)
axes[0, 0].axvline(df["income"].mean(), color="red", linestyle="--", label="Mean")
axes[0, 0].axvline(df["income"].median(), color="green", linestyle="--", label="Median")
axes[0, 0].legend()
axes[0, 0].set_title("Income Distribution")
axes[0, 0].set_xlabel("Income ($)")

# Box plot by region
df.boxplot(column="income", by="region", ax=axes[0, 1])
axes[0, 1].set_title("Income by Region")

# Correlation heatmap
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=axes[1, 0], center=0)
axes[1, 0].set_title("Correlation Matrix")

# Scatter plot
axes[1, 1].scatter(df["education_years"], df["income"], alpha=0.5)
axes[1, 1].set_xlabel("Education Years")
axes[1, 1].set_ylabel("Income ($)")
axes[1, 1].set_title("Education vs Income")

# Add regression line
z = np.polyfit(df["education_years"], df["income"], 1)
p = np.poly1d(z)
axes[1, 1].plot(df["education_years"].sort_values(),
                p(df["education_years"].sort_values()),
                "r--", alpha=0.8)

plt.tight_layout()
plt.savefig("statistical_report.png", dpi=300)
plt.show()

print("\n" + "=" * 60)
print("Analysis complete. Report saved to statistical_report.png")
```

---

## Key Takeaways

1. **NumPy arrays** are faster than Python lists
2. **Vectorized operations** avoid explicit loops
3. **Broadcasting** enables flexible array operations
4. **Descriptive statistics** summarize data (mean, median, std)
5. **Correlation** measures relationships between variables
6. **Statistical tests** help validate hypotheses
7. Use **scipy.stats** for distributions and tests
8. **Visualize** distributions before statistical analysis

---

## Next Week Preview
Weeks 23-24: Complete a data analysis project.
