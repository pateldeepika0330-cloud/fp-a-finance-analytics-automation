import pandas as pd


# =========================================================
# FP&A AI - FORECASTING AGENT
# =========================================================

def forecast(df):

    print("\n[Forecasting Agent] Starting rolling forecast...")

    result = df.copy()

    # -----------------------------------------------------
    # 1. Sort data chronologically
    # -----------------------------------------------------

    result = result.sort_values(
        [
            "Region",
            "Business_Unit",
            "Month"
        ]
    )

    # -----------------------------------------------------
    # 2. Calculate 3-month moving average
    #
    # Uses previous 3 months of actual revenue
    # to generate the model forecast.
    # -----------------------------------------------------

    result["AI_Revenue_Forecast"] = (
        result
        .groupby(
            ["Region", "Business_Unit"]
        )["Revenue_Actual"]
        .transform(
            lambda x:
            x.shift(1)
            .rolling(
                window=3,
                min_periods=3
            )
            .mean()
        )
    )

    # -----------------------------------------------------
    # 3. Forecast vs Budget
    # -----------------------------------------------------

    result["AI_Forecast_vs_Budget"] = (
        result["AI_Revenue_Forecast"]
        - result["Revenue_Budget"]
    )

    result["AI_Forecast_vs_Budget_Pct"] = (
        result["AI_Forecast_vs_Budget"]
        / result["Revenue_Budget"]
        * 100
    )

    # -----------------------------------------------------
    # 4. Forecast vs Existing Business Forecast
    # -----------------------------------------------------

    result["AI_vs_Business_Forecast"] = (
        result["AI_Revenue_Forecast"]
        - result["Revenue_Forecast"]
    )

    result["AI_vs_Business_Forecast_Pct"] = (
        result["AI_vs_Business_Forecast"]
        / result["Revenue_Forecast"]
        * 100
    )

    # -----------------------------------------------------
    # 5. Forecast Risk Classification
    # -----------------------------------------------------

    def classify_forecast_risk(value):

        if pd.isna(value):
            return "Insufficient History"

        elif value <= -10:
            return "High Risk"

        elif value <= -5:
            return "Medium Risk"

        elif value < 0:
            return "Low Risk"

        else:
            return "On / Above Plan"

    result["Forecast_Risk"] = (
        result["AI_Forecast_vs_Budget_Pct"]
        .apply(classify_forecast_risk)
    )

    # -----------------------------------------------------
    # 6. Forecast accuracy check
    #
    # Compares historical model forecast with actuals.
    # -----------------------------------------------------

    result["Forecast_Error"] = (
        result["Revenue_Actual"]
        - result["AI_Revenue_Forecast"]
    )

    result["Absolute_Forecast_Error_Pct"] = (
        (
            result["Forecast_Error"].abs()
            / result["Revenue_Actual"]
        )
        * 100
    )

    # -----------------------------------------------------
    # 7. Summary statistics
    # -----------------------------------------------------

    valid_forecasts = result.dropna(
        subset=["AI_Revenue_Forecast"]
    )

    if len(valid_forecasts) > 0:

        mape = (
            valid_forecasts[
                "Absolute_Forecast_Error_Pct"
            ].mean()
        )

        print(
            f"[Forecasting Agent] "
            f"Average forecast error: {mape:.2f}%"
        )

    print(
        "[Forecasting Agent] "
        "3-month rolling forecast completed."
    )

    return result


# =========================================================
# TEST AGENT
# =========================================================

if __name__ == "__main__":

    from ingestion_agent import load_data

    finance_data = load_data()

    forecast_data = forecast(finance_data)

    print("\nFORECAST SAMPLE\n")

    print(
        forecast_data[
            [
                "Month",
                "Region",
                "Business_Unit",
                "Revenue_Actual",
                "Revenue_Budget",
                "Revenue_Forecast",
                "AI_Revenue_Forecast",
                "AI_Forecast_vs_Budget_Pct",
                "Forecast_Risk"
            ]
        ]
        .dropna(
            subset=["AI_Revenue_Forecast"]
        )
        .head(15)
        .round(2)
    )