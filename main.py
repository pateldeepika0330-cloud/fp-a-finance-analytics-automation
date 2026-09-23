from pathlib import Path
import pandas as pd

from agents.ingestion_agent import load_data
from agents.variance_agent import variance
from agents.forecasting_agent import forecast
from agents.scenario_agent import scenario
from agents.costcenter_agent import cost_center
from agents.insights_agent import insights


# =========================================================
# FP&A AGENTIC AI AUTOMATION PIPELINE
# =========================================================

def run_pipeline():

    print("\n")
    print("=" * 60)
    print("FP&A AGENTIC AI FINANCE AUTOMATION")
    print("=" * 60)

    # -----------------------------------------------------
    # STEP 1 - DATA INGESTION
    # -----------------------------------------------------

    finance_data = load_data(
        "data/financials.xlsx"
    )

    # -----------------------------------------------------
    # STEP 2 - VARIANCE ANALYSIS
    # -----------------------------------------------------

    variance_data, region_summary = variance(
        finance_data
    )

    # -----------------------------------------------------
    # STEP 3 - FORECASTING
    # -----------------------------------------------------

    forecast_data = forecast(
        finance_data
    )

    # -----------------------------------------------------
    # STEP 4 - SCENARIO PLANNING
    # -----------------------------------------------------

    scenario_data = scenario(
        finance_data
    )

    # -----------------------------------------------------
    # STEP 5 - COST CENTER ANALYSIS
    # -----------------------------------------------------

    cost_center_data, cost_center_summary = (
        cost_center(finance_data)
    )

    # -----------------------------------------------------
    # STEP 6 - MANAGEMENT INSIGHTS
    # -----------------------------------------------------

    management_insights = insights(
        finance_data
    )

    # -----------------------------------------------------
    # STEP 7 - EXECUTIVE KPI SUMMARY
    # -----------------------------------------------------

    executive_summary = pd.DataFrame({

        "KPI": [
            "Revenue",
            "Opex",
            "EBITDA"
        ],

        "Actual": [
            finance_data["Revenue_Actual"].sum(),
            finance_data["Opex_Actual"].sum(),
            finance_data["EBITDA_Actual"].sum()
        ],

        "Budget": [
            finance_data["Revenue_Budget"].sum(),
            finance_data["Opex_Budget"].sum(),
            finance_data["EBITDA_Budget"].sum()
        ],

        "Forecast": [
            finance_data["Revenue_Forecast"].sum(),
            finance_data["Opex_Forecast"].sum(),
            finance_data["EBITDA_Forecast"].sum()
        ]
    })

    executive_summary["Variance"] = (
        executive_summary["Actual"]
        - executive_summary["Budget"]
    )

    executive_summary["Variance_Pct"] = (
        executive_summary["Variance"]
        / executive_summary["Budget"]
        * 100
    )

    # -----------------------------------------------------
    # STEP 8 - SCENARIO SUMMARY
    # -----------------------------------------------------

    scenario_summary = pd.DataFrame({

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

    scenario_summary["EBITDA_Margin_Pct"] = (
        scenario_summary["EBITDA"]
        / scenario_summary["Revenue"]
        * 100
    )

    # -----------------------------------------------------
    # STEP 9 - CREATE OUTPUT DIRECTORY
    # -----------------------------------------------------

    output_directory = Path("output")

    output_directory.mkdir(
        exist_ok=True
    )

    output_file = (
        output_directory
        / "final_report.xlsx"
    )

    # -----------------------------------------------------
    # STEP 10 - EXPORT EXCEL MANAGEMENT REPORT
    # -----------------------------------------------------

    print(
        "\n[Pipeline] Creating management report..."
    )

    with pd.ExcelWriter(
        output_file,
        engine="openpyxl"
    ) as writer:

        executive_summary.to_excel(
            writer,
            sheet_name="Executive Summary",
            index=False
        )

        management_insights.to_excel(
            writer,
            sheet_name="Management Insights",
            index=False
        )

        region_summary.to_excel(
            writer,
            sheet_name="Regional Analysis",
            index=False
        )

        cost_center_summary.to_excel(
            writer,
            sheet_name="Cost Center Summary",
            index=False
        )

        scenario_summary.to_excel(
            writer,
            sheet_name="Scenario Summary",
            index=False
        )

        variance_data.to_excel(
            writer,
            sheet_name="Variance Detail",
            index=False
        )

        forecast_data.to_excel(
            writer,
            sheet_name="Forecast Detail",
            index=False
        )

        cost_center_data.to_excel(
            writer,
            sheet_name="Cost Center Detail",
            index=False
        )

    # -----------------------------------------------------
    # PIPELINE COMPLETE
    # -----------------------------------------------------

    print("\n" + "=" * 60)

    print(
        "FP&A AUTOMATION COMPLETED SUCCESSFULLY"
    )

    print("=" * 60)

    print(
        f"\nManagement report created:"
        f"\n{output_file}"
    )

    print(
        "\nAgents successfully executed:"
    )

    print(
        """
        ✓ Data Ingestion Agent
        ✓ Variance Analysis Agent
        ✓ Forecasting Agent
        ✓ Scenario Planning Agent
        ✓ Cost Center Agent
        ✓ Management Insights Agent
        """
    )

    return {
        "finance_data": finance_data,
        "variance_data": variance_data,
        "forecast_data": forecast_data,
        "scenario_data": scenario_data,
        "cost_center_data": cost_center_data,
        "management_insights": management_insights,
        "executive_summary": executive_summary
    }


# =========================================================
# RUN PIPELINE
# =========================================================

if __name__ == "__main__":

    results = run_pipeline()