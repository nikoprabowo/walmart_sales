# Walmart Sales Analysis

This repository contains a complete **end-to-end data pipeline** for analyzing Walmart sales data. (by Niko Prabowo - nikoberwibowo@gmail.com)

---

## Project Overview

We aim to answer key business questions about Walmart store performance:

1. How do holidays impact weekly sales?
2. Does air temperature affect consumer spending?
3. Which stores perform best over time?
4. Are there seasonal trends or patterns in sales?
5. Do fuel prices, CPI, and unemployment influence revenue?

---

## Project Structure

```bash
walmart_sales/
├── data/ # Cleaned CSV saved here
├── notebooks/
│ ├── ingest_transform.ipynb # Load and clean raw data
│ └── analysis.ipynb # Business analysis and visualizations
├── reports/
│ ├── Warlmart Sales Dashboard Niko Prabowo.pdf
├── scripts/
│ ├── ingest_transform.py
│ └── analysis.py
├── run_all.sh
├── requirements.txt
└── README.md
```

---

## Setup Instructions

1. Clone the repository
2. Create a Python virtual environment and install dependencies:

```bash
   python -m venv venv
   source venv/bin/activate # Linux/macOS
   venv\Scripts\activate # Windows
   pip install -r requirements.txt
```

3. Run the full pipeline:

```bash
    ./run_all.sh
```

This will:

- Download and load the raw Walmart dataset
- Clean and transform data
- Generate analysis plots and statistics
- Save cleaned CSV to data/walmart_sales_data.csv

## Results

- Cleaned data: ./data/walmart_sales_data.csv
- Visualizations: displayed inline when running analysis.py
- Insights: holiday impact, seasonal trends, top performing stores, and economic factor correlations

## Notes

- Ensure you have a stable internet connection for Kaggle dataset download.
- Scripts are modular and can be reused for similar retail datasets.

---

Thanks.
