from agents.ingestion_agent import load_data
from agents.forecasting_agent import forecast
from agents.variance_agent import variance
from agents.scenario_agent import scenario
from agents.costcenter_agent import cost_center
from agents.insights_agent import insights

def run_pipeline(file):

    df = load_data(file)

    df = forecast(df)
    df = variance(df)
    df = scenario(df)

    cc = cost_center(df)
    ai = insights(df)

    df.to_excel("output/final_report.xlsx", index=False)

    return df, cc, ai