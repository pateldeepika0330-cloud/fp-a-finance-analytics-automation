import pandas as pd
from pathlib import Path


# =========================================================
# FP&A AI - DATA INGESTION AGENT
# =========================================================

REQUIRED_COLUMNS = [
    "Month",
    "Region",
    "Business_Unit",
    "Revenue_Actual",
    "Revenue_Budget",
    "Revenue_Forecast",
    "COGS_Actual",
    "COGS_Budget",
    "COGS_Forecast",
    "Opex_Actual",
    "Opex_Budget",
    "Opex_Forecast",
    "EBITDA_Actual",
    "EBITDA_Budget",
    "EBITDA_Forecast",
]


def load_data(file_path="data/financials.xlsx"):

    print("\n[Ingestion Agent] Starting data ingestion...")

    path = Path(file_path)

    # -----------------------------------------------------
    # 1. Check whether the financial file exists
    # -----------------------------------------------------

    if not path.exists():
        raise FileNotFoundError(
            f"Financial data file not found: {file_path}"
        )

    # -----------------------------------------------------
    # 2. Load the financial data
    # -----------------------------------------------------

    if path.suffix.lower() == ".xlsx":

        df = pd.read_excel(path)

    elif path.suffix.lower() == ".csv":

        df = pd.read_csv(path)

    else:

        raise ValueError(
            "Unsupported file format. Use CSV or Excel."
        )

    print(
        f"[Ingestion Agent] Loaded {len(df)} financial records."
    )

    # -----------------------------------------------------
    # 3. Validate required finance fields
    # -----------------------------------------------------

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    print(
        "[Ingestion Agent] Required financial fields validated."
    )

    # -----------------------------------------------------
    # 4. Standardize date
    # -----------------------------------------------------

    df["Month"] = pd.to_datetime(
        df["Month"],
        errors="coerce"
    )

    # -----------------------------------------------------
    # 5. Check duplicate records
    # -----------------------------------------------------

    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:

        print(
            f"[Ingestion Agent] Removing "
            f"{duplicate_count} duplicate records."
        )

        df = df.drop_duplicates()

    else:

        print(
            "[Ingestion Agent] No duplicate records detected."
        )

    # -----------------------------------------------------
    # 6. Check missing values
    # -----------------------------------------------------

    missing_values = (
        df[REQUIRED_COLUMNS]
        .isnull()
        .sum()
        .sum()
    )

    if missing_values > 0:

        print(
            f"[Ingestion Agent] Warning: "
            f"{missing_values} missing values detected."
        )

    else:

        print(
            "[Ingestion Agent] No missing values detected."
        )

    # -----------------------------------------------------
    # 7. Add reporting dimensions
    # -----------------------------------------------------

    df["Year"] = df["Month"].dt.year

    df["Month_Name"] = df["Month"].dt.strftime("%b")

    df["Quarter"] = (
        "Q" +
        df["Month"].dt.quarter.astype(str)
    )

    # -----------------------------------------------------
    # 8. Finance control checks
    # -----------------------------------------------------

    if (df["Revenue_Budget"] <= 0).any():

        print(
            "[Ingestion Agent] Warning: "
            "Non-positive revenue budget detected."
        )

    if (df["Revenue_Actual"] < 0).any():

        print(
            "[Ingestion Agent] Warning: "
            "Negative revenue detected."
        )

    # -----------------------------------------------------
    # Final validation
    # -----------------------------------------------------

    print(
        "[Ingestion Agent] Data validation completed successfully."
    )

    print(
        f"[Ingestion Agent] Final dataset: "
        f"{df.shape[0]} rows x {df.shape[1]} columns."
    )

    return df


# =========================================================
# TEST THE AGENT
# =========================================================

if __name__ == "__main__":

    finance_data = load_data()

    print("\nSample validated financial records:\n")

    print(
        finance_data[
            [
                "Month",
                "Year",
                "Quarter",
                "Region",
                "Business_Unit",
                "Revenue_Actual",
                "Revenue_Budget",
                "EBITDA_Actual"
            ]
        ].head()
    )