#!/usr/bin/env python
# coding: utf-8
# walmart_sales\scripts\analysis.py
"""
Walmart Sales Analysis Script
- Answers business questions:
  1. How do holidays impact weekly sales?
  2. Does air temperature affect consumer spending?
  3. Which stores perform best over time?
  4. Are there seasonal trends or patterns in sales?
  5. Do fuel prices, CPI, and unemployment influence revenue?
"""

import sys
import platform
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import statsmodels.api as sm

pd.options.display.float_format = "{:,.0f}".format


def print_env_info():
    """Print environment and library versions."""
    print("=" * 50)
    print("📦 Environment & Library Versions")
    print("=" * 50)
    print(f"Python version:     {sys.version.split()[0]}")
    print(f"Platform:           {platform.platform()}")
    print(f"pandas:             {pd.__version__}")
    print(f"numpy:              {np.__version__}")
    print(f"matplotlib:         {plt.matplotlib.__version__}")
    print(f"seaborn:            {sns.__version__}")
    print(f"statsmodels:        {sm.__version__}")
    print("=" * 50)


def load_clean_data(path: str = ".\\data\\walmart_sales_data.csv") -> pd.DataFrame:
    """Load the cleaned Walmart dataset."""
    df = pd.read_csv(path)
    df["Store"] = df["Store"].astype("category")
    df["Holiday_Flag"] = df["Holiday_Flag"].astype("category")
    df["Temp_Bin"] = pd.Categorical(
        df["Temp_Bin"], categories=["Cold", "Mild", "Warm", "Hot"], ordered=True
    )
    return df


def analyze_holiday_impact(df: pd.DataFrame):
    """Compare sales during holiday vs non-holiday weeks."""
    holiday_impact = (
        df.groupby("Holiday")["Weekly_Sales"]
        .agg(["mean", "median", "std", "sum", "count"])
        .rename(
            columns={
                "mean": "Avg_Sales",
                "median": "Median_Sales",
                "std": "Std_Dev",
                "sum": "Total_Sales",
                "count": "Num_Weeks",
            }
        )
    )
    print("\nHoliday Impact Summary:")
    print(holiday_impact)

    holiday_diff = (
        holiday_impact.loc["Holiday", "Avg_Sales"]
        / holiday_impact.loc["No Holiday", "Avg_Sales"]
        - 1
    ) * 100
    print(
        f"\nHoliday weeks have {holiday_diff:.2f}% higher average sales than non-holiday weeks."
    )


def analyze_temperature_effect(df: pd.DataFrame):
    """Analyze effect of temperature on sales."""
    temp_sales = (
        df.groupby("Temp_Bin")["Weekly_Sales"]
        .mean()
        .reindex(["Cold", "Mild", "Warm", "Hot"])
    )
    print("\nAverage Sales by Temperature Category:")
    print(temp_sales)

    plt.figure(figsize=(8, 5))
    bars = plt.bar(temp_sales.index, temp_sales.values, color="skyblue")
    plt.title("Average Weekly Sales by Temperature Category")
    plt.xlabel("Temperature Category")
    plt.ylabel("Average Weekly Sales ($)")
    for bar in bars:
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{bar.get_height():,.0f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )
    plt.tight_layout()
    plt.show()

    corr = df[["Weekly_Sales", "Temperature"]].corr().iloc[0, 1]
    print(f"Correlation between Temperature and Weekly Sales: {corr:.3f}")


def analyze_store_performance(df: pd.DataFrame):
    """Aggregate total and average sales by store and plot top stores."""
    store_perf = (
        df.groupby("Store")
        .agg(
            Total_Sales=("Weekly_Sales", "sum"),
            Average_Weekly_Sales=("Weekly_Sales", "mean"),
            Std_Weekly_Sales=("Weekly_Sales", "std"),
        )
        .sort_values("Total_Sales", ascending=False)
    )

    # Top 5 by total sales
    top5_sales = store_perf.head(5)
    plt.figure(figsize=(8, 5))
    bars = plt.bar(
        top5_sales.index.astype(str),
        top5_sales["Total_Sales"],
        color="skyblue",
        edgecolor="black",
    )
    for bar in bars:
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 5e6,
            f"${bar.get_height():,.0f}",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
        )
    plt.title("Top 5 Stores by Total Sales", fontsize=14, fontweight="bold")
    plt.xlabel("Store")
    plt.ylabel("Total Sales (USD)")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()


def analyze_seasonal_trends(df: pd.DataFrame):
    """Identify seasonal trends in sales across months and seasons."""
    # Monthly trends
    seasonal_trends = df.groupby(["Year", "Month"])["Weekly_Sales"].mean().reset_index()
    seasonal_trends["Month_Name"] = seasonal_trends["Month"].apply(
        lambda x: pd.to_datetime(str(x), format="%m").strftime("%b")
    )

    plt.figure(figsize=(12, 6))
    for year in seasonal_trends["Year"].unique():
        data = seasonal_trends[seasonal_trends["Year"] == year]
        plt.plot(data["Month"], data["Weekly_Sales"], marker="o", label=str(year))
    plt.xticks(
        ticks=range(1, 13),
        labels=[
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
    )
    plt.title(
        "Average Weekly Sales Trend by Month and Year", fontsize=14, fontweight="bold"
    )
    plt.xlabel("Month")
    plt.ylabel("Average Weekly Sales (USD)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(title="Year")
    plt.tight_layout()
    plt.show()

    # Seasonal averages
    seasonal_sales = (
        df.groupby("Season")["Weekly_Sales"]
        .mean()
        .reindex(["Winter", "Spring", "Summer", "Fall"])
    )
    plt.figure(figsize=(8, 5))
    ax = sns.barplot(
        x=seasonal_sales.index, y=seasonal_sales.values, palette="coolwarm"
    )
    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", padding=3, fontsize=10, fontweight="bold")
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: f"{x/1_000_000:.1f}M")
    )
    plt.title("Average Weekly Sales by Season", fontsize=14, fontweight="bold")
    plt.xlabel("Season")
    plt.ylabel("Average Weekly Sales (in Millions)")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()


def analyze_economic_indicators(df: pd.DataFrame):
    """Examine effect of Fuel Price, CPI, and Unemployment on sales."""
    # Correlation matrix
    corr = df[
        ["Weekly_Sales", "Fuel_Price", "CPI", "Unemployment", "Temperature"]
    ].corr()
    print("\nCorrelation Matrix:")
    print(corr)

    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm")
    plt.title("Correlation between Weekly Sales and Economic Indicators")
    plt.show()

    # Regression model
    df = df.dropna(subset=["Fuel_Price", "CPI", "Unemployment"])
    X = sm.add_constant(df[["Fuel_Price", "CPI", "Unemployment"]].astype(float))
    y = np.log1p(df["Weekly_Sales"].astype(float))
    model = sm.OLS(y, X).fit(cov_type="HC3")
    print(model.summary())


def main():
    print_env_info()
    df = load_clean_data()
    analyze_holiday_impact(df)
    analyze_temperature_effect(df)
    analyze_store_performance(df)
    analyze_seasonal_trends(df)
    analyze_economic_indicators(df)


if __name__ == "__main__":
    main()
