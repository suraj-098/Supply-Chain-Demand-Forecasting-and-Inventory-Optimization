# DATA DICTIONARY
## Supply Chain Demand Forecasting and Inventory Optimization Dataset

### 1. Overview
This dataset contains historical daily product sales records along with operational parameters essential for demand forecasting and inventory replenishment optimization.

### 2. Field Specifications

| Field Name | Data Type | Required? | Description | Example Values | Validation Rules |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `date` | String / Date (ISO 8601) | **Yes (P0)** | Date of sales record or week-ending timestamp | `2026-05-01`, `2026-10-15` | Must parse to valid timestamp; chronological per product. |
| `product_id` | String | **Yes (P0)** | Unique identifier for SKU / item | `SKU-1001`, `SKU-1004` | Non-empty alphanumeric string, max 64 chars. |
| `sales_quantity` | Integer / Float | **Yes (P0)** | Number of units sold on given date | `35`, `0`, `12` | Must be non-negative integer ($\ge 0$). Nulls coerced/filled. |
| `current_stock` | Integer | **Recommended** | Units currently on hand in inventory | `180`, `25`, `310` | Non-negative integer. If absent, fallback defaults to 0 or demo input. |
| `lead_time_days`| Integer | **Recommended** | Supplier fulfillment delay in days | `5`, `7`, `10` | Positive integer ($\ge 1$). Fallback default: 7 days. |
| `unit_cost` | Float | **Optional** | Cost of goods sold (COGS) / unit price | `22.50`, `210.00` | Non-negative float. Used for inventory valuation. Fallback: 1.00. |

### 3. Missing Value & Edge Case Policy
1. **Missing `sales_quantity`**: Imputed with `0` (indicating zero sales on that period).
2. **Negative `sales_quantity`**: Flagged as return/anomaly and clipped to `0` or filtered out with an explicit warning.
3. **Duplicate `(date, product_id)` entries**: Aggregated via `sum()` to obtain total daily demand for that SKU.
4. **Missing `current_stock`**: Populated with configurable baseline or median historical stock.
5. **Missing `lead_time_days`**: Populated with standard supplier lead time assumption (7 days).
