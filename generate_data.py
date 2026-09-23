import pandas as pd
import numpy as np
from pathlib import Path

# ---------------------------------------------------------
# FP&A AI Portfolio Project
# Synthetic Financial Dataset Generator
# ---------------------------------------------------------

np.random.seed(42)

# Create output folder if it does not exist
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Business dimensions
months = pd.date_range(
    start="2025-01-01",
    end="2026-12-01",
    freq="MS"
)

regions = ["North America", "EMEA", "APAC"]

business_units = [
    "Enterprise",
    "SMB",
    "Digital"
]

cost_centers = {
    "Sales": "CC100",
    "Marketing": "CC200",
    "Technology": "CC300",
    "Finance": "CC400",
    "Operations": "CC500"
}

records = []

# ---------------------------------------------------------
# Generate monthly FP&A data
# ---------------------------------------------------------

for month in months:

    for region in regions:

        for business_unit in business_units:

            # -------------------------
            # Revenue
            # -------------------------

            base_revenue = np.random.randint(700_000, 1_500_000)

            budget_revenue = base_revenue

            actual_revenue = budget_revenue * np.random.uniform(
                0.88, 1.12
            )

            forecast_revenue = actual_revenue * np.random.uniform(
                0.97, 1.08
            )

            # -------------------------
            # COGS
            # -------------------------

            budget_cogs = budget_revenue * np.random.uniform(
                0.38, 0.45
            )

            actual_cogs = actual_revenue * np.random.uniform(
                0.39, 0.47
            )

            forecast_cogs = forecast_revenue * np.random.uniform(
                0.39, 0.46
            )

            # -------------------------
            # Operating expenses
            # -------------------------

            budget_opex = budget_revenue * np.random.uniform(
                0.20, 0.30
            )

            actual_opex = budget_opex * np.random.uniform(
                0.90, 1.15
            )

            forecast_opex = actual_opex * np.random.uniform(
                0.98, 1.07
            )

            # -------------------------
            # Profitability
            # -------------------------

            actual_gross_profit = (
                actual_revenue - actual_cogs
            )

            budget_gross_profit = (
                budget_revenue - budget_cogs
            )

            forecast_gross_profit = (
                forecast_revenue - forecast_cogs
            )

            actual_ebitda = (
                actual_gross_profit - actual_opex
            )

            budget_ebitda = (
                budget_gross_profit - budget_opex
            )

            forecast_ebitda = (
                forecast_gross_profit - forecast_opex
            )

            # -------------------------
            # Headcount
            # -------------------------

            budget_headcount = np.random.randint(80, 250)

            actual_headcount = int(
                budget_headcount *
                np.random.uniform(0.92, 1.08)
            )

            # -------------------------
            # Store record
            # -------------------------

            records.append({

                "Month": month,
                "Region": region,
                "Business_Unit": business_unit,

                "Revenue_Actual": round(actual_revenue, 2),
                "Revenue_Budget": round(budget_revenue, 2),
                "Revenue_Forecast": round(forecast_revenue, 2),

                "COGS_Actual": round(actual_cogs, 2),
                "COGS_Budget": round(budget_cogs, 2),
                "COGS_Forecast": round(forecast_cogs, 2),

                "Opex_Actual": round(actual_opex, 2),
                "Opex_Budget": round(budget_opex, 2),
                "Opex_Forecast": round(forecast_opex, 2),

                "Gross_Profit_Actual": round(actual_gross_profit, 2),
                "Gross_Profit_Budget": round(budget_gross_profit, 2),
                "Gross_Profit_Forecast": round(forecast_gross_profit, 2),

                "EBITDA_Actual": round(actual_ebitda, 2),
                "EBITDA_Budget": round(budget_ebitda, 2),
                "EBITDA_Forecast": round(forecast_ebitda, 2),

                "Headcount_Actual": actual_headcount,
                "Headcount_Budget": budget_headcount
            })


# ---------------------------------------------------------
# Create dataframe
# ---------------------------------------------------------

df = pd.DataFrame(records)

# ---------------------------------------------------------
# Add variance calculations
# ---------------------------------------------------------

df["Revenue_Variance"] = (
    df["Revenue_Actual"] -
    df["Revenue_Budget"]
)

df["Revenue_Variance_Pct"] = (
    df["Revenue_Variance"] /
    df["Revenue_Budget"]
) * 100

df["Opex_Variance"] = (
    df["Opex_Actual"] -
    df["Opex_Budget"]
)

df["EBITDA_Variance"] = (
    df["EBITDA_Actual"] -
    df["EBITDA_Budget"]
)

# ---------------------------------------------------------
# Save files
# ---------------------------------------------------------

csv_path = DATA_DIR / "financials.csv"
excel_path = DATA_DIR / "financials.xlsx"

df.to_csv(csv_path, index=False)

df.to_excel(
    excel_path,
    index=False,
    sheet_name="Financial_Data"
)

print("------------------------------------------")
print("FP&A dataset generated successfully!")
print("------------------------------------------")

print(f"Rows created: {len(df)}")
print(f"CSV file: {csv_path}")
print(f"Excel file: {excel_path}")

print("\nSample data:")
print(df.head())