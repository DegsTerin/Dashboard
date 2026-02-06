# Dashboard

Interactive IT salary dashboard providing detailed analysis of compensation by year, experience level, employment type, and company size. 
Values can be displayed in USD or converted to EUR (fixed rate 0.92). 
Features graphical visualisations of salary distribution, top job titles, remote work proportion, and job title comparisons. 
Supports dynamic filtering, data download, and automatic insights on salary trends. 
Data sourced from public repositories (Kaggle / GitHub), with outliers handled for visualisation purposes. 
The dashboard contains multiple pages with different analyses and metrics.


https://dev-dashboard.streamlit.app/

<img width="1917" height="938" alt="image" src="https://github.com/user-attachments/assets/1d42bc76-0ea1-4676-80c9-0c964724a8e3" />



Complete setup guide (Windows or macOS) — Python 3.12 + Streamlit
1) Install Python 3.12

Windows

Download: https://www.python.org/downloads/latest/python3.12/

Download Python 3.12.

Run the installer, tick Add Python to PATH, then click Install Now.

Check in Command Prompt or PowerShell:

python --version


Expected: Python 3.12.x
If it doesn’t appear, you likely didn’t tick PATH. Reinstall Python and tick it.

macOS

Download: https://www.python.org/ftp/python/3.12.10/python-3.12.10-macos11.pkg

Open the .pkg and follow the installer (Continue → Install).

Check in Terminal:

python3 --version


Expected: Python 3.12.x
If it doesn’t appear, Python wasn’t installed correctly.

2) Install Git

Windows

Download: https://git-scm.com/download/win

Run the installer and follow the defaults (Next → Next → Finish).

Check:

git --version


Expected: git version 2.xx.x
If it doesn’t appear, reinstall Git.

macOS

Install instructions: https://git-scm.com/install/mac

Follow the standard installer steps.

Check:

git --version


Expected: git version 2.xx.x
If it doesn’t appear, reinstall Git.

3) Clone the project

Windows / macOS

git clone https://github.com/DegsTerin/Dashboard.git

cd Dashboard

4) Create and activate a virtual environment

Windows (Command Prompt / PowerShell)

python -m venv .venv
.venv\Scripts\Activate


If PowerShell blocks activation:

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned


macOS (Terminal)

python3 -m venv .venv
source .venv/bin/activate

5) Upgrade pip

Windows / macOS

python -m pip install --upgrade pip

6) Install dependencies

Windows / macOS

pip install -r requirements.txt

7) Run Streamlit

Windows / macOS

streamlit run app.py


Open the link shown in the terminal (usually http://localhost:8501).
