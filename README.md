# MCA Insights Engine
## Setup
1. Activate venv: `source venv/bin/activate`
2. Run integration: `python integrate_data.py`
3. Run changes: `python detect_changes.py`
4. Run enrichment: `python enrich_data.py`
5. Dashboard: `streamlit run dashboard.py`

## Architecture
- Data flow: CSVs -> Merge/Clean -> Change Detection -> Enrichment -> Dashboard/Chatbot.
- Enrichment logic: Scrapes ZaubaCorp for sector/directors (proxy; use APIs for scale).

## Workflow
Download CSVs from data.gov.in, simulate snapshots, run scripts sequentially.


## Project Overview
The MCA Insights Engine is a data processing and visualization tool designed to analyze and monitor company data from the Ministry of Corporate Affairs (MCA) in India. It integrates raw company datasets, detects incremental changes, enriches data with publicly available information, generates AI-powered summaries, and provides an interactive dashboard for insights. This project is ideal for business analysts, data scientists, and MCA compliance officers to track company statuses, capital details, and regional trends.

- **Repository**: [https://github.com/rohitvmeshram/mca-insights-engine/tree/main](https://github.com/rohitvmeshram/mca-insights-engine/tree/main)
- **Author**: Rohit Meshram <rohitvmeshram976@gmail.com> 
- **License**: MIT

## Step-by-Step Guide

### Setup
1. **Activate Virtual Environment**
   - Create and activate a virtual environment:
     ```bash
     python -m venv .venv
     source .venv/bin/activate  # On macOS/Linux
     .\venv\Scripts\activate    # On Windows

Run Integration

Consolidate raw CSV data into a master dataset:
bashpython integrate_data.py

Outputs master_dataset.csv in data/.


Run Changes

Detect updates and generate logs/summaries:
bashpython detect_changes.py

Outputs logs (e.g., logs/maharashtra_change_log_day2.csv) and summaries (e.g., summaries/maharashtra_daily_summary_day2.txt).


Run Enrichment

Enhance dataset with web data:
bashpython enrich_data.py

Outputs enriched_dataset.csv in enriched/.


Launch Dashboard

Start the Streamlit dashboard:
bashstreamlit run dashboard.py

Access at http://localhost:8501.



Architecture

Data Flow: CSVs -> Merge/Clean -> Change Detection -> Enrichment -> Dashboard/Chatbot.
Enrichment Logic: Scrapes ZaubaCorp for sector/directors using a proxy (use APIs for scale).

Workflow

Download CSVs: Get raw data from data.gov.in or simulate snapshots with changes.
Simulate Snapshots: Create/update CSVs (e.g., maharashtra_day1.csv, maharashtra_day2.csv) in data/.
Run Scripts Sequentially: Execute integrate_data.py, detect_changes.py, enrich_data.py, then dashboard.py.

Documentation

Scripts: integrate_data.py, detect_changes.py, enrich_data.py, dashboard.py.
Data Files: data/master_dataset.csv, logs/*.csv, enriched/enriched_dataset.csv, summaries/*.txt.
Dependencies: Install with pip install -r requirements.txt or pip install streamlit pandas langchain==0.2.5 langchain-core==0.2.10 langchain-openai==0.1.7 langchain-experimental==0.0.62 pydantic==1.10.15 tabulate.
