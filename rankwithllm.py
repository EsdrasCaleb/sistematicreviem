import pandas as pd
from transformers import pipeline
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

# Load the model and pipeline from Hugging Face
classifier_soft = pipeline("text-classification", model="mrm8488/distilroberta-finetuned-software")
classier_zero = classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
# Function to classify text
def classify_text(text):
    if(text):
        result = classifier_soft(text)
        label = result[0]['label']
        score = result[0]['score']
        score_eng = classier_zero(text, candidate_labels=["software engineering"])
        return label, score,score_eng
    else:
        return '',0,0

# Function to detect language
def detect_language(text):
    try:
        return detect(text)
    except LangDetectException:
        return None

# Load the dataset
df = pd.read_csv('scholar_results.csv')

# Filter by language (English, Portuguese, Spanish)
df['Language'] = df['Language'].apply(lambda x: x if x in ['en', 'pt', 'es'] else detect_language(x))
df = df[df['Language'].isin(['en', 'pt', 'es'])]

# Classify title and abstract
df[['Title Classification', 'Title Score', 'Title Eng Score']] = df['Title'].apply(lambda x: pd.Series(classify_text(x)))
df[['Abstract Classification', 'Abstract Score', 'Abstract Eng Score']] = df['Abstract'].apply(lambda x: pd.Series(classify_text(x)))


# Filter based on classification (assuming positive label is related to "software engineering")
df = df[(df['Title Classification'] == 'LABEL_1') | (df['Abstract Classification'] == 'LABEL_1')]

# Save to a new CSV file
df.to_csv('filtered_scholar_results.csv', index=False)

print("Filtered and classified data saved to 'filtered_scholar_results.csv'")
