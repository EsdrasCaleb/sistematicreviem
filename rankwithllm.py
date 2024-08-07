import pandas as pd
from transformers import pipeline
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

# Load the model and pipeline from Hugging Face
classifier_soft = pipeline("text-classification", model="mrm8488/distilroberta-finetuned-software")
classier_zero = classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")




# Function to classify text
def classify_text(text,keywords=None):
    if(text):
        result = classifier_soft(text)
        label = result[0]['label']
        score = result[0]['score']
        score_label = classier_zero(text, candidate_labels=["software engineering","game development"])
        # If there are no keywords or abstract, return None
        soft_index = 0
        game_index = 1
        if(score_label["labels"] == "game development"):
            soft_index = 1
            game_index = 0
        keywordscore = 0
        if keywords:
            # Split keywords if they are in a single string
            if isinstance(keywords, str):
                keywords = keywords.split(',')  # Assuming keywords are comma-separated

            result = classier_zero(text, candidate_labels=keywords)

            scores = result['scores']

            # Calculate and return the mean score
            if scores:
                keywordscore = sum(scores) / len(scores)

        return label, score,score_label["scores"][soft_index],keywordscore,score_label["scores"][game_index]
    else:
        return '',0,0,0,0

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
df[['Title Classification', 'Title Score', 'Title Eng Score','Keyword Analyze Title','Title Game Score']] = df['Title'].apply(lambda x: pd.Series(classify_text(x)))
df[['Abstract Classification', 'Abstract Score', 'Abstract Eng Score',"Keyword Analyze Abstract",'Abstract Game Score']] =df.apply(lambda row: classify_text(row['Keywords'], row['Abstract']), axis=1)


# Filter based on classification (assuming positive label is related to "software engineering")
df = df[(df['Title Classification'] == 'LABEL_1') | (df['Abstract Classification'] == 'LABEL_1')]

# Save to a new CSV file
df.to_csv('filtered_scholar_results.csv', index=False)

print("Filtered and classified data saved to 'filtered_scholar_results.csv'")
