import pandas as pd
import requests
from io import StringIO

# UNSPSC dataset URL (redirects to S3)  can always change this link if it becomes outdated or broken
url = "https://data.ok.gov/dataset/18a622a6-32d1-48f6-842a-8232bc4ca06c/resource/b92ad3ac-b0f5-4c62-9bd0-eac023cfd083/download/data-unspsc-codes.csv"

# This just pretends to be a Real Internet User so it can download the dataset from google
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

# Check for success
if response.status_code == 200:
    # Load CSV content into pandas
    df = pd.read_csv(StringIO(response.text))
    
    print("Original UNSPSC dataset columns:")
    print(df.columns.tolist())

    # Rename if needed 
    #(this is just default naming system that the dataset uses can be found on the data.gov website)
    df_cleaned = df.rename(columns={
        'Segment': 'Segment Code',
        'Segment Title': 'Segment Name',
        'Family': 'Family Code',
        'Family Title': 'Family Name',
        'Class': 'Class Code',
        'Class Title': 'Class Name',
        'Commodity': 'Commodity Code',
        'Commodity Title': 'Commodity Name',
        'Commodity Definition': 'Description'
    })

    df_cleaned = df_cleaned.dropna(subset=['Segment Code', 'Segment Name'])

    # Save locally
    # Will Create a New .CVS document in the same folder that the Python file is saved in
    df_cleaned.to_csv("clean_unspsc_data.csv", index=False)
    print("Cleaned dataset preview:")
    print(df_cleaned.head())
else:
    print(f"❌ Failed to fetch dataset. Status code: {response.status_code}")