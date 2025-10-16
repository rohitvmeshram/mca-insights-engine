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
 - **Author**: Rohit Meshram <rohitvmeshram@example.com> (replace with your email)
 - **License**: MIT
 
 ## Step-by-Step Guide
 
 1. **Activate Virtual Environment**
    - Create and activate a virtual environment:
      ```bash
      python -m venv .venv
      source .venv/bin/activate  # On macOS/Linux
      .\venv\Scripts\activate    # On Windows
      ```
 
 2. **Install Dependencies**
    - Install required packages:
      ```bash
      pip install -r requirements.txt
      ```
    - Or manually install:
      ```bash
      pip install streamlit pandas langchain==0.2.5 langchain-core==0.2.10 langchain-openai==0.1.7 langchain-experimental==0.0.62 pydantic==1.10.15 tabulate
      ```
 
 3. **Set Up Environment Variables**
    - Create a `.env` file in the root directory:
      ```bash
      echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
      ```
    - Obtain an API key from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys).
 
 4. **Prepare Data**
    - Place raw snapshot CSVs in the `data/` folder:
      ```bash
      cp maharashtra_day1.csv maharashtra_day2.csv data/
      ```
    - Ensure consistent column structure (CIN, COMPANY_NAME, etc.).
 
 5. **Clone the Repository**
    - Download the project:
      ```bash
      git clone https://github.com/rohitvmeshram/mca-insights-engine.git
      cd mca-insights-engine
      ```
 
 6. **Run Integration**
    - Consolidate raw CSV data into a master dataset:
      ```bash
      python integrate_data.py
      ```
    - Outputs `master_dataset.csv` in `data/`.
 
 7. **Run Changes**
    - Detect updates and generate logs/summaries:
      ```bash
      python detect_changes.py
      ```
    - Outputs logs (e.g., `logs/maharashtra_change_log_day2.csv`) and summaries (e.g., `summaries/maharashtra_daily_summary_day2.txt`).
 
 8. **Run Enrichment**
    - Enhance dataset with web data:
      ```bash
      python enrich_data.py
      ```
    - Outputs `enriched_dataset.csv` in `enriched/`.
 
 9. **Launch Dashboard**
    - Start the Streamlit dashboard:
      ```bash
     streamlit run dashboard.py
      ```
    - Access at [http://localhost:8501](http://localhost:8501).
 
 ## Architecture
 
 1. **Define Data Flow**
    - Process data through stages:
      ```bash
      # Data flow: CSVs -> Merge/Clean -> Change Detection -> Enrichment -> Dashboard/Chatbot
      ```
 
 2. **Explain Enrichment Logic**
    - Scrape ZaubaCorp for sector/directors using a proxy:
      ```bash
      # Use proxyscrape.com proxy; consider APIs for scale
      ```
 
 ## Workflow
 
 1. **Download CSVs**
    - Get raw data or simulate snapshots:
      ```bash
      wget https://data.gov.in/api/data -O data/raw_data.csv  # Example
      ```
    - Or create mock files in `data/`.
 
 2. **Simulate Snapshots**
    - Update CSVs with changes:
      ```bash
      echo "CIN,COMPANY_NAME,DATE_OF_INCORPORATION" > data/maharashtra_day1.csv
      echo "U12345,TestCo,2023-01-01" >> data/maharashtra_day1.csv
      ```
 
 3. **Run Scripts Sequentially**
    - Execute in order:
      ```bash
      python integrate_data.py
      python detect_changes.py
      python enrich_data.py
      streamlit run dashboard.py
      ```
 
 ## Documentation
 
 1. **List Scripts**
    - Key files:
      ```bash
      # integrate_data.py, detect_changes.py, enrich_data.py, dashboard.py
      ```
 
 2. **List Data Files**
    - Output files:
      ```bash
      # data/master_dataset.csv, logs/*.csv, enriched/enriched_dataset.csv, summaries/*.txt
      ```
 
 3. **Specify Dependencies**
    - Install requirements:
      ```bash
      pip install -r requirements.txt
      ```
 
 ## Troubleshooting
 
 1. **Handle Quota Error (429)**
    - Check OpenAI billing:
     ```bash
      open https://platform.openai.com/account/billing
     ```
    - Disable RAG in `dashboard.py`.
 
 2. **Fix Missing Modules**
    - Install missing package:
      ```bash
      pip install tabulate
      ```
 
 3. **Resolve Data Issues**
    - Verify CSV presence:
      ```bash
      ls data/  # On macOS/Linux
      dir data/ # On Windows
      ```
 
 ## Contributing
 
 1. **Fork Repository**
    - Create your copy:
      ```bash
     git fork https://github.com/rohitvmeshram/mca-insights-engine
      ```
 
 2. **Create Branch**
    - Start a new feature:
      ```bash
      git checkout -b feature-branch
      ```
 
 3. **Commit Changes**
    - Save your work:
      ```bash
      git commit -m "Add feature"
      ```
 
 4. **Submit Pull Request**
    - Push and request review:
      ```bash
      git push origin feature-branch
      ```
 
 ## License
 
 1. **Apply License**
    - Use MIT License:
     ```bash
      echo "MIT License" > LICENSE
      ```
 
 ## Acknowledgments
 
 1. **Credit Inspiration**
    - Acknowledge MCA needs:
      ```bash
      # Inspired by MCA data analysis requirements
      ```
 
 2. **Thank Communities**
    - Recognize tools:
      ```bash
      # Thanks to Streamlit, LangChain, and Pandas communities
      ```
