import pandas as pd


# =========================================================
# FP&A AI - COST CENTER ANALYSIS AGENT
# =========================================================

def cost_center(df):

    print("\n[Cost Center Agent] Starting cost center analysis...")

    # Illustrative allocation assumptions for synthetic data
    allocations = {
        "Sales": 0.30,
        "Marketing": 0.20,
        "Technology": 0.25,
        "Finance": 0.10,
        "Operations": 0.15
    }

    cost_center_codes = {
        "Sales": "CC100",
        "Marketing": "CC200",
        "Technology": "CC300",
        "Finance": "CC400",
        "Operations": "CC500"
    }

    records = []

    # -----------------------------------------------------
    # 1. Allocate Opex to cost centers
    # -----------------------------------------------------

    for _, row in df.iterrows():

        for center, allocation_pct in allocations.items():

            actual_opex = (
                row["Opex_Actual"] * allocation_pct
            )

            budget_opex = (
                row["Opex_Budget"] * allocation_pct
            )

            forecast_opex = (
                row["Opex_Forecast"] * allocation_pct
            )

            variance = (
                actual_opex - budget_opex
            )

            variance_pct = (
                variance / budget_opex * 100
                if budget_opex != 0
                else 0
            )

            # For costs:
            # Actual below Budget = Favorable
            status = (
                "Favorable"
                if variance <= 0
                else "Unfavorable"
            )

            records.append({

                "Month": row["Month"],
                "Region": row["Region"],
                "Business_Unit": row["Business_Unit"],

                "Cost_Center": center,
                "Cost_Center_Code": cost_center_codes[center],

                "Allocation_Pct": allocation_pct * 100,

                "Opex_Actual": actual_opex,
                "Opex_Budget": budget_opex,
                "Opex_Forecast": forecast_opex,

                "Opex_Variance": variance,
                "Opex_Variance_Pct": variance_pct,

                "Status": status
            })

    result = pd.DataFrame(records)

    # -----------------------------------------------------
    # 2. Cost center summary
    # -----------------------------------------------------

    summary = (
        result
        .groupby(
            ["Cost_Center_Code", "Cost_Center"],
            as_index=False
        )
        .agg(
            Opex_Actual=("Opex_Actual", "sum"),
            Opex_Budget=("Opex_Budget", "sum"),
            Opex_Forecast=("Opex_Forecast", "sum")
        )
    )

    summary["Opex_Variance"] = (
        summary["Opex_Actual"]
        - summary["Opex_Budget"]
    )

    summary["Opex_Variance_Pct"] = (
        summary["Opex_Variance"]
        / summary["Opex_Budget"]
        * 100
    )

    summary["Status"] = summary[
        "Opex_Variance"
    ].apply(
        lambda x:
        "Favorable"
        if x <= 0
        else "Unfavorable"
    )

    # -----------------------------------------------------
    # 3. Identify largest overspend
    # -----------------------------------------------------

    worst_center = summary.loc[
        summary["Opex_Variance"].idxmax()
    ]

    print(
        "[Cost Center Agent] "
        "Cost center analysis completed."
    )

    print(
        f"[Cost Center Agent] Largest Opex variance: "
        f"{worst_center['Cost_Center']} "
        f"({worst_center['Opex_Variance_Pct']:.2f}%)"
    )

    return result, summary


# =========================================================
# TEST AGENT
# =========================================================

if __name__ == "__main__":

    from ingestion_agent import load_data

    finance_data = load_data()

    cost_center_data, cost_center_summary = (
        cost_center(finance_data)
    )

    print("\nCOST CENTER SUMMARY\n")

    print(
        cost_center_summary.round(2)
    )

    print("\nSAMPLE COST CENTER DATA\n")

    print(
        cost_center_data[
            [
                "Month",
                "Region",
                "Business_Unit",
                "Cost_Center",
                "Opex_Actual",
                "Opex_Budget",
                "Opex_Variance",
                "Opex_Variance_Pct",
                "Status"
            ]
        ]
        .head(10)
        .round(2)
    )