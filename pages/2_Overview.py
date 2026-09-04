# ===============================
# 2_Overview.py
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
    page_title="Salary Overview",
    page_icon="📊",
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
st.title("📊 Salary Overview")
st.markdown("An interactive dashboard geared towards **decision-making**, not just visualisation.")

# ===============================
# KPIs
# ===============================
st.subheader("Key Performance Indicators")

if df_filtered.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

c1, c2, c3 = st.columns(3)

c1.metric("Average Salary", f"{currency_symbol}{df_filtered['Display_Salary'].mean():,.0f}")
c2.metric("Median Salary", f"{currency_symbol}{df_filtered['Display_Salary'].median():,.0f}")
c3.metric("Records", len(df_filtered))

# ===============================
# SALARY DISTRIBUTION
# ===============================
st.subheader("Salary Distribution")

fig = px.histogram(
    df_filtered,
    x="Display_Salary",
    nbins=40,
    title="Salary Distribution",
    labels={"Display_Salary": f"Annual Salary ({currency})"}
)
fig.update_traces(
    hovertemplate=f"Annual Salary: {currency_symbol}%{{x:,.0f}}<extra></extra>"
)
st.plotly_chart(fig, use_container_width=True)

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
