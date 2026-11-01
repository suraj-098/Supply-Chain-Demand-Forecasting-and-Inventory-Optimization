import pandas as pd
import numpy as np

def generate_sample_sales_data(num_days=180, seed=42):
    np.random.seed(seed)
    
    # 6 representative products across categories
    products = [
        {"product_id": "SKU-1001", "name": "Premium Wireless Mouse", "base_demand": 35, "trend": 0.05, "seasonality": 7, "lead_time_days": 5, "current_stock": 180, "unit_cost": 22.50},
        {"product_id": "SKU-1002", "name": "Mechanical Gaming Keyboard", "base_demand": 20, "trend": 0.02, "seasonality": 14, "lead_time_days": 7, "current_stock": 95, "unit_cost": 48.00},
        {"product_id": "SKU-1003", "name": "USB-C Multi-Port Hub", "base_demand": 45, "trend": 0.08, "seasonality": 7, "lead_time_days": 4, "current_stock": 310, "unit_cost": 15.20},
        {"product_id": "SKU-1004", "name": "27-inch 4K Monitor", "base_demand": 12, "trend": 0.01, "seasonality": 30, "lead_time_days": 10, "current_stock": 25, "unit_cost": 210.00},
        {"product_id": "SKU-1005", "name": "Noise Cancelling Headphones", "base_demand": 28, "trend": 0.04, "seasonality": 7, "lead_time_days": 6, "current_stock": 140, "unit_cost": 65.00},
        {"product_id": "SKU-1006", "name": "Ergonomic Desk Mat", "base_demand": 18, "trend": 0.01, "seasonality": 7, "lead_time_days": 3, "current_stock": 110, "unit_cost": 12.00},
    ]
    
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=num_days, freq="D")
    
    records = []
    
    for p in products:
        base = p["base_demand"]
        trend = p["trend"]
        lead_time = p["lead_time_days"]
        stock = p["current_stock"]
        cost = p["unit_cost"]
        
        for t, d in enumerate(dates):
            # Weekly seasonality (higher sales on weekends or mid-week)
            day_of_week = d.dayofweek
            seasonal_factor = 1.0 + 0.25 * np.sin(2 * np.pi * day_of_week / 7)
            trend_factor = 1.0 + (trend * t / num_days)
            noise = np.random.normal(0, base * 0.15)
            
            qty = int(max(0, round(base * seasonal_factor * trend_factor + noise)))
            
            # Stock decreases with sales and replenishes occasionally
            records.append({
                "date": d.strftime("%Y-%m-%d"),
                "product_id": p["product_id"],
                "sales_quantity": qty,
                "current_stock": stock,
                "lead_time_days": lead_time,
                "unit_cost": cost
            })
            
    df = pd.DataFrame(records)
    return df

def generate_sample_with_dirty_records(clean_df):
    dirty_df = clean_df.copy()
    
    # Introduce a duplicate row
    dup = dirty_df.iloc[[5, 20]].copy()
    dirty_df = pd.concat([dirty_df, dup], ignore_index=True)
    
    # Introduce a couple of missing sales values
    dirty_df.loc[12, "sales_quantity"] = np.nan
    dirty_df.loc[45, "sales_quantity"] = np.nan
    
    # Introduce a negative sales anomaly (return or error)
    dirty_df.loc[30, "sales_quantity"] = -5
    
    # Introduce inconsistent date formatting
    dirty_df.loc[60, "date"] = "2026/08/15"
    dirty_df.loc[80, "date"] = "15-09-2026"
    
    return dirty_df

if __name__ == "__main__":
    clean_df = generate_sample_sales_data(num_days=180)
    dirty_df = generate_sample_with_dirty_records(clean_df)
    
    clean_path = "data/processed/clean_sales_history.csv"
    raw_path = "data/raw/sample_sales_raw.csv"
    secondary_path = "data/raw/secondary_sample_sales.csv"
    
    dirty_df.to_csv(raw_path, index=False)
    clean_df.to_csv(clean_path, index=False)
    
    # Secondary sample file for testing Day 7 review
    secondary_df = generate_sample_sales_data(num_days=90, seed=101)
    secondary_df.to_csv(secondary_path, index=False)
    
    print(f"Generated raw dataset: {raw_path} ({len(dirty_df)} rows)")
    print(f"Generated clean dataset: {clean_path} ({len(clean_df)} rows)")
    print(f"Generated secondary dataset: {secondary_path} ({len(secondary_df)} rows)")
