import pandas as pd
import matplotlib.pyplot as plt
import calendar

# ---------------- LOAD DATA ----------------
data = pd.read_csv("sales_data.csv")

# Clean up column names (remove spaces)
data.columns = data.columns.str.strip()
print("Columns found:", data.columns.tolist())

data["Sale_Date"] = pd.to_datetime(data["Sale_Date"])
data["Month"] = data["Sale_Date"].dt.month_name()
data["Month_No"] = data["Sale_Date"].dt.month

# ---------------- BASIC METRICS ----------------
total_sales = data["Sales_Amount"].sum()
print("Total Sales:", total_sales)

total_quantity = data["Quantity_Sold"].sum()
print("Total Quantity Sold:", total_quantity)

# ---------------- PRODUCT-WISE SALES ----------------
product_sales = (
    data.groupby("Product_Category")["Sales_Amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 3 Products:\n", product_sales.head(3))
print("\nWorst 3 Products:\n", product_sales.tail(3))

# ---------------- REGION-WISE SALES ----------------
region_sales = (
    data.groupby("Region")["Sales_Amount"]
    .sum()
    .sort_values(ascending=False)
)
print("\nRegion-wise Sales:\n", region_sales)

# ---------------- MONTH-WISE SALES ----------------
monthly_sales = (
    data.groupby(["Month_No", "Month"])["Sales_Amount"]
    .sum()
    .reset_index()
    .sort_values("Month_No")
)

print("\nMonth-wise Sales:\n", monthly_sales)

# ---------------- GRAPHS ----------------

#  Top 3 Products
plt.figure(figsize=(8, 4))
product_sales.head(3).plot(kind="bar", color="skyblue")
plt.title("Top 3 Product Categories by Sales")
plt.ylabel("Sales Amount")
plt.xlabel("Product Category")
plt.tight_layout()
plt.show()

#  Worst 3 Products
plt.figure(figsize=(8, 4))
product_sales.tail(3).plot(kind="bar", color="salmon")
plt.title("Worst 3 Product Categories by Sales")
plt.ylabel("Sales Amount")
plt.xlabel("Product Category")
plt.tight_layout()
plt.show()

# Region-wise Sales
plt.figure(figsize=(6, 4))
region_sales.plot(kind="bar", color="orange")
plt.title("Region-wise Sales")
plt.ylabel("Sales Amount")
plt.xlabel("Region")
plt.tight_layout()
plt.show()

# Month-wise Trend
plt.figure(figsize=(8, 4))
plt.plot(monthly_sales["Month"], monthly_sales["Sales_Amount"], marker="o", color="green")
plt.title("Month-wise Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales Amount")
plt.xticks(rotation=45)
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()

