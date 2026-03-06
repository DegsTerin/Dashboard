# Dashboard

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Plotly](https://img.shields.io/badge/Charts-Plotly-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/python/)
[![Sponsor](https://img.shields.io/badge/Sponsor-DegsTerin-EA4AAA?logo=githubsponsors&logoColor=white)](https://github.com/sponsors/DegsTerin)

Interactive IT salary dashboard built with Streamlit, Pandas, and Plotly.
It helps explore compensation trends by year, experience level, employment type, company size, remote work ratio, and job title comparisons.

## Live Demo

https://dev-dashboard.streamlit.app/

## Preview

<img width="1917" height="938" alt="Dashboard preview" src="https://github.com/user-attachments/assets/1d42bc76-0ea1-4676-80c9-0c964724a8e3" />

## Highlights

- Explore salary data across multiple years
- Filter by experience level, employment type, and company size
- Compare remote work distribution and top job titles
- Switch display currency between USD and EUR
- View multiple analysis pages in one Streamlit app

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly

## Project Structure

```text
Dashboard/
|-- Data/
|   `-- Salaries.csv
|-- pages/
|   |-- 1_Main_Courts.py
|   |-- 2_Overview.py
|   |-- 3_Work_Mode.py
|   `-- 4_Role_Comparison.py
|-- Home.py
`-- requirements.txt
```

## Run Locally

1. Install Python 3.12 or newer.
2. Clone the repository:

```bash
git clone https://github.com/DegsTerin/Dashboard.git
cd Dashboard
```

3. Create and activate a virtual environment.

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate
```

If execution is blocked:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

4. Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

5. Start the app:

```bash
streamlit run Home.py
```

Open the local URL shown in the terminal, usually `http://localhost:8501`.

## Data Notes

- The application reads salary data from `Data/Salaries.csv`
- The main page also supports loading the dataset from the GitHub raw URL
- EUR values use a fixed conversion rate from USD for display purposes

## Support

If this project helps you, consider supporting ongoing development:

- GitHub Sponsors: `https://github.com/sponsors/DegsTerin`

