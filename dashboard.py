import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI

st.title("MCA Insights Dashboard")

# Load and map master dataset
master_df = pd.read_csv('master_dataset.csv', low_memory=False)

# Map columns if they exist under different names
column_map = {
    'CIN': 'CIN',
    'CompanyName': 'COMPANY_NAME',
    'CompanyRegistrationdate_date': 'DATE_OF_INCORPORATION',
    'AuthorizedCapital': 'AUTHORIZED_CAPITAL',
    'PaidupCapital': 'PAIDUP_CAPITAL',
    'CompanyStatus': 'COMPANY_STATUS',
    'nic_code': 'PRINCIPAL_BUSINESS_ACTIVITY',
    'Registered_Office_Address': 'REGISTERED_OFFICE_ADDRESS',
    'CompanyROCcode': 'ROC_CODE',
    'CompanyStateCode': 'STATE'
}
master_df = master_df.rename(columns={k: v for k, v in column_map.items() if k in master_df.columns})

# Ensure required columns exist, use fallback if missing
for col in ['DATE_OF_INCORPORATION', 'COMPANY_NAME', 'COMPANY_STATUS', 'STATE', 'AUTHORIZED_CAPITAL', 'PRINCIPAL_BUSINESS_ACTIVITY']:
    if col not in master_df.columns:
        master_df[col] = 'Unknown'
        print(f"Warning: {col} not found, using 'Unknown'")

# Search functionality
search_term = st.text_input("Search by CIN or Company Name")
if search_term:
    results = master_df[master_df['CIN'].str.contains(search_term, case=False, na=False) | 
                        master_df['COMPANY_NAME'].str.contains(search_term, case=False, na=False)]
    st.dataframe(results)

# Filters
year_options = master_df['DATE_OF_INCORPORATION'].str[:4].unique()
state_options = master_df['STATE'].unique()
status_options = master_df['COMPANY_STATUS'].unique()

year = st.selectbox("Filter by Year", year_options)
state = st.selectbox("Filter by State", state_options)
status = st.selectbox("Filter by Status", status_options)

filtered = master_df[(master_df['DATE_OF_INCORPORATION'].str[:4] == year) & 
                     (master_df['STATE'] == state) & 
                     (master_df['COMPANY_STATUS'] == status)]
st.dataframe(filtered)

# Change History Visualization
st.subheader("Change History")
change_logs = []
states = ['maharashtra', 'gujarat', 'delhi', 'tamil_nadu', 'karnataka']
for state in states:
    for day in ['day2', 'day3']:
        log_file = f'logs/{state}_change_log_{day}.csv'
        if os.path.exists(log_file):
            change_logs.append(pd.read_csv(log_file, low_memory=False))
if change_logs:
    all_changes = pd.concat(change_logs, ignore_index=True)
    st.bar_chart(all_changes['Change_Type'].value_counts())
else:
    st.write("No change logs available.")

# Display Enriched Data
st.subheader("Enriched Data")
enriched_file = 'enriched/enriched_dataset.csv'
if os.path.exists(enriched_file):
    enriched_df = pd.read_csv(enriched_file, low_memory=False)
    st.dataframe(enriched_df)
else:
    st.write("No enriched data available.")

# Display AI Summaries
st.subheader("Daily AI Summaries")
for state in states:
    for day in ['day2', 'day3']:
        summary_file = f'summaries/{state}_daily_summary_{day}.txt'
        if os.path.exists(summary_file):
            with open(summary_file, 'r') as f:
                st.text(f"{state.capitalize()} {day.capitalize()} Summary:\n{f.read()}")

# Conversational Chatbot (Rule-Based)
st.subheader("Chat with MCA Data (Rule-Based)")
query = st.text_input("Ask a question (e.g., 'Show new incorporations in Maharashtra')")

if query:
    # Rule for "Show new incorporations in Maharashtra."
    if 'new incorporations' in query.lower() and 'maharashtra' in query.lower():
        results = master_df[(master_df['STATE'] == 'Maharashtra') & (master_df['DATE_OF_INCORPORATION'] > '2023-01-01')]
        st.dataframe(results)
    # Rule for "List all companies in the manufacturing sector with authorized capital above Rs.10 lakh."
    elif 'manufacturing' in query.lower() and 'above' in query.lower():
        results = master_df[(master_df['PRINCIPAL_BUSINESS_ACTIVITY'].str.contains('manufacturing', case=False, na=False)) & 
                            (master_df['AUTHORIZED_CAPITAL'] > 1000000)]
        st.dataframe(results)
    # Rule for "How many companies were struck off last month?"
    elif 'struck off' in query.lower():
        struck_off = 0
        for state in states:
            for day in ['day2', 'day3']:
                log_file = f'logs/{state}_change_log_{day}.csv'
                if os.path.exists(log_file):
                    changes = pd.read_csv(log_file, low_memory=False)
                    struck_off += len(changes[changes['Change_Type'] == 'Deregistered'])
        st.write(f"Companies struck off: {struck_off}")
    else:
        st.write("Query not understood. Try examples from the PDF.")

# Advanced RAG Chatbot
st.subheader("Chat with MCA Data (Advanced RAG with LLM)")
query_rag = st.text_input("Ask an advanced question (e.g., 'Summarize companies in Delhi with capital over 5 crore')")

if query_rag:
    # Load environment variables for API key
    load_dotenv()
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    # Create Pandas DataFrame agent
    agent = create_pandas_dataframe_agent(
        llm,
        master_df,
        agent_type="openai-tools",
        verbose=True,
        allow_dangerous_code=True,
        prefix="You are querying MCA company data. Answer in natural language with tables if needed."
    )
    # Run query
    try:
        response = agent.invoke(query_rag)
        st.write("AI Response:")
        st.write(response['output'])
    except Exception as e:
        st.write(f"Error: {str(e)}. Check API key or rephrase query.")