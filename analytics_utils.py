from pathlib import Path

import pandas as pd
import streamlit as st

REMOTE_DATA_URL = (
    "https://raw.githubusercontent.com/"
    "DegsTerin/Interactive-Data-Analytics/refs/heads/main/Data/Salaries.csv"
)
REQUIRED_COLUMNS = {
    "Year",
    "Experience_Level",
    "Employment_Type",
    "Company_Size",
    "Salary_In_Usd",
    "Job_Title",
    "Remote_Ratio",
    "Employee_Residence_Iso3",
}
EXCHANGE_RATE_EUR = 0.92


@st.cache_data
def load_salary_data(source: str = "auto") -> pd.DataFrame:
    """Load salary dataset from remote source with optional local fallback."""
    local_path = Path(__file__).parent / "Data" / "Salaries.csv"

    if source == "remote":
        return pd.read_csv(REMOTE_DATA_URL)
    if source == "local":
        return pd.read_csv(local_path)

    try:
        return pd.read_csv(REMOTE_DATA_URL)
    except Exception:
        return pd.read_csv(local_path)


@st.cache_data
def filter_salary_data(
    df: pd.DataFrame,
    years: list[int],
    experience_levels: list[str],
    employment_types: list[str],
    company_sizes: list[str],
) -> pd.DataFrame:
    filtered = df[
        df["Year"].isin(years)
        & df["Experience_Level"].isin(experience_levels)
        & df["Employment_Type"].isin(employment_types)
        & df["Company_Size"].isin(company_sizes)
    ]
    return filtered.copy()


def with_display_salary(df: pd.DataFrame, currency: str) -> pd.DataFrame:
    output = df.copy()
    output["Display_Salary"] = (
        output["Salary_In_Usd"]
        if currency == "USD"
        else output["Salary_In_Usd"] * EXCHANGE_RATE_EUR
    )
    return output


def validate_dataset(df: pd.DataFrame) -> set[str]:
    return REQUIRED_COLUMNS.difference(df.columns)
