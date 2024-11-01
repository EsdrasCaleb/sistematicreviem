import pandas as pd
from transformers import pipeline


# Load the model and pipeline from Hugging Face
classier_zero = classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")




# Function to classify text
def classify_text(text,keywords=None):
    if(text and isinstance(text, str) and text.strip() ):
        score_label = classier_zero(text, candidate_labels=["game development"])
        # If there are no keywords or abstract, return None
        if isinstance(keywords, str):
            keywordscore = 0
            keywords_arr = keywords.split(',',1)  # Assuming keywords are comma-separated
            if(keywords and len(keywords_arr) > 0):
                result = classier_zero(text, candidate_labels=keywords_arr)
                keywordscore = result['scores'][0]

            print(score_label["scores"][0],keywordscore)
            return score_label["scores"][0],keywordscore
        else:
            print( score_label["scores"][0])
            return score_label["scores"][0]
    else:
        if keywords != None :
            print('blank')
            return 0,0,0
        else:
            return 0,0


# Load the dataset
df = pd.read_csv('resultbitex2.csv')
#df['Keywords'] = df['Keywords'].fillna('')
# Classify title and abstract
def apply_classification(row):
    abstract = row['Abstract']
    keywords = row['Keywords']
    # Ensure classify_text returns the expected number of values
    result = classify_text(abstract, keywords)
    # Return results based on the expected number of columns
    if len(result) == 2:
        return pd.Series(result, index=['Abstract Game Score','Keyword Analyze Abstract',])
    else:
        return pd.Series(result, index=['Abstract Game Score'])

#df[['Abstract Game Score','Keyword Analyze Abstract']] = df.apply(apply_classification, axis=1)


#df[['Abstract Eng Score','Abstract Game Score','Keyword Analyze Abstract']] = df.apply(lambda row: classify_text(row['Abstract'],row['Keywords']), axis=1)
df[['Title Game Score']] = df['Title'].apply(lambda x: pd.Series(classify_text(x)))
df[['Abstract Game Score']] = df['Abstract'].apply(lambda x: pd.Series(classify_text(x)))


# Save to a new CSV file
df.to_csv('results/classified.csv', index=False)

print("Filtered and classified data saved")
