#!/bin/bash
# ============================================================
# Walmart Sales Analysis - Run All Pipeline - Niko Prabowo - nikoberwibowo@gmail.com
# ============================================================

# Exit immediately if a command exits with a non-zero status
set -e

# Activate virtual environment if needed
# source venv/bin/activate

echo "=================================================="
echo "Step 1: Running data ingest & transform..."
echo "=================================================="
python scripts/ingest_transform.py

echo "=================================================="
echo "Step 2: Running data analysis..."
echo "=================================================="
python scripts/analysis.py

echo "=================================================="
echo "Pipeline finished successfully!"
echo "Cleaned data saved in './data/walmart_sales_data.csv'"
echo "Plots and analysis displayed in your Python environment."