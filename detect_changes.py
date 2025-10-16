import pandas as pd
import os
from datetime import datetime
import json

def detect_changes(prev_file, current_file, log_file):
    # Load data with low_memory=False to avoid DtypeWarnings
    prev_df = pd.read_csv(prev_file, low_memory=False)
    current_df = pd.read_csv(current_file, low_memory=False)
    
    # Try to identify the correct merge key (e.g., CIN or variants)
    possible_keys = ['CIN', 'CORPORATE_IDENTIFICATION_NUMBER', 'COMPANY_ID']
    merge_key = None
    for key in possible_keys:
        if key in prev_df.columns and key in current_df.columns:
            merge_key = key
            print(f"Using {merge_key} as merge key.")
            break
    
    if merge_key is None:
        print(f"Error: No valid merge key found in {prev_file} or {current_file}. Skipping merge.")
        return
    
    # Merge DataFrames on the identified key
    merged = pd.merge(prev_df, current_df, on=merge_key, suffixes=('_old', '_new'), how='outer', indicator=True)
    
    changes = []
    for _, row in merged.iterrows():
        cin = row[merge_key]
        if row['_merge'] == 'right_only':  # New incorporation (only in current)
            changes.append({'CIN': cin, 'Change_Type': 'New Incorporation', 'Field_Changed': '', 'Old_Value': '', 'New_Value': '', 'Date': datetime.now().date()})
        elif row['_merge'] == 'left_only':  # Deregistered (only in previous)
            changes.append({'CIN': cin, 'Change_Type': 'Deregistered', 'Field_Changed': '', 'Old_Value': '', 'New_Value': '', 'Date': datetime.now().date()})
        else:  # Both: Check for field updates
            fields = ['COMPANY_STATUS', 'AUTHORIZED_CAPITAL', 'PAIDUP_CAPITAL']
            for field in fields:
                old_val = row.get(f'{field}_old')  # Safe get
                new_val = row.get(f'{field}_new')
                if pd.notna(old_val) and pd.notna(new_val) and old_val != new_val:  # Check for NaN and differences
                    changes.append({'CIN': cin, 'Change_Type': 'Update', 'Field_Changed': field, 'Old_Value': str(old_val), 'New_Value': str(new_val), 'Date': datetime.now().date()})
    
    # Save log
    change_df = pd.DataFrame(changes)
    if not change_df.empty:
        change_df.to_csv(log_file, index=False)
        print(f"Changes logged to {log_file}")
    else:
        print(f"No changes detected for {log_file}")

def generate_summary(log_file, summary_file):
    if os.path.exists(log_file):
        changes = pd.read_csv(log_file)
        summary = {
            'New Incorporations': len(changes[changes['Change_Type'] == 'New Incorporation']),
            'Deregistered': len(changes[changes['Change_Type'] == 'Deregistered']),
            'Updated Records': len(changes[changes['Change_Type'] == 'Update'])
        }
        # Save as TXT
        with open(summary_file, 'w') as f:
            f.write("Daily Summary\n")
            for k, v in summary.items():
                f.write(f"{k}: {v}\n")
        # Save as JSON
        json_file = summary_file.replace('.txt', '.json')
        with open(json_file, 'w') as f:
            json.dump(summary, f, indent=4)
        print(f"Summary saved to {summary_file} and {json_file}")
    else:
        print(f"Warning: {log_file} not found, skipping summary generation.")

if __name__ == "__main__":
    states = ['maharashtra', 'gujarat', 'delhi', 'tamil_nadu', 'karnataka']
    latest_dfs = []
    for state in states:
        day1 = f'data/{state}_day1.csv'
        day2 = f'data/{state}_day2.csv'
        day3 = f'data/{state}_day3.csv'
        if os.path.exists(day1) and os.path.exists(day2) and os.path.exists(day3):
            detect_changes(day1, day2, f'logs/{state}_change_log_day2.csv')
            generate_summary(f'logs/{state}_change_log_day2.csv', f'summaries/{state}_daily_summary_day2.txt')
            detect_changes(day2, day3, f'logs/{state}_change_log_day3.csv')
            generate_summary(f'logs/{state}_change_log_day3.csv', f'summaries/{state}_daily_summary_day3.txt')
            # Collect the latest data (day 3) for master dataset
            latest_df = pd.read_csv(day3, low_memory=False)
            latest_df['STATE'] = state.capitalize()  # Add state information
            latest_dfs.append(latest_df)
        else:
            print(f"Warning: Missing files for {state}. Skipping {state}.")

    # Update master dataset with latest data from all states
    if latest_dfs:
        master_df = pd.concat(latest_dfs, ignore_index=True)
        # Map columns to expected format before saving
        column_map = {
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
        master_df.to_csv('master_dataset.csv', index=False)
        print("Master dataset updated with latest data from all states.")
    else:
        print("No valid data found to update the master dataset.")