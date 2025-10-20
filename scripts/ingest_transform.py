#!/usr/bin/env python
# coding: utf-8
# walmart_sales\scripts\ingest_transform.py
"""
Walmart Sales Data Ingest & Transform Script
- Load raw Walmart sales data
- Transform dates, holidays, seasons, and rolling sales
- Detect outliers and summarize data quality
- Save clean dataset to CSV
"""

import os
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import kagglehub
from kagglehub import KaggleDatasetAdapter


def load_data(file_path: str = "Walmart_Sales.csv") -> pd.DataFrame:
    """Load Walmart dataset from Kaggle."""
    df = kagglehub.dataset_load(
        KaggleDatasetAdapter.PANDAS,
        "mikhail1681/walmart-sales",
        file_path,
    )
    return df


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """Perform all data transformations and feature engineering."""
    df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", errors="coerce")
    df = df.dropna(subset=["Date"]).copy()
    df = df.sort_values(["Store", "Date"]).reset_index(drop=True)

    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Week"] = df["Date"].dt.isocalendar().week.astype("UInt32")
    df["DayOfWeek"] = df["Date"].dt.dayofweek.astype("int8")

    df["Store"] = df["Store"].astype("category")
    df["Holiday_Flag"] = df["Holiday_Flag"].astype("category")
    df["Holiday"] = df["Holiday_Flag"].cat.rename_categories(
        {0: "No Holiday", 1: "Holiday"}
    )

    # Rolling averages
    df["Sales_3week_MA"] = df.groupby("Store")["Weekly_Sales"].transform(
        lambda x: x.rolling(window=3, min_periods=1).mean()
    )
    df["Sales_12week_MA"] = df.groupby("Store")["Weekly_Sales"].transform(
        lambda x: x.rolling(window=12, min_periods=1).mean()
    )

    # Temperature bins
    df["Temp_Bin"] = pd.cut(
        df["Temperature"],
        bins=[-1e9, 40, 60, 80, 1e9],
        labels=["Cold", "Mild", "Warm", "Hot"],
        include_lowest=True,
    )
    df["Temp_Bin"] = pd.Categorical(
        df["Temp_Bin"], categories=["Cold", "Mild", "Warm", "Hot"], ordered=True
    )

    # Season mapping
    df["Season"] = df["Month"].apply(
        lambda x: (
            "Winter"
            if x in [12, 1, 2]
            else "Spring" if x in [3, 4, 5] else "Summer" if x in [6, 7, 8] else "Fall"
        )
    )
    return df


def detect_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Detect outliers using z-score and summarize."""
    df["zscore_sales"] = df.groupby("Store")["Weekly_Sales"].transform(
        lambda x: stats.zscore(x, nan_policy="omit")
    )
    df["is_outlier"] = np.where(np.abs(df["zscore_sales"]) > 3, 1, 0)

    outlier_rows = df[df["is_outlier"] == 1]
    print(f"Found {len(outlier_rows)} outlier rows (>3 std deviations from mean)")
    return df


def summary_statistics(df: pd.DataFrame):
    """Print store summary statistics and data quality report."""
    store_summary = (
        df.groupby("Store")
        .agg(
            mean_sales=("Weekly_Sales", "mean"),
            median_sales=("Weekly_Sales", "median"),
            outlier_pct=("is_outlier", lambda x: 100 * x.mean()),
        )
        .sort_values("mean_sales", ascending=False)
        .round(2)
    )
    print("\nTop 10 Stores by Average Sales:")
    print(store_summary.head(10))

    avg_outlier_pct = store_summary["outlier_pct"].mean()
    print(f"Average percentage of outliers between stores: {avg_outlier_pct:.2f}%")

    def data_health_report(df: pd.DataFrame) -> pd.Series:
        return pd.Series(
            {
                "Total Rows": len(df),
                "Missing Values (any)": df.isna().any(axis=1).sum(),
                "Temp Null %": round(df["Temperature"].isna().mean() * 100, 2),
                "Sales Null %": round(df["Weekly_Sales"].isna().mean() * 100, 2),
                "Outlier %": round(df["is_outlier"].mean() * 100, 2),
            }
        )

    print("\nData Quality Summary:")
    print(data_health_report(df))


def save_clean_data(df: pd.DataFrame, path: str = ".\\data\\walmart_sales_data.csv"):
    """Save cleaned DataFrame to CSV."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8")
    print(f"Cleaned data saved to {path}")


def main():
    df = load_data()
    df = transform_data(df)
    df = detect_outliers(df)
    summary_statistics(df)
    save_clean_data(df)


if __name__ == "__main__":
    main()
