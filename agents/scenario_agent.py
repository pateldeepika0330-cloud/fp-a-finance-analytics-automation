import pandas as pd


# =========================================================
# FP&A AI - SCENARIO PLANNING AGENT
# =========================================================

def scenario(df):

    print("\n[Scenario Agent] Starting scenario analysis...")

    result = df.copy()

    # -----------------------------------------------------
    # Scenario assumptions
    # -----------------------------------------------------

    # Base Case:
    # Uses the current business forecast.

    # Best Case:
    # Revenue +10%
    # COGS improves by 2%
    # Opex remains controlled.

    # Worst Case:
    # Revenue -10%
    # COGS increases by 3%
    # Opex increases by 5%.

    # -----------------------------------------------------
    # 1. BASE CASE
    # -----------------------------------------------------

    result["Base_Revenue"] = (
        result["Revenue_Forecast"]
    )

    result["Base_COGS"] = (
        result["COGS_Forecast"]
    )

    result["Base_Opex"] = (
        result["Opex_Forecast"]
    )

    result["Base_EBITDA"] = (
        result["Base_Revenue"]
        - result["Base_COGS"]
        - result["Base_Opex"]
    )

    # -----------------------------------------------------
    # 2. BEST CASE
    # -----------------------------------------------------

    result["Best_Revenue"] = (
        result["Revenue_Forecast"] * 1.10
    )

    result["Best_COGS"] = (
        result["COGS_Forecast"] * 0.98
    )

    result["Best_Opex"] = (
        result["Opex_Forecast"]
    )

    result["Best_EBITDA"] = (
        result["Best_Revenue"]
        - result["Best_COGS"]
        - result["Best_Opex"]
    )

    # -----------------------------------------------------
    # 3. WORST CASE
    # -----------------------------------------------------

    result["Worst_Revenue"] = (
        result["Revenue_Forecast"] * 0.90
    )

    result["Worst_COGS"] = (
        result["COGS_Forecast"] * 1.03
    )

    result["Worst_Opex"] = (
        result["Opex_Forecast"] * 1.05
    )

    result["Worst_EBITDA"] = (
        result["Worst_Revenue"]
        - result["Worst_COGS"]
        - result["Worst_Opex"]
    )

    # -----------------------------------------------------
    # 4. EBITDA MARGINS
    # -----------------------------------------------------

    result["Base_EBITDA_Margin"] = (
        result["Base_EBITDA"]
        / result["Base_Revenue"]
        * 100
    )

    result["Best_EBITDA_Margin"] = (
        result["Best_EBITDA"]
        / result["Best_Revenue"]
        * 100
    )

    result["Worst_EBITDA_Margin"] = (
        result["Worst_EBITDA"]
        / result["Worst_Revenue"]
        * 100
    )

    # -----------------------------------------------------
    # 5. Scenario impact
    # -----------------------------------------------------

    result["Best_vs_Base_EBITDA"] = (
        result["Best_EBITDA"]
        - result["Base_EBITDA"]
    )

    result["Worst_vs_Base_EBITDA"] = (
        result["Worst_EBITDA"]
        - result["Base_EBITDA"]
    )

    # -----------------------------------------------------
    # 6. Management Risk Flag
    # -----------------------------------------------------

    result["Scenario_Risk"] = result[
        "Worst_EBITDA_Margin"
    ].apply(
        lambda x:
        "Critical"
        if x < 10
        else (
            "High"
            if x < 20
            else (
                "Medium"
                if x < 30
                else "Low"
            )
        )
    )

    print(
        "[Scenario Agent] "
        "Base, Best and Worst cases generated."
    )

    return result


# =========================================================
# TEST AGENT
# =========================================================

if __name__ == "__main__":

    from ingestion_agent import load_data

    finance_data = load_data()

    scenario_data = scenario(finance_data)

    # -----------------------------------------------------
    # Company-level scenario summary
    # -----------------------------------------------------

    summary = pd.DataFrame({

        "Scenario": [
            "Base Case",
            "Best Case",
            "Worst Case"
        ],

        "Revenue": [
            scenario_data["Base_Revenue"].sum(),
            scenario_data["Best_Revenue"].sum(),
            scenario_data["Worst_Revenue"].sum()
        ],

        "EBITDA": [
            scenario_data["Base_EBITDA"].sum(),
            scenario_data["Best_EBITDA"].sum(),
            scenario_data["Worst_EBITDA"].sum()
        ]
    })

    summary["EBITDA_Margin_Pct"] = (
        summary["EBITDA"]
        / summary["Revenue"]
        * 100
    )

    print("\nCOMPANY SCENARIO SUMMARY\n")

    print(
        summary.round(2)
    )

    print("\nSAMPLE BUSINESS UNIT SCENARIOS\n")

    print(
        scenario_data[
            [
                "Month",
                "Region",
                "Business_Unit",
                "Base_EBITDA",
                "Best_EBITDA",
                "Worst_EBITDA",
                "Base_EBITDA_Margin",
                "Worst_EBITDA_Margin",
                "Scenario_Risk"
            ]
        ]
        .head(10)
        .round(2)
    )