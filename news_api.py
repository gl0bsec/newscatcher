#%%
import requests
import pandas as pd
# import openpyxl
import json
import os

def fetch_and_save_to_excel(q, from_date, page_size=100):
    url = 'https://api.newscatcherapi.com/v2/search'
    headers = {'x-api-key': 'UAwfLdafFkZewrWSwR6fw7XNUq0bnQPaBgbCxhi_kSM'}
    params = {'q': q, 'from': from_date, 'page_size': page_size, "lang": "en"}
    # Replace slashes in date with underscores
    safe_from_date = from_date.replace('/', '_')
    json_filename = f"{q}_{safe_from_date}_page_size_{page_size}.json"

    if os.path.exists(json_filename):
        print("exists")
        return 

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        with open(json_filename, 'w') as f:
            json.dump(data, f)
        print(f"JSON data saved to {json_filename}")
        
        articles = data.get('articles', [])
        
        if articles:
            df = pd.DataFrame(articles)
            
            # Define the Excel filename based on the query parameters
            excel_filename = f"{q}_{safe_from_date}_page_size_{page_size}.csv"
            
            # Save DataFrame to Excel
            df.csv(excel_filename, index=False)
            print(f"Data saved to {excel_filename}")
        else:
            print("No articles found.")
    else:
        print(f"Failed to fetch data: {response.status_code}")
        print(f"Failed to fetch data: {response.text}")
#%%
# Example usage
search_terms = ["United Nations", "United Nations universal periodic review", "united nations committee against torture", "refugees", "migrants"]
for term in search_terms:
    fetch_and_save_to_excel(q=term, from_date="2023/08/15", page_size=20)
# fetch_and_save_to_excel(q="Apple", from_date="2021/12/15", page_size=100)
