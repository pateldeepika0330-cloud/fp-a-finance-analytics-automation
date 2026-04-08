import streamlit as st
import matplotlib.pyplot as plt
from main import run_pipeline

st.set_page_config(layout="wide")

st.title("FP&A Agentic AI Dashboard")

file = st.file_uploader("Upload Excel", type=["xlsx"])

if file:
    df, cc, ai = run_pipeline(file)

    st.subheader("Data")
    st.dataframe(df.head())

    st.subheader("Forecast")
    fig, ax = plt.subplots()
    ax.plot(df['Revenue_Actual'])
    ax.plot(df['Forecast_Revenue'])
    st.pyplot(fig)

    st.subheader("Variance")
    st.dataframe(df[['Revenue_Var_%','Cost_Var_%']].head())

    st.subheader("Cost Center")
    st.dataframe(cc)

    st.subheader("AI Insights")
    st.success(ai)