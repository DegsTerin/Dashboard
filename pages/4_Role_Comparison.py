# ===============================
# 4_Role_Comparison.py
# ===============================

import streamlit as st
import plotly.express as px

from analytics_utils import (
    filter_salary_data,
    load_salary_data,
    validate_dataset,
    with_display_salary,
)

# ===============================
# GLOBAL VISUAL CONFIGURATION
# ===============================
st.set_page_config(
    page_title="Role Salary Comparison",
    page_icon="⚖️",
    layout="wide",
)

PALETTE = px.colors.qualitative.Set2
px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = PALETTE

# ===============================
# Data Loading
# ===============================

df = load_salary_data()

# ===============================
# DATA VALIDATION
# ===============================
missing_columns = validate_dataset(df)
if missing_columns:
    st.error(
        "Invalid or incomplete dataset. Missing required columns: "
        + ", ".join(sorted(missing_columns))
    )
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
df_filtered = filter_salary_data(
    df, years, experience_levels, employment_types, company_sizes
)
df_filtered = with_display_salary(df_filtered, currency)

# Determine the currency symbol
currency_symbol = "$" if currency == "USD" else "€"

# ===============================
# TITLE
# ===============================
st.title("⚖️ Role Salary Comparison Analysis")
st.markdown("An interactive dashboard geared towards **decision-making**, not just visualisation.")

# ===============================
# KPIs
# ===============================
st.subheader("Key Performance Indicators")

if df_filtered.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

c1, c2 = st.columns(2)

c1.metric("Total Records", len(df_filtered))
c2.metric("Average Salary", f"{currency_symbol}{df_filtered['Display_Salary'].mean():,.0f}")

st.divider()

# ===============================
# JOB TITLE COMPARISON
# ===============================
st.subheader("⚖️ Job Title Comparison")

# Use original df for job title selection to ensure all titles are available
job_title_a_col, job_title_b_col = st.columns(2)
job_title_a = job_title_a_col.selectbox("Select first role", sorted(df["Job_Title"].unique()))
job_title_b = job_title_b_col.selectbox("Select second role", sorted(df["Job_Title"].unique()), index=1 if len(df["Job_Title"].unique()) > 1 else 0)

comparison = (
    df_filtered[df_filtered["Job_Title"].isin([job_title_a, job_title_b])]
    .groupby("Job_Title")["Display_Salary"]
    .agg(average="mean", median="median")
    .reset_index()
)

if comparison.empty:
    st.info(f"No data available for comparison with the selected roles and filters.")
else:
    fig = px.bar(
        comparison,
        x="Job_Title",
        y=["average", "median"],
        barmode="group",
        title="Salary Comparison (Average vs. Median)",
        labels={
            "value": f"Annual Salary ({currency})",
            "Job_Title": "Role",
            "variable": "Metric"
        }
    )

    fig.update_traces(
        hovertemplate=f"Salary: {currency_symbol}%{{y:,.0f}}<extra></extra>"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Extra insight
    if len(comparison) == 2:
        avg_a = comparison.loc[comparison["Job_Title"] == job_title_a, "average"].values[0]
        avg_b = comparison.loc[comparison["Job_Title"] == job_title_b, "average"].values[0]

        if avg_b != 0:
            diff = ((avg_a - avg_b) / avg_b) * 100
            st.info(
                f"On average, **{job_title_a}** typically pays "
                f"**{diff:.1f}% {'more' if diff > 0 else 'less'}** than **{job_title_b}**."
            )
        else:
            st.info(f"Cannot compare {job_title_a} and {job_title_b} as {job_title_b} has an average salary of 0.")
    elif len(comparison) == 1:
        st.info(f"Only data for {comparison['Job_Title'].iloc[0]} is available under current filters.")

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
with st.expander("ℹ️ About Interactive Data Analytics", expanded=True):
    st.markdown("""
    - Data Source: Kaggle / GitHub
    - Values expressed in annual USD
    - Outliers removed at the 99th percentile for visualization only
    - Comparisons based on average and median
    """)
