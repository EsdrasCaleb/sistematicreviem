import pandas as pd
from keybert import KeyBERT
from transformers import pipeline
from tqdm import tqdm
from langdetect import detect

# Initialize zero-shot-classification pipeline with the best model
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")  # High-performing zero-shot model

def extract_keywords(data_frame):
    """
    Extract keywords from the combination of title and abstract using KeyBERT.

    Parameters:
    - data_frame: pd.DataFrame containing 'title' and 'abstract' columns.

    Adds a new column 'extracted_keywords' to the DataFrame.
    """
    # Initialize KeyBERT model with the best embeddings model
    kw_model = KeyBERT(model='distilbert-base-nli-mean-tokens')  # A robust model for extracting keywords

    # Function to combine title and abstract and extract keywords
    def combine_and_extract(row):
        text = f"{row['title']} {row['abstract']}"
        keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2),top_n=5, stop_words='english')  # Extract top 5 keywords
        # Filter keywords with a score of 0.5 or higher
        filtered_keywords = [kw[0] for kw in keywords if kw[1] >= 0.5]

        return ', '.join(filtered_keywords)  # Join keywords into a single string

    # Apply the keyword extraction function
    tqdm.pandas(desc="Extracting Keywords")
    return data_frame.progress_apply(combine_and_extract, axis=1)


def classify_with_zero_shot(data_frame, candidate_label):
    """
    Classify each row based on the candidate labels using zero-shot classification.

    Parameters:
    - data_frame: pd.DataFrame containing the text to classify (assumed to be combined title and abstract).
    - candidate_labels: list of strings representing the labels to classify against.
    - string_name: string to create the new column name for the scores.

    Adds a new column '{string_name} score' to the DataFrame with classification scores.
    """

    # Function to classify the text
    def classify(row):
        text = f"{row['title']} {row['abstract']}"
        result = classifier(text, [candidate_label], multi_label=False)
        return result['scores'][0]  # Return the score of the highest label

    # Apply the classification function
    tqdm.pandas(desc=f"Classifing in {candidate_label}")
    return data_frame.progress_apply(classify, axis=1)

def detect_language(data_frame):
    """
    Detect the language of the text in the 'abstract' column.

    Parameters:
    - data_frame: pd.DataFrame containing 'abstract' column.

    Adds a new column 'detected_language' to the DataFrame.
    """
    def detect_lang(row):
        text = f"{row['abstract']}"
        try:
            if isinstance(text, str) and text.strip():
                return detect(text)
            else:
                return 'unknown'
        except Exception as e:
            return 'error'  # In case of an error, return 'error'

    tqdm.pandas(desc="Detecting Language")
    return data_frame.progress_apply(detect_lang, axis=1)


def classify_in_batches(text, candidate_keywords, batch_size=20):
    """
    Classifies keywords in batches to avoid overloading the model.

    Parameters:
    - text: The combined title and abstract text.
    - candidate_keywords: List of keywords to classify.
    - batch_size: Number of keywords per batch for classification.

    Returns:
    - filtered_keywords: Top 5 keywords with >50% confidence across all batches.
    """
    all_scores = []

    # Process keywords in batches
    for i in range(0, len(candidate_keywords), batch_size):
        batch = candidate_keywords[i:i + batch_size]
        results = classifier(text, batch)

        # Collect scores for the batch
        all_scores.extend(zip(batch, results['scores']))

    # Filter keywords with confidence > 0.5 and sort by score
    filtered_keywords = [kw for kw, score in sorted(all_scores, key=lambda x: x[1], reverse=True) if score >= 0.5]
    return filtered_keywords[:5]  # Return top 5

def extract_keywords_file(data_frame,file_path):
    with open(file_path, 'r') as file:
        # Read the file content and split by ', '
        keywords_list = file.read().strip().split(', ')

    def combine_and_extract_relevant_keywords(row):
        text = f"{row['title']} {row['abstract']}"

        # Step 2: Classify relevance of keywords in batches
        filtered_keywords = classify_in_batches(text, keywords_list)

        return ', '.join(filtered_keywords)  #

    # Apply the keyword extraction function
    tqdm.pandas(desc="Extracting Keywords")
    return data_frame.progress_apply(combine_and_extract_relevant_keywords, axis=1)