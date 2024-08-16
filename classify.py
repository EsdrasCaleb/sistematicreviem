import pandas as pd

# Load your dataset
df = pd.read_csv('results/classified.csv')  # Replace with your file path


# Define a function to calculate the score
def calculate_score(row):
    score = 0

    # Score for Abstract Game Score
    if row['Abstract Game Score'] > 0.9:
        score += 6
    elif row['Abstract Game Score'] > 0.5:
        score += 5

    if row['Title Game Score'] > 0.5:
        score += 5

    # Score for Year
    if row['Year'] > 2014:
        score += 1

    # Score for Keywords
    keywords = str(row['Keywords']).lower()
    if 'game' in keywords:
        score += 5
    if 'smell' in keywords:
        score += 1

    # Score for Citations
    citations = row['Number of Citations']
    if citations > 10:
        score += 1

    return score


# Apply the function to each row to create the new Score column
df['Score'] = df.apply(calculate_score, axis=1)
df_filtered = df[df['Score'] >= 5]
# Sort the DataFrame by the Score column in descending order
df_sorted = df_filtered.sort_values(by='Score', ascending=False)

# Save the sorted DataFrame to a new CSV file
df_sorted.to_csv('results/filtered_classified.csv', index=False)
df_filtered = df[df['Score'] < 5]
df_sorted = df_filtered.sort_values(by='Score', ascending=False)
df_sorted.to_csv('results/cuted_classified.csv', index=False)