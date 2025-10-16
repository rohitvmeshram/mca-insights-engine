import pandas as pd
import os

# List of states and their CSV files (assume downloaded)
states = ['maharashtra', 'gujarat', 'delhi', 'tamil_nadu', 'karnataka']
data_dir = 'data/'

def integrate_data():
    dfs = []
    for state in states:
        file_path = os.path.join(data_dir, f'{state}.csv')
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            df['STATE'] = state.capitalize()  # Add state column for tracking
            dfs.append(df)
        else:
            print(f"Warning: {file_path} not found.")

    # Merge into master
    master_df = pd.concat(dfs, ignore_index=True)

    # Standardize columns (assuming common columns like CIN, COMPANY_NAME, etc.)
    columns = ['CIN', 'COMPANY_NAME', 'DATE_OF_INCORPORATION', 'AUTHORIZED_CAPITAL', 
               'PAIDUP_CAPITAL', 'COMPANY_STATUS', 'PRINCIPAL_BUSINESS_ACTIVITY', 
               'REGISTERED_OFFICE_ADDRESS', 'ROC_CODE', 'STATE']
    master_df = master_df.reindex(columns=columns, fill_value=pd.NA)

    # Clean: Handle nulls, remove duplicates by CIN
    master_df.fillna('Unknown', inplace=True)
    master_df.drop_duplicates(subset=['CIN'], keep='last', inplace=True)

    # Save canonical master
    master_df.to_csv('master_dataset.csv', index=False)
    print("Master dataset created.")

if __name__ == "__main__":
    integrate_data()