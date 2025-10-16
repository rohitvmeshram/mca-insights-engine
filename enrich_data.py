import pandas as pd
import requests
from bs4 import BeautifulSoup

def enrich_cin(cin):
    url = f"https://www.zaubacorp.com/company/{cin}"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Proxy extraction (adapt based on page structure)
        sector = soup.find(text='Industry') or 'Unknown'
        directors = soup.find(text='Directors') or 'Unknown'
        address = soup.find(text='Address') or 'Unknown'
        return {'SECTOR': sector, 'DIRECTORS': directors, 'ADDRESS': address, 'SOURCE': 'ZaubaCorp', 'SOURCE_URL': url}
    except:
        return {'SECTOR': 'Error', 'DIRECTORS': 'Error', 'ADDRESS': 'Error', 'SOURCE': 'ZaubaCorp', 'SOURCE_URL': url}

if __name__ == "__main__":
    changes = pd.read_csv('logs/change_log_day2.csv')  # Sample changes
    sample_cins = changes['CIN'].unique()[:50]  # Limit to 50
    enriched = []
    for cin in sample_cins:
        data = enrich_cin(cin)
        enriched.append({'CIN': cin, 'COMPANY_NAME': 'Placeholder', 'STATE': 'Placeholder', 'STATUS': 'Placeholder', **data})
    
    enriched_df = pd.DataFrame(enriched)
    enriched_df.to_csv('enriched/enriched_dataset.csv', index=False)
    print("Enriched dataset created.")