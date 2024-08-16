import pandas as pd
from langdetect import detect

def detect_language(text):
    """Detect the language of the given text."""
    try:
        return detect(text)
    except:
        return 'unknown'

# Load the combined CSV file
df = pd.read_csv('results/noduplicates.csv')

df_filtered = df[df['Language'].str.lower().isin(['en', 'english'])]
df_removed = df[~df['Language'].str.lower().isin(['en', 'english'])]

df_filtered.to_csv('results/onlyenglsih.csv', index=False)
df_removed.to_csv('results/removedbylanguage.csv', index=False)
print("Filtered data saved in results to 'removedbylanguage.csv' 'onlyenglsih.csv'.")
