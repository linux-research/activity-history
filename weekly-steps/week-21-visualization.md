# Week 21: Data Visualization

## Overview
This week covers data visualization with Matplotlib and Seaborn: creating charts, customizing plots, and telling stories with data.

---

## Part 1: Matplotlib Basics

### Installation

```bash
pip install matplotlib seaborn
```

### Basic Setup

```python
import matplotlib.pyplot as plt
import numpy as np

# Simple plot
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

plt.plot(x, y)
plt.show()

# With labels
plt.plot(x, y)
plt.xlabel("X Axis")
plt.ylabel("Y Axis")
plt.title("My First Plot")
plt.show()

# Save to file
plt.plot(x, y)
plt.savefig("plot.png", dpi=300, bbox_inches="tight")
```

---

## Part 2: Line Charts

```python
import matplotlib.pyplot as plt
import numpy as np

# Multiple lines
x = np.linspace(0, 10, 100)
plt.plot(x, np.sin(x), label="sin(x)")
plt.plot(x, np.cos(x), label="cos(x)")
plt.legend()
plt.title("Trigonometric Functions")
plt.show()

# Customizing lines
plt.plot(x, np.sin(x),
         color="blue",      # Color
         linestyle="--",    # Line style: -, --, -., :
         linewidth=2,       # Line width
         marker="o",        # Markers
         markersize=5,
         label="sin(x)")

# Style shortcuts
plt.plot(x, y, "r--")   # Red dashed
plt.plot(x, y, "bo")    # Blue circles
plt.plot(x, y, "g^-")   # Green triangles with line
```

---

## Part 3: Bar Charts

```python
import matplotlib.pyplot as plt

# Vertical bars
categories = ["A", "B", "C", "D"]
values = [25, 40, 30, 55]

plt.bar(categories, values, color="steelblue")
plt.xlabel("Category")
plt.ylabel("Value")
plt.title("Bar Chart")
plt.show()

# Horizontal bars
plt.barh(categories, values, color="coral")
plt.show()

# Grouped bars
x = np.arange(4)
width = 0.35
values1 = [25, 40, 30, 55]
values2 = [30, 35, 45, 40]

plt.bar(x - width/2, values1, width, label="2023")
plt.bar(x + width/2, values2, width, label="2024")
plt.xticks(x, categories)
plt.legend()
plt.show()

# Stacked bars
plt.bar(categories, values1, label="2023")
plt.bar(categories, values2, bottom=values1, label="2024")
plt.legend()
plt.show()
```

---

## Part 4: Scatter Plots

```python
import matplotlib.pyplot as plt
import numpy as np

# Basic scatter
x = np.random.rand(50)
y = np.random.rand(50)
plt.scatter(x, y)
plt.show()

# Customized
colors = np.random.rand(50)
sizes = np.random.rand(50) * 500

plt.scatter(x, y,
           c=colors,          # Color by value
           s=sizes,           # Size by value
           alpha=0.5,         # Transparency
           cmap="viridis")    # Colormap
plt.colorbar(label="Color Scale")
plt.show()
```

---

## Part 5: Histograms

```python
import matplotlib.pyplot as plt
import numpy as np

# Basic histogram
data = np.random.normal(100, 15, 1000)
plt.hist(data, bins=30, color="steelblue", edgecolor="black")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.title("Distribution")
plt.show()

# Multiple histograms
data1 = np.random.normal(100, 15, 1000)
data2 = np.random.normal(120, 10, 1000)

plt.hist(data1, bins=30, alpha=0.5, label="Group 1")
plt.hist(data2, bins=30, alpha=0.5, label="Group 2")
plt.legend()
plt.show()

# Density plot (KDE)
plt.hist(data, bins=30, density=True, alpha=0.7)
plt.show()
```

---

## Part 6: Pie Charts

```python
import matplotlib.pyplot as plt

# Basic pie
labels = ["A", "B", "C", "D"]
sizes = [35, 25, 25, 15]

plt.pie(sizes, labels=labels, autopct="%1.1f%%")
plt.title("Pie Chart")
plt.show()

# Customized
colors = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"]
explode = (0.1, 0, 0, 0)  # Explode first slice

plt.pie(sizes,
       labels=labels,
       colors=colors,
       explode=explode,
       autopct="%1.1f%%",
       shadow=True,
       startangle=90)
plt.axis("equal")  # Equal aspect ratio
plt.show()
```

---

## Part 7: Subplots

```python
import matplotlib.pyplot as plt
import numpy as np

# Create 2x2 grid
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# Access each subplot
x = np.linspace(0, 10, 100)

axes[0, 0].plot(x, np.sin(x))
axes[0, 0].set_title("Sin(x)")

axes[0, 1].plot(x, np.cos(x))
axes[0, 1].set_title("Cos(x)")

axes[1, 0].bar(["A", "B", "C"], [10, 20, 15])
axes[1, 0].set_title("Bar Chart")

axes[1, 1].scatter(np.random.rand(20), np.random.rand(20))
axes[1, 1].set_title("Scatter")

plt.tight_layout()
plt.show()

# Different subplot sizes
fig = plt.figure(figsize=(12, 5))
ax1 = fig.add_subplot(1, 2, 1)  # 1 row, 2 cols, position 1
ax2 = fig.add_subplot(1, 2, 2)  # 1 row, 2 cols, position 2
```

---

## Part 8: Seaborn

Seaborn provides high-level plotting functions with better defaults.

```python
import seaborn as sns
import pandas as pd

# Set style
sns.set_style("whitegrid")  # white, dark, whitegrid, darkgrid, ticks
sns.set_palette("husl")

# Sample data
df = pd.DataFrame({
    "category": np.random.choice(["A", "B", "C"], 100),
    "value": np.random.randn(100),
    "size": np.random.randint(10, 50, 100)
})

# Distribution plots
sns.histplot(data=df, x="value", kde=True)
sns.kdeplot(data=df, x="value")
sns.boxplot(data=df, x="category", y="value")
sns.violinplot(data=df, x="category", y="value")

# Categorical plots
sns.barplot(data=df, x="category", y="value")
sns.countplot(data=df, x="category")
sns.stripplot(data=df, x="category", y="value")

# Relationship plots
sns.scatterplot(data=df, x="value", y="size", hue="category")
sns.lineplot(data=df, x="value", y="size", hue="category")

# Heatmaps
correlation = df.corr()
sns.heatmap(correlation, annot=True, cmap="coolwarm")

plt.show()
```

---

## Part 9: Plotting with Pandas

```python
import pandas as pd

# Pandas has built-in plotting
df = pd.DataFrame({
    "A": np.random.randn(100).cumsum(),
    "B": np.random.randn(100).cumsum(),
    "C": np.random.randn(100).cumsum()
})

# Line plot
df.plot()

# Other plot types
df.plot(kind="line")
df.plot(kind="bar")
df.plot(kind="barh")
df.plot(kind="hist")
df.plot(kind="box")
df.plot(kind="scatter", x="A", y="B")
df.plot(kind="pie", y="A")

# Customization
df.plot(
    kind="line",
    figsize=(10, 6),
    title="My Plot",
    xlabel="X",
    ylabel="Y",
    legend=True,
    grid=True
)
plt.show()
```

---

## Part 10: Complete Visualization Example

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Create sample sales data
np.random.seed(42)
dates = pd.date_range("2024-01-01", periods=365, freq="D")
df = pd.DataFrame({
    "date": dates,
    "sales": np.random.randint(100, 1000, 365) + np.sin(np.arange(365) * 0.1) * 200,
    "region": np.random.choice(["North", "South", "East", "West"], 365),
    "product": np.random.choice(["A", "B", "C"], 365)
})

# Create dashboard
fig = plt.figure(figsize=(15, 10))
fig.suptitle("Sales Dashboard 2024", fontsize=16, fontweight="bold")

# 1. Sales over time (line chart)
ax1 = fig.add_subplot(2, 3, 1)
daily_sales = df.groupby("date")["sales"].sum()
ax1.plot(daily_sales.index, daily_sales.values, color="steelblue", alpha=0.7)
ax1.set_title("Daily Sales Trend")
ax1.set_xlabel("Date")
ax1.set_ylabel("Sales ($)")

# 2. Sales by region (bar chart)
ax2 = fig.add_subplot(2, 3, 2)
region_sales = df.groupby("region")["sales"].sum().sort_values(ascending=True)
region_sales.plot(kind="barh", ax=ax2, color="coral")
ax2.set_title("Sales by Region")
ax2.set_xlabel("Total Sales ($)")

# 3. Product distribution (pie chart)
ax3 = fig.add_subplot(2, 3, 3)
product_sales = df.groupby("product")["sales"].sum()
ax3.pie(product_sales, labels=product_sales.index, autopct="%1.1f%%",
        colors=["#ff9999", "#66b3ff", "#99ff99"])
ax3.set_title("Sales by Product")

# 4. Sales distribution (histogram)
ax4 = fig.add_subplot(2, 3, 4)
ax4.hist(df["sales"], bins=30, color="steelblue", edgecolor="black", alpha=0.7)
ax4.axvline(df["sales"].mean(), color="red", linestyle="--", label=f"Mean: {df['sales'].mean():.0f}")
ax4.legend()
ax4.set_title("Sales Distribution")
ax4.set_xlabel("Sales ($)")
ax4.set_ylabel("Frequency")

# 5. Monthly comparison (grouped bar)
ax5 = fig.add_subplot(2, 3, 5)
df["month"] = df["date"].dt.month
monthly_region = df.pivot_table(values="sales", index="month", columns="region", aggfunc="sum")
monthly_region.plot(kind="bar", ax=ax5)
ax5.set_title("Monthly Sales by Region")
ax5.set_xlabel("Month")
ax5.set_ylabel("Sales ($)")
ax5.legend(title="Region")

# 6. Sales heatmap by region and product
ax6 = fig.add_subplot(2, 3, 6)
heatmap_data = df.pivot_table(values="sales", index="region", columns="product", aggfunc="sum")
sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlOrRd", ax=ax6)
ax6.set_title("Sales Heatmap")

plt.tight_layout()
plt.savefig("sales_dashboard.png", dpi=300, bbox_inches="tight")
plt.show()
```

---

## Key Takeaways

1. **Matplotlib** is the foundation for Python visualization
2. **Seaborn** provides higher-level, prettier plots
3. **Pandas** has built-in plotting capabilities
4. Choose the right chart type for your data
5. **Always label** axes and add titles
6. Use **subplots** for dashboards
7. **Save figures** with appropriate resolution
8. **Color** wisely - consider colorblind-friendly palettes

---

## Next Week Preview
Week 22 covers NumPy basics and descriptive statistics.
