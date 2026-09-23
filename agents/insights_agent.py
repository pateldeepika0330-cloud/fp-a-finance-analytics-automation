import pandas as pd


# =========================================================
# FP&A AI - MANAGEMENT INSIGHTS AGENT
# =========================================================

def insights(df):

    print("\n[Insights Agent] Generating management insights...")

    insights_list = []

    # -----------------------------------------------------
    # 1. COMPANY-LEVEL KPIs
    # -----------------------------------------------------

    actual_revenue = df["Revenue_Actual"].sum()
    budget_revenue = df["Revenue_Budget"].sum()

    actual_opex = df["Opex_Actual"].sum()
    budget_opex = df["Opex_Budget"].sum()

    actual_ebitda = df["EBITDA_Actual"].sum()
    budget_ebitda = df["EBITDA_Budget"].sum()

    revenue_variance = (
        actual_revenue - budget_revenue
    )

    revenue_variance_pct = (
        revenue_variance / budget_revenue * 100
    )

    opex_variance = (
        actual_opex - budget_opex
    )

    opex_variance_pct = (
        opex_variance / budget_opex * 100
    )

    ebitda_variance = (
        actual_ebitda - budget_ebitda
    )

    ebitda_variance_pct = (
        ebitda_variance / budget_ebitda * 100
    )

    # -----------------------------------------------------
    # 2. REVENUE INSIGHT
    # -----------------------------------------------------

    if revenue_variance < 0:

        revenue_status = "below"

        revenue_action = (
            "Review sales pipeline, conversion rates, "
            "pricing and regional revenue assumptions."
        )

    else:

        revenue_status = "above"

        revenue_action = (
            "Assess whether favorable revenue performance "
            "is sustainable and reflect it in the rolling forecast."
        )

    insights_list.append({
        "Category": "Revenue",
        "Observation":
            f"Revenue is {abs(revenue_variance_pct):.2f}% "
            f"{revenue_status} budget.",
        "Financial_Impact": revenue_variance,
        "Recommended_Action": revenue_action
    })

    # -----------------------------------------------------
    # 3. OPEX INSIGHT
    # -----------------------------------------------------

    if opex_variance > 0:

        opex_status = "above"

        opex_action = (
            "Review discretionary spend, hiring, vendor costs "
            "and cost-center overspend."
        )

    else:

        opex_status = "below"

        opex_action = (
            "Validate whether underspend represents sustainable "
            "savings or timing-related expenditure."
        )

    insights_list.append({
        "Category": "Opex",
        "Observation":
            f"Opex is {abs(opex_variance_pct):.2f}% "
            f"{opex_status} budget.",
        "Financial_Impact": opex_variance,
        "Recommended_Action": opex_action
    })

    # -----------------------------------------------------
    # 4. EBITDA INSIGHT
    # -----------------------------------------------------

    if ebitda_variance < 0:

        ebitda_status = "below"

        ebitda_action = (
            "Assess revenue recovery opportunities and "
            "cost-control measures to protect profitability."
        )

    else:

        ebitda_status = "above"

        ebitda_action = (
            "Validate key drivers of EBITDA outperformance "
            "and incorporate sustainable improvements into forecast."
        )

    insights_list.append({
        "Category": "EBITDA",
        "Observation":
            f"EBITDA is {abs(ebitda_variance_pct):.2f}% "
            f"{ebitda_status} budget.",
        "Financial_Impact": ebitda_variance,
        "Recommended_Action": ebitda_action
    })

    # -----------------------------------------------------
    # 5. REGIONAL REVENUE DRIVER
    # -----------------------------------------------------

    region_summary = (
        df.groupby(
            "Region",
            as_index=False
        )
        .agg(
            Revenue_Actual=("Revenue_Actual", "sum"),
            Revenue_Budget=("Revenue_Budget", "sum")
        )
    )

    region_summary["Variance"] = (
        region_summary["Revenue_Actual"]
        - region_summary["Revenue_Budget"]
    )

    region_summary["Variance_Pct"] = (
        region_summary["Variance"]
        / region_summary["Revenue_Budget"]
        * 100
    )

    weakest_region = region_summary.loc[
        region_summary["Variance"].idxmin()
    ]

    insights_list.append({
        "Category": "Regional Performance",
        "Observation":
            f"{weakest_region['Region']} has the largest "
            f"revenue pressure at "
            f"{weakest_region['Variance_Pct']:.2f}% vs budget.",
        "Financial_Impact":
            weakest_region["Variance"],
        "Recommended_Action":
            "Review regional pipeline, pricing, volume and "
            "forecast assumptions."
    })

    # -----------------------------------------------------
    # 6. BUSINESS UNIT DRIVER
    # -----------------------------------------------------

    bu_summary = (
        df.groupby(
            "Business_Unit",
            as_index=False
        )
        .agg(
            EBITDA_Actual=("EBITDA_Actual", "sum"),
            EBITDA_Budget=("EBITDA_Budget", "sum")
        )
    )

    bu_summary["Variance"] = (
        bu_summary["EBITDA_Actual"]
        - bu_summary["EBITDA_Budget"]
    )

    weakest_bu = bu_summary.loc[
        bu_summary["Variance"].idxmin()
    ]

    insights_list.append({
        "Category": "Business Unit",
        "Observation":
            f"{weakest_bu['Business_Unit']} has the largest "
            f"negative EBITDA variance.",
        "Financial_Impact":
            weakest_bu["Variance"],
        "Recommended_Action":
            "Perform driver-level review of revenue, gross margin "
            "and operating expenses for this business unit."
    })

    # -----------------------------------------------------
    # 7. Convert insights into dataframe
    # -----------------------------------------------------

    insights_df = pd.DataFrame(
        insights_list
    )

    # -----------------------------------------------------
    # 8. Determine priority
    # -----------------------------------------------------

    def priority(value):

        absolute_value = abs(value)

        if absolute_value >= 5_000_000:
            return "High"

        elif absolute_value >= 1_000_000:
            return "Medium"

        else:
            return "Low"

    insights_df["Priority"] = (
        insights_df["Financial_Impact"]
        .apply(priority)
    )

    print(
        f"[Insights Agent] "
        f"{len(insights_df)} management insights generated."
    )

    return insights_df


# =========================================================
# TEST AGENT
# =========================================================

if __name__ == "__main__":

    from ingestion_agent import load_data

    finance_data = load_data()

    management_insights = insights(
        finance_data
    )

    print("\nMANAGEMENT INSIGHTS\n")

    for _, row in management_insights.iterrows():

        print(
            f"\n[{row['Priority']}] "
            f"{row['Category']}"
        )

        print(
            f"Observation: "
            f"{row['Observation']}"
        )

        print(
            f"Financial Impact: "
            f"{row['Financial_Impact']:,.2f}"
        )

        print(
            f"Recommended Action: "
            f"{row['Recommended_Action']}"
        )