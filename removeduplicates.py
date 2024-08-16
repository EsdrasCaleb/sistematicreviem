import pandas as pd
from langdetect import detect

def detect_language(text):
    try:
        # Check if the text is a string
        if isinstance(text, str) and text.strip():
            return detect(text)
        else:
            return 'unknown'
    except:
        return 'unknown'
def merge_rows(row_group):
    merged_row = {}
    for column in row_group.columns:
        # Merge non-empty values from duplicates
        merged_value = row_group[column].dropna().unique()
        if len(merged_value) > 0:
            merged_row[column] = ', '.join(map(str, merged_value))
        else:
            merged_row[column] = None
    return pd.Series(merged_row)
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

df_doi = combined_df[mask_doi].groupby(['DOI']).apply(merge_rows).reset_index(drop=True)

df_link = combined_df[~mask_doi & mask_link].groupby(['Link']).apply(merge_rows).reset_index(drop=True)
final_df = pd.concat([df_doi, df_link], ignore_index=True)


# Save the cleaned data to a new CSV file
final_df.to_csv('results/noduplicates.csv', index=False)

print("Duplicates removed and data saved to 'noduplicates.csv'.")
