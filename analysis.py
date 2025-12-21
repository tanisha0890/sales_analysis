import pandas as pd
import matplotlib.pyplot as plt
import os

def analyze_sales():
    # ---------------- LOAD DATA ----------------
    # Ensure sales_data.csv exists in the same folder
    data = pd.read_csv("sales_data.csv")
    data.columns = data.columns.str.strip()

    # Date processing
    data["Sale_Date"] = pd.to_datetime(data["Sale_Date"])
    data["Month"] = data["Sale_Date"].dt.month_name()
    data["Month_No"] = data["Sale_Date"].dt.month

    # ---------------- NUMERIC INSIGHTS ----------------
    total_sales = data["Sales_Amount"].sum()
    total_quantity = data["Quantity_Sold"].sum()

    region_sales = (
        data.groupby("Region")["Sales_Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    best_region = region_sales.idxmax()

    product_sales = (
        data.groupby("Product_Category")["Sales_Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    top_3_products = product_sales.head(3)
    worst_3_products = product_sales.tail(3)

    # ---------------- MONTH-WISE SALES ----------------
    monthly_sales = (
        data.groupby(["Month_No", "Month"])["Sales_Amount"]
        .sum()
        .reset_index()
        .sort_values("Month_No")
    )

    # ---------------- GRAPH STYLING (STOCK STYLE) ----------------
    os.makedirs("static/graphs", exist_ok=True)
    plt.style.use('dark_background')
    
    # Common chart properties
    accent_green = "#00ff41"
    grid_color = "#2f3336"

    # Graph 1: Trend Line
    plt.figure(figsize=(10, 5), facecolor='#16181c')
    ax = plt.gca()
    ax.set_facecolor('#16181c')
    
    plt.plot(monthly_sales["Month"], monthly_sales["Sales_Amount"], 
             marker="o", color=accent_green, linewidth=2, markersize=6)
    
    plt.title("MONTH-WISE PERFORMANCE", color='white', fontsize=12, loc='left', pad=20)
    plt.grid(color=grid_color, linestyle='--', linewidth=0.5)
    plt.xticks(rotation=0, color='#71767b')
    plt.yticks(color='#71767b')
    plt.tight_layout()
    plt.savefig("static/graphs/monthly_sales.png", facecolor='#16181c')
    plt.close()

    # Graph 2: Region Bar Chart
    plt.figure(figsize=(10, 5), facecolor='#16181c')
    ax2 = plt.gca()
    ax2.set_facecolor('#16181c')
    
    region_sales.plot(kind="bar", color='#1d9bf0', edgecolor=grid_color)
    
    plt.title("REGION DISTRIBUTION", color='white', fontsize=12, loc='left', pad=20)
    plt.xticks(rotation=0, color='#71767b')
    plt.yticks(color='#71767b')
    plt.tight_layout()
    plt.savefig("static/graphs/region_sales.png", facecolor='#16181c')
    plt.close()

    return {
        "total_sales": f"${total_sales:,.2f}",
        "total_quantity": f"{total_quantity:,}",
        "best_region": best_region,
        "top_3_products": top_3_products,
        "worst_3_products": worst_3_products
    }
