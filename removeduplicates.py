import pandas as pd
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

def detect_language(text):
    try:
        # Check if the text is a string
        if isinstance(text, str) and text.strip():
            return detect(text)
        else:
            return 'unknown'
    except:
        return 'unknown'
# Load the two CSV files
df1 = pd.read_csv('resultbitex.csv')
df2 = pd.read_csv('scholar_results.csv')
df1['Title_lower'] = df1['Title'].str.lower()
df2['Title_lower'] = df2['Title'].str.lower()

# Step 1: Filter out papers in df2 that have titles present in df1
df2_filtered = df2[~df2['Title_lower'].isin(df1['Title_lower'])]

# Step 2: Combine the two DataFrames, filling in missing data in df1 with data from df2
combined_df = pd.concat([df1, df2], ignore_index=True)

# Ensure all columns are present in the combined DataFrame
for column in df2.columns:
    if column not in combined_df.columns:
        combined_df[column] = None

# Fill missing values in df1 with corresponding values from df2
combined_df = combined_df.groupby('Title_lower', as_index=False).first()

mask_doi = combined_df['DOI'].notnull()
mask_link = combined_df['Link'].notnull()

df_doi = combined_df[mask_doi].drop_duplicates(subset='DOI', keep='first')

df_link = combined_df[~mask_doi & mask_link].drop_duplicates(subset='Link', keep='first')
final_df = pd.concat([df_doi, df_link], ignore_index=True)
# Detect language where 'Language' is missing
def detect_language_from_abstract_or_title(row):
    if pd.isnull(row['Language']):
        if pd.isnull(row['Abstract']):
            return detect_language(row['Title'])
        else:
            return detect_language(row['Abstract'])
    return row['Language']

# Detect language for rows where 'Language' is missing
combined_df['Language'] = combined_df.apply(detect_language_from_abstract_or_title, axis=1)

# Save the cleaned data to a new CSV file
final_df.to_csv('resultsnew/noduplicates.csv', index=False)

print("Duplicates removed and data saved to 'cleaned_data.csv'.")
