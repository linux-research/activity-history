# Weeks 23-24: Data Analysis Project

## Overview
Over these two weeks, you'll complete an end-to-end data analysis project: loading data, cleaning, exploring, analyzing, visualizing, and drawing insights.

---

## Project: Analyzing a Real Dataset

Choose a dataset from:
- [Kaggle Datasets](https://kaggle.com/datasets)
- [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml)
- [Data.gov](https://data.gov)

---

## Week 23: Data Loading, Cleaning, and Exploration

### Step 1: Load and Inspect Data

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("your_dataset.csv")

# Initial inspection
print("=" * 60)
print("DATA INSPECTION")
print("=" * 60)

print(f"\nShape: {df.shape}")
print(f"\nColumn names:\n{df.columns.tolist()}")
print(f"\nData types:\n{df.dtypes}")
print(f"\nFirst 5 rows:\n{df.head()}")
print(f"\nBasic statistics:\n{df.describe()}")
print(f"\nMissing values:\n{df.isnull().sum()}")
```

### Step 2: Clean Data

```python
def clean_data(df):
    """Clean the dataset."""
    df = df.copy()

    # 1. Remove duplicates
    initial_rows = len(df)
    df = df.drop_duplicates()
    print(f"Removed {initial_rows - len(df)} duplicates")

    # 2. Handle missing values
    # Numeric columns: fill with median
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna(df[col].median())
            print(f"Filled missing values in {col} with median")

    # Categorical columns: fill with mode or 'Unknown'
    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna('Unknown')
            print(f"Filled missing values in {col} with 'Unknown'")

    # 3. Fix data types
    # Convert date columns
    date_cols = [col for col in df.columns if 'date' in col.lower()]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    # 4. Standardize strings
    for col in cat_cols:
        df[col] = df[col].str.strip().str.title()

    # 5. Handle outliers (optional)
    # Using IQR method for numeric columns
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        df[col] = df[col].clip(lower=Q1 - 1.5*IQR, upper=Q3 + 1.5*IQR)

    return df

df_clean = clean_data(df)
print(f"\nCleaned data shape: {df_clean.shape}")
```

### Step 3: Exploratory Data Analysis

```python
def explore_data(df):
    """Perform exploratory data analysis."""
    print("=" * 60)
    print("EXPLORATORY DATA ANALYSIS")
    print("=" * 60)

    # Numeric columns analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    print(f"\nNumeric columns: {list(numeric_cols)}")

    for col in numeric_cols:
        print(f"\n{col}:")
        print(f"  Mean: {df[col].mean():.2f}")
        print(f"  Median: {df[col].median():.2f}")
        print(f"  Std: {df[col].std():.2f}")
        print(f"  Min: {df[col].min():.2f}")
        print(f"  Max: {df[col].max():.2f}")

    # Categorical columns analysis
    cat_cols = df.select_dtypes(include=['object']).columns
    print(f"\nCategorical columns: {list(cat_cols)}")

    for col in cat_cols:
        print(f"\n{col}:")
        print(f"  Unique values: {df[col].nunique()}")
        print(f"  Top 5 values:\n{df[col].value_counts().head()}")

    # Correlations
    print("\nCorrelation Matrix:")
    print(df[numeric_cols].corr().round(3))

explore_data(df_clean)
```

### Step 4: Create Visualizations

```python
def visualize_data(df):
    """Create visualizations for the dataset."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    cat_cols = df.select_dtypes(include=['object']).columns

    # Set style
    plt.style.use('seaborn-v0_8-whitegrid')

    # 1. Distribution plots for numeric columns
    n_numeric = len(numeric_cols)
    fig, axes = plt.subplots(2, (n_numeric + 1) // 2, figsize=(15, 8))
    axes = axes.flatten()

    for i, col in enumerate(numeric_cols):
        axes[i].hist(df[col], bins=30, edgecolor='black', alpha=0.7)
        axes[i].set_title(f'Distribution of {col}')
        axes[i].set_xlabel(col)

    plt.tight_layout()
    plt.savefig('distributions.png', dpi=300)
    plt.show()

    # 2. Box plots
    fig, axes = plt.subplots(1, len(numeric_cols), figsize=(15, 5))
    for i, col in enumerate(numeric_cols):
        axes[i].boxplot(df[col].dropna())
        axes[i].set_title(col)

    plt.tight_layout()
    plt.savefig('boxplots.png', dpi=300)
    plt.show()

    # 3. Correlation heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Heatmap')
    plt.savefig('correlation_heatmap.png', dpi=300)
    plt.show()

    # 4. Bar charts for categorical columns
    for col in cat_cols[:3]:  # Limit to first 3
        plt.figure(figsize=(10, 5))
        df[col].value_counts().head(10).plot(kind='barh')
        plt.title(f'Top 10 {col}')
        plt.xlabel('Count')
        plt.tight_layout()
        plt.savefig(f'{col}_distribution.png', dpi=300)
        plt.show()

visualize_data(df_clean)
```

---

## Week 24: Analysis, Insights, and Report

### Step 5: Deep Analysis

```python
def analyze_data(df):
    """Perform deeper analysis on the dataset."""
    results = {}

    # Group analysis (adjust based on your data)
    # Example: If you have a 'category' column
    if 'category' in df.columns:
        category_analysis = df.groupby('category').agg({
            'value': ['mean', 'sum', 'count']
        }).round(2)
        results['category_analysis'] = category_analysis

    # Time series analysis (if you have date column)
    date_cols = df.select_dtypes(include=['datetime64']).columns
    if len(date_cols) > 0:
        date_col = date_cols[0]
        df['month'] = df[date_col].dt.to_period('M')
        monthly = df.groupby('month').agg({
            col: 'sum' for col in df.select_dtypes(include=[np.number]).columns[:3]
        })
        results['monthly_trends'] = monthly

    # Top/Bottom analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols[:2]:
        results[f'top_5_{col}'] = df.nlargest(5, col)
        results[f'bottom_5_{col}'] = df.nsmallest(5, col)

    return results

analysis_results = analyze_data(df_clean)
for key, value in analysis_results.items():
    print(f"\n{key}:")
    print(value)
```

### Step 6: Statistical Tests

```python
from scipy import stats

def statistical_tests(df):
    """Perform statistical tests."""
    print("=" * 60)
    print("STATISTICAL TESTS")
    print("=" * 60)

    numeric_cols = df.select_dtypes(include=[np.number]).columns

    # Normality tests
    print("\n1. Normality Tests (Shapiro-Wilk):")
    for col in numeric_cols[:3]:
        stat, p_value = stats.shapiro(df[col].sample(min(5000, len(df))))
        normal = "Normal" if p_value > 0.05 else "Not Normal"
        print(f"  {col}: p-value = {p_value:.4f} ({normal})")

    # Correlation significance
    print("\n2. Correlation Tests:")
    if len(numeric_cols) >= 2:
        col1, col2 = numeric_cols[:2]
        r, p_value = stats.pearsonr(df[col1], df[col2])
        sig = "Significant" if p_value < 0.05 else "Not Significant"
        print(f"  {col1} vs {col2}:")
        print(f"    Correlation: {r:.4f}")
        print(f"    P-value: {p_value:.4f} ({sig})")

statistical_tests(df_clean)
```

### Step 7: Generate Report

```python
def generate_report(df, filename='analysis_report.md'):
    """Generate a markdown report."""
    with open(filename, 'w') as f:
        f.write("# Data Analysis Report\n\n")

        f.write("## 1. Dataset Overview\n\n")
        f.write(f"- **Rows**: {len(df)}\n")
        f.write(f"- **Columns**: {len(df.columns)}\n")
        f.write(f"- **Columns**: {', '.join(df.columns)}\n\n")

        f.write("## 2. Data Quality\n\n")
        f.write(f"- **Missing Values**: {df.isnull().sum().sum()}\n")
        f.write(f"- **Duplicates**: {df.duplicated().sum()}\n\n")

        f.write("## 3. Summary Statistics\n\n")
        f.write("```\n")
        f.write(df.describe().to_string())
        f.write("\n```\n\n")

        f.write("## 4. Key Findings\n\n")
        f.write("1. Finding 1: [Describe your insight]\n")
        f.write("2. Finding 2: [Describe your insight]\n")
        f.write("3. Finding 3: [Describe your insight]\n\n")

        f.write("## 5. Visualizations\n\n")
        f.write("![Distributions](distributions.png)\n\n")
        f.write("![Correlation Heatmap](correlation_heatmap.png)\n\n")

        f.write("## 6. Recommendations\n\n")
        f.write("Based on the analysis:\n")
        f.write("1. Recommendation 1\n")
        f.write("2. Recommendation 2\n")
        f.write("3. Recommendation 3\n")

    print(f"Report saved to {filename}")

generate_report(df_clean)
```

### Step 8: Complete Analysis Script

```python
# complete_analysis.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def main():
    """Main analysis pipeline."""

    # 1. Load data
    print("Loading data...")
    df = pd.read_csv("your_dataset.csv")

    # 2. Initial exploration
    print("\n" + "=" * 60)
    print("INITIAL EXPLORATION")
    print(f"Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")

    # 3. Clean data
    print("\n" + "=" * 60)
    print("CLEANING DATA")
    df_clean = clean_data(df)

    # 4. Explore
    print("\n" + "=" * 60)
    print("EXPLORING DATA")
    explore_data(df_clean)

    # 5. Visualize
    print("\n" + "=" * 60)
    print("CREATING VISUALIZATIONS")
    visualize_data(df_clean)

    # 6. Analyze
    print("\n" + "=" * 60)
    print("PERFORMING ANALYSIS")
    results = analyze_data(df_clean)

    # 7. Statistical tests
    print("\n" + "=" * 60)
    print("STATISTICAL TESTS")
    statistical_tests(df_clean)

    # 8. Save results
    print("\n" + "=" * 60)
    print("SAVING RESULTS")
    df_clean.to_csv("cleaned_data.csv", index=False)
    generate_report(df_clean)

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    main()
```

---

## Deliverables Checklist

- [ ] Cleaned dataset (CSV)
- [ ] Distribution plots (PNG)
- [ ] Correlation heatmap (PNG)
- [ ] Category/group visualizations (PNG)
- [ ] Analysis report (Markdown)
- [ ] Python script (reproducible analysis)
- [ ] Key insights and recommendations

---

## Key Takeaways

1. **Data cleaning** is often 80% of the work
2. Always **explore before analyzing**
3. **Visualizations** reveal patterns
4. Use **statistical tests** to validate findings
5. **Document everything** for reproducibility
6. **Tell a story** with your data
7. **Actionable insights** are the goal
8. **Version control** your analysis code

---

## Next Week Preview
Week 25 begins the Automation Track with file system automation.
