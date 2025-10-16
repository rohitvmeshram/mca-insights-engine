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
