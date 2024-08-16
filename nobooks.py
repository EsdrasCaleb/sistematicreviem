import pandas as pd

# Load your dataset
df = pd.read_csv('results/onlyenglsih.csv')  # Replace with your file path

# Filter out rows where the 'Link' column contains 'books.google.com'
df_filtered = df[~df['Link'].str.contains('books.google.com', na=False)]

# Save the filtered DataFrame to a new CSV file
df_filtered.to_csv('results/onlyenglsih_nobooks.csv')  # Replace with your file path

print(f"Original dataset had {len(df)} rows.")
print(f"Filtered dataset has {len(df_filtered)} rows.")
