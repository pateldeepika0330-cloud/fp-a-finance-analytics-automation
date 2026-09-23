import pandas as pd


# =========================================================
# FP&A AI - VARIANCE ANALYSIS AGENT
# =========================================================

def variance(df):

    print("\n[Variance Agent] Starting variance analysis...")

    result = df.copy()

    # -----------------------------------------------------
    # 1. Revenue Variance
    # Revenue: Higher Actual than Budget = Favorable
    # -----------------------------------------------------

    result["Revenue_Variance"] = (
        result["Revenue_Actual"]
        - result["Revenue_Budget"]
    )

    result["Revenue_Variance_Pct"] = (
        result["Revenue_Variance"]
        / result["Revenue_Budget"]
        * 100
    )

    result["Revenue_Status"] = result[
        "Revenue_Variance"
    ].apply(
        lambda x: "Favorable"
        if x >= 0
        else "Unfavorable"
    )

    # -----------------------------------------------------
    # 2. Opex Variance
    # Cost: Lower Actual than Budget = Favorable
    # -----------------------------------------------------

    result["Opex_Variance"] = (
        result["Opex_Actual"]
        - result["Opex_Budget"]
    )

    result["Opex_Variance_Pct"] = (
        result["Opex_Variance"]
        / result["Opex_Budget"]
        * 100
    )

    result["Opex_Status"] = result[
        "Opex_Variance"
    ].apply(
        lambda x: "Favorable"
        if x <= 0
        else "Unfavorable"
    )

    # -----------------------------------------------------
    # 3. EBITDA Variance
    # Higher EBITDA than Budget = Favorable
    # -----------------------------------------------------

    result["EBITDA_Variance"] = (
        result["EBITDA_Actual"]
        - result["EBITDA_Budget"]
    )

    result["EBITDA_Variance_Pct"] = (
        result["EBITDA_Variance"]
        / result["EBITDA_Budget"]
        * 100
    )

    result["EBITDA_Status"] = result[
        "EBITDA_Variance"
    ].apply(
        lambda x: "Favorable"
        if x >= 0
        else "Unfavorable"
    )

    # -----------------------------------------------------
    # 4. Materiality Classification
    #
    # < 5%  = Low
    # 5-10% = Medium
    # >10%  = High
    # -----------------------------------------------------

    def classify_materiality(value):

        absolute_value = abs(value)

        if absolute_value >= 10:
            return "High"

        elif absolute_value >= 5:
            return "Medium"

        else:
            return "Low"

    result["Revenue_Materiality"] = (
        result["Revenue_Variance_Pct"]
        .apply(classify_materiality)
    )

    result["Opex_Materiality"] = (
        result["Opex_Variance_Pct"]
        .apply(classify_materiality)
    )

    # -----------------------------------------------------
    # 5. Management Attention Flag
    # -----------------------------------------------------

    result["Management_Attention"] = result.apply(
        lambda row:
        "Review Required"
        if (
            row["Revenue_Materiality"] == "High"
            or row["Opex_Materiality"] == "High"
        )
        else "Normal",
        axis=1
    )

    # -----------------------------------------------------
    # 6. Portfolio / Region Summary
    # -----------------------------------------------------

    region_summary = (
        result
        .groupby("Region", as_index=False)
        .agg(
            Revenue_Actual=("Revenue_Actual", "sum"),
            Revenue_Budget=("Revenue_Budget", "sum"),
            Opex_Actual=("Opex_Actual", "sum"),
            Opex_Budget=("Opex_Budget", "sum"),
            EBITDA_Actual=("EBITDA_Actual", "sum"),
            EBITDA_Budget=("EBITDA_Budget", "sum")
        )
    )

    region_summary["Revenue_Variance"] = (
        region_summary["Revenue_Actual"]
        - region_summary["Revenue_Budget"]
    )

    region_summary["Revenue_Variance_Pct"] = (
        region_summary["Revenue_Variance"]
        / region_summary["Revenue_Budget"]
        * 100
    )

    region_summary["EBITDA_Variance"] = (
        region_summary["EBITDA_Actual"]
        - region_summary["EBITDA_Budget"]
    )

    # -----------------------------------------------------
    # 7. Identify largest unfavorable revenue driver
    # -----------------------------------------------------

    worst_region = region_summary.loc[
        region_summary["Revenue_Variance"].idxmin()
    ]

    print(
        "[Variance Agent] Variance calculations completed."
    )

    print(
        f"[Variance Agent] Largest revenue pressure: "
        f"{worst_region['Region']} "
        f"({worst_region['Revenue_Variance_Pct']:.2f}%)"
    )

    return result, region_summary


# =========================================================
# TEST AGENT
# =========================================================

if __name__ == "__main__":

    from ingestion_agent import load_data

    finance_data = load_data()

    variance_data, region_summary = variance(
        finance_data
    )

    print("\nREGIONAL VARIANCE SUMMARY\n")

    print(
        region_summary[
            [
                "Region",
                "Revenue_Actual",
                "Revenue_Budget",
                "Revenue_Variance",
                "Revenue_Variance_Pct",
                "EBITDA_Variance"
            ]
        ].round(2)
    )

    print("\nSAMPLE VARIANCE ANALYSIS\n")

    print(
        variance_data[
            [
                "Month",
                "Region",
                "Business_Unit",
                "Revenue_Variance_Pct",
                "Revenue_Status",
                "Opex_Variance_Pct",
                "Opex_Status",
                "Revenue_Materiality",
                "Management_Attention"
            ]
        ].head(10)
    )
    