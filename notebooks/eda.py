import pandas as pd
import numpy as np

def run_eda(csv_path="data/processed/clean_sales_history.csv"):
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    
    print("=" * 60)
    print("SUPPLY CHAIN DEMAND FORECASTING - EXPLORATORY DATA ANALYSIS")
    print("=" * 60)
    
    print(f"\n1. Dataset Dimensions: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"2. Date Range: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')} ({(df['date'].max() - df['date'].min()).days + 1} days)")
    print(f"3. Unique Products: {df['product_id'].nunique()}")
    
    print("\n4. Demand Statistics by Product SKU:")
    sku_summary = df.groupby("product_id").agg(
        total_sales=("sales_quantity", "sum"),
        avg_daily_sales=("sales_quantity", "mean"),
        std_daily_sales=("sales_quantity", "std"),
        min_sales=("sales_quantity", "min"),
        max_sales=("sales_quantity", "max"),
        lead_time=("lead_time_days", "first"),
        current_stock=("current_stock", "first"),
        unit_cost=("unit_cost", "first")
    ).reset_index()
    
    print(sku_summary.to_string(index=False))
    
    print("\n5. Day of Week Demand Seasonality (Average Units Sold):")
    df["day_name"] = df["date"].dt.day_name()
    dow_summary = df.groupby("day_name")["sales_quantity"].mean().reindex([
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ])
    for day, val in dow_summary.items():
        bar = "#" * int(val / 2)
        print(f"  {day:<10} | {val:5.1f} units | {bar}")

    print("\n" + "=" * 60)
    print("EDA completed successfully. Ready for Week 2 model training.")
    print("=" * 60)

if __name__ == "__main__":
    run_eda()
