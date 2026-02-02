# ===============================
# 1_Main_Courts.py
# ===============================

import streamlit as st
import pandas as pd
import plotly.express as px

# ===============================
# GLOBAL VISUAL CONFIGURATION
# ===============================
st.set_page_config(
    page_title="Advanced Data Salary Analysis",
    page_icon="📊",
    layout="wide",
)

PALETTE = px.colors.qualitative.Set2
px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = PALETTE

# ===============================
# Data Loading
# ===============================

# Clear cache when switching data source manually
st.cache_data.clear()

@st.cache_data
def load_data():
    # URL (production / GitHub)
    return pd.read_csv(
        "https://raw.githubusercontent.com/DegsTerin/Dashboard/refs/heads/main/Data/Salaries.csv"
    )

    # LOCAL (uncomment for local testing)
    #return pd.read_csv("Data/Salaries.csv")

df = load_data()

# ===============================
# DATA VALIDATION
# ===============================
REQUIRED_COLUMNS = {
    "Year", "Experience_Level", "Employment_Type", "Company_Size",
    "Salary_In_Usd", "Job_Title", "Remote_Ratio", "Employee_Residence_Iso3"
}

if not REQUIRED_COLUMNS.issubset(df.columns):
    st.error("Invalid or incomplete dataset. Missing required columns.")
    st.stop()

# ===============================
# SIDEBAR
# ===============================
st.sidebar.header("🔍 Filters")

currency = st.sidebar.radio("Currency", ["USD", "EUR"], horizontal=True)

years = st.sidebar.multiselect("Year", sorted(df["Year"].unique()), default=sorted(df["Year"].unique()))
experience_levels = st.sidebar.multiselect("Experience Level", sorted(df["Experience_Level"].unique()), default=sorted(df["Experience_Level"].unique()))
employment_types = st.sidebar.multiselect("Employment Type", sorted(df["Employment_Type"].unique()), default=sorted(df["Employment_Type"].unique()))
company_sizes = st.sidebar.multiselect("Company Size", sorted(df["Company_Size"].unique()), default=sorted(df["Company_Size"].unique()))

# ===============================
# FILTER WITH CACHE
# ===============================
@st.cache_data
def filter_data(df, years, experience_levels, employment_types, company_sizes):
    return df[
        df["Year"].isin(years) &
        df["Experience_Level"].isin(experience_levels) &
        df["Employment_Type"].isin(employment_types) &
        df["Company_Size"].isin(company_sizes)
    ]

df_filtered = filter_data(df, years, experience_levels, employment_types, company_sizes)

# Simple USD \u2192 EUR conversion (fixed, intentional)
EXCHANGE_RATE_EUR = 0.92
df_filtered["Display_Salary"] = df_filtered["Salary_In_Usd"] if currency == "USD" else df_filtered["Salary_In_Usd"] * EXCHANGE_RATE_EUR

# Determine the currency symbol
currency_symbol = "$" if currency == "USD" else "€"

# ===============================
# TITLE
# ===============================
st.title("📊 Advanced Data Salary Analysis")
st.markdown("An interactive dashboard geared towards **decision-making**, not just visualisation.")

# ===============================
# KPIs
# ===============================
st.subheader("Key Performance Indicators")

if df_filtered.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Average Salary", f"{currency_symbol}{df_filtered['Display_Salary'].mean():,.0f}")
c2.metric("Median Salary", f"{currency_symbol}{df_filtered['Display_Salary'].median():,.0f}")
c3.metric("Maximum Salary", f"{currency_symbol}{df_filtered['Display_Salary'].max():,.0f}")
c4.metric("Records", len(df_filtered))

st.divider()

# ===============================
# SALARY EVOLUTION OVER TIME (NEW)
# ===============================
st.subheader("📈 Salary Evolution Over Time")

salary_evolution = df_filtered.groupby("Year")["Display_Salary"].mean().reset_index()

fig = px.line(
    salary_evolution,
    x="Year",
    y="Display_Salary",
    markers=True,
    title="Average Salary by Year",
    labels={"Display_Salary": f"Average Salary ({currency})", "Year": ""}
)
fig.update_traces(
    hovertemplate=f"Year: %{{x}}<br>Average Salary: {currency_symbol}%{{y:,.0f}}<extra></extra>"
)
st.plotly_chart(fig, use_container_width=True)

# ===============================
# TOP JOB TITLES
# ===============================
st.subheader("🏆 Highest Paid Job Titles")

top_job_titles = (
    df_filtered.groupby("Job_Title", as_index=False)["Display_Salary"]
    .mean()
    .nlargest(10, "Display_Salary")
    .sort_values("Display_Salary")
)

fig = px.bar(
    top_job_titles,
    x="Display_Salary",
    y="Job_Title",
    orientation="h",
    title="Top 10 Job Titles by Average Salary",
    labels={"Display_Salary": f"Average Salary ({currency})", "Job_Title": ""}
)

fig.update_traces(
    hovertemplate=f"Average salary: {currency_symbol}%{{x:,.0f}}<extra></extra>"
)
st.plotly_chart(fig, use_container_width=True)

# ===============================
# EXPERIENCE LEVEL x COMPANY SIZE HEATMAP (NEW)
# ===============================
st.subheader("🔥 Experience Level vs. Company Size")

heatmap_data = (
    df_filtered.groupby(["Experience_Level", "Company_Size"])["Display_Salary"]
    .mean()
    .reset_index()
)

fig = px.density_heatmap(
    heatmap_data,
    x="Company_Size",
    y="Experience_Level",
    z="Display_Salary",
    color_continuous_scale="Blues",
    title="Average Salary by Experience Level and Company Size"
)

st.plotly_chart(fig, use_container_width=True)

# ===============================
# JOB TITLE COMPARISON (IMPROVED)
# ===============================
st.subheader("⚖️ Job Title Comparison")

job_title_a_col, job_title_b_col = st.columns(2)
job_title_a = job_title_a_col.selectbox("Job Title A", sorted(df["Job_Title"].unique()))
job_title_b = job_title_b_col.selectbox("Job Title B", sorted(df["Job_Title"].unique()), index=1)

comparison = (
    df_filtered[df_filtered["Job_Title"].isin([job_title_a, job_title_b])]
    .groupby("Job_Title")["Display_Salary"]
    .agg(average="mean", median="median")
    .reset_index()
)

fig = px.bar(
    comparison,
    x="Job_Title",
    y=["average", "median"],
    barmode="group",
    title="Salary Comparison (Average vs. Median)",
    labels={"value": f"Salary ({currency})", "variable": "Metric"}
)

fig.update_traces(
    hovertemplate=f"Salary: {currency_symbol}%{{y:,.0f}}<extra></extra>"
)

st.plotly_chart(fig, use_container_width=True)

# Ensure comparison has at least two rows before calculating delta
if len(comparison) >= 2:
    delta = (comparison.loc[1, "average"] / comparison.loc[0, "average"] - 1) * 100
    st.info(f"{job_title_b} typically pays **{delta:.1f}%** more than {job_title_a} on average.")
else:
    st.info(f"Not enough data to compare {job_title_a} and {job_title_b}.")


# ===============================
# COUNTRY RANKING (NEW)
# ===============================
st.subheader("🌍 Countries with Highest Average Salaries")

country_ranking = (
    df_filtered.groupby("Employee_Residence_Iso3")["Display_Salary"]
    .mean()
    .nlargest(10)
    .reset_index()
)

fig = px.bar(
    country_ranking,
    x="Display_Salary",
    y="Employee_Residence_Iso3",
    orientation="h",
    title="Top 10 Countries by Average Salary",
    labels={"Display_Salary": f"Average Salary ({currency})", "Employee_Residence_Iso3": "Country"}
)

st.plotly_chart(fig, use_container_width=True)

# ===============================
# TABLE
# ===============================
st.subheader("📋 Detailed Data")
st.dataframe(df_filtered, use_container_width=True)

# ===============================
# Data Download
# ===============================
st.sidebar.download_button(
    "📥 Download Filtered Data",
    data=df_filtered.to_csv(index=False),
    file_name="filtered_data.csv",
    mime="text/csv"
)

# ===============================
# ABOUT
# ===============================
with st.expander("ℹ️ About the Dashboard", expanded=True):
    st.markdown("""
    - Data Source: Kaggle / GitHub
    - Values expressed in annual USD
    - Outliers removed at the 99th percentile for visualization only
    - Comparisons based on average and median
    """)