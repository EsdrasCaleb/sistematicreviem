import pandas as pd
from langdetect import detect

def detect_language(text):
    """Detect the language of the given text."""
    try:
        return detect(text)
    except:
        return 'unknown'

# Load the combined CSV file
df = pd.read_csv('resultsnew/noduplicates.csv')

# Step 1: Filter out rows with null abstracts
df['Detected_Language'] = df['Title'].apply(lambda x: detect_language(x) if pd.notnull(x) else 'unknown')
df['Detected_Language_Abstract'] = df['Abstract'].apply(lambda x: detect_language(x) if pd.notnull(x) else 'unknown')
# Define the allowed languages (using language codes)
allowed_languages = ['en']

# Step 3: Filter the DataFrame based on the detected language
filtered_df = df[
    df['Detected_Language_Abstract'].str.lower().isin(allowed_languages) &
    df['Abstract'].notnull()
]

filtered_df2 = filtered_df[
    filtered_df['Detected_Language'].str.lower().isin(allowed_languages)
]
# Save the filtered data to a new CSV file
filtered_df2.to_csv('resultsnew/filterlanguage_all.csv', index=False)

print("Filtered data saved to 'filtered_results.csv'.")
