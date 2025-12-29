import pandas as pd
import matplotlib.pyplot as plt
import os

# ---------- COLUMN DEFINITIONS ----------
REQUIRED_COLUMNS = {
    "Sale_Date",
    "Sales_Amount",
    "Quantity_Sold",
    "Region",
    "Product_Category"
}

COLUMN_ALIASES = {
    "Sale_Date": ["sale_date", "date", "sales_date", "transaction_date"],
    "Sales_Amount": ["sales_amount", "amount", "revenue", "sales", "total_sales"],
    "Quantity_Sold": ["quantity_sold", "qty", "units", "units_sold"],
    "Region": ["region", "location", "area", "zone"],
    "Product_Category": ["product_category", "category", "product", "item"]
}

def run_analysis(data):
    """
    data: pandas DataFrame (uploaded CSV already read)
    """

    # ---------------- NORMALIZE COLUMN NAMES ----------------
    data.columns = data.columns.str.strip().str.lower()

    # ---------------- MAP ALIASES ----------------
    rename_map = {}

    for required_col, aliases in COLUMN_ALIASES.items():
        for col in data.columns:
            if col == required_col.lower() or col in aliases:
                rename_map[col] = required_col
                break

    data = data.rename(columns=rename_map)

    # ---------------- VALIDATION ----------------
    missing = REQUIRED_COLUMNS - set(data.columns)
    if missing:
        raise ValueError(
            f"MISSING REQUIRED COLUMNS → {', '.join(missing)}"
        )

    # ---------------- DATE PROCESSING ----------------
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

    top_3_products = product_sales.head(3).to_dict()
    worst_3_products = product_sales.tail(3).to_dict()

    # ---------------- MONTH-WISE SALES ----------------
    monthly_sales = (
        data.groupby(["Month_No", "Month"])["Sales_Amount"]
        .sum()
        .reset_index()
        .sort_values("Month_No")
    )

    # ---------------- GRAPH GENERATION ----------------
    os.makedirs("static/graphs", exist_ok=True)
    plt.style.use("dark_background")

    accent_green = "#00ff41"
    grid_color = "#2f3336"

    # ----- Monthly Trend -----
    plt.figure(figsize=(10, 5), facecolor="#16181c")
    ax = plt.gca()
    ax.set_facecolor("#16181c")

    plt.plot(
        monthly_sales["Month"],
        monthly_sales["Sales_Amount"],
        marker="o",
        color=accent_green,
        linewidth=2
    )

    plt.title("MONTH-WISE PERFORMANCE", loc="left", pad=20)
    plt.grid(color=grid_color, linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.savefig("static/graphs/monthly_sales.png", facecolor="#16181c")
    plt.close()

    # ----- Region Distribution -----
    plt.figure(figsize=(10, 5), facecolor="#16181c")
    ax2 = plt.gca()
    ax2.set_facecolor("#16181c")

    region_sales.plot(
        kind="bar",
        color="#1d9bf0",
        edgecolor=grid_color
    )

    plt.title("REGION DISTRIBUTION", loc="left", pad=20)
    plt.tight_layout()
    plt.savefig("static/graphs/region_sales.png", facecolor="#16181c")
    plt.close()

    # ---------------- RETURN RESULTS ----------------
    return {
        "total_sales": f"${total_sales:,.2f}",
        "total_quantity": f"{int(total_quantity):,}",
        "best_region": best_region,
        "top_3_products": top_3_products,
        "worst_3_products": worst_3_products
    }

