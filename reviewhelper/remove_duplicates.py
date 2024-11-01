import pandas as pd
import numpy as np

def merge_rows(row_group):
    merged_row = {}
    for column in row_group.columns:
        if column == 'keywords':
            # Split keywords into individual items, remove duplicates, and join them back as a string
            all_keywords = row_group[column].dropna().str.split(',').sum()  # Flatten lists of keywords
            unique_keywords = list(set(map(str.strip, all_keywords)))  # Remove duplicates and strip whitespace
            merged_row[column] = ', '.join(unique_keywords)
        else:
            # Normalize values to lowercase for case-insensitive uniqueness
            merged_value = row_group[column].dropna().str.lower().unique()

            # Revert to original case when possible
            original_values = row_group[column].dropna().unique()
            merged_values_dict = dict(zip(merged_value, original_values))
            merged_unique_values = [merged_values_dict[val] for val in merged_value]

            # If the column is 'file_name', merge all values with commas
            if column == 'file_name':
                merged_row[column] = ', '.join(merged_unique_values)
            elif column == 'doi':
                merged_row[column] = ', '.join(merged_unique_values)
            else:
                # Use the first non-null value, if available
                merged_row[column] = next((val for val in merged_unique_values if pd.notna(val)), None)

    return pd.Series(merged_row)

def remove_duplicates(data_frame, column):
    # Check if the specified column exists in the DataFrame
    if column not in data_frame.columns:
        raise ValueError(f"The specified column '{column}' does not exist in the DataFrame.")

    # Treat empty strings as null values, avoiding in-place modification
    data_frame = data_frame.copy()
    data_frame[column] = data_frame[column].replace('', np.nan)

    # Separate rows where the specified column is null (now includes empty strings)
    null_rows = data_frame[data_frame[column].isnull()]
    non_null_rows = data_frame[data_frame[column].notnull()].copy()

    # Normalize the specified column for case-insensitive deduplication
    non_null_rows['normalized_column'] = non_null_rows[column].str.lower()

    # Deduplicate based on the normalized column
    deduped_df = non_null_rows.groupby('normalized_column', as_index=False).apply(merge_rows)

    # Drop the temporary normalized column used for deduplication
    deduped_df = deduped_df.drop(columns=['normalized_column'])

    # Concatenate the deduplicated non-null rows with the original null rows
    final_df = pd.concat([deduped_df, null_rows], ignore_index=True)

    return final_df
