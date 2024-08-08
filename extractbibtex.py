import os
import bibtexparser
import pandas as pd
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

def detect_language(text):
    if(text!=''):
        try:
            return detect(text)
        except LangDetectException:
            return ''
    else:
        return ''

def parse_bibtex_file(filepath):
    with open(filepath, 'r') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    entries = bib_database.entries
    return entries


def extract_entry_info(entry):
    title = entry.get('title', '')
    year = entry.get('year', '')
    num_citations = entry.get('citations', '')
    authors = entry.get('author', '')
    source = entry.get('journal', '') or entry.get('booktitle', '') or entry.get('publisher', '')
    abstract = entry.get('abstract', '')
    link = entry.get('url', '')
    language = entry.get('language', detect_language(abstract))
    doi = entry.get('doi', '')
    references = entry.get('references', '')
    num_pages = entry.get('pages', '')
    keywords = entry.get('keywords', entry.get('author_keywords',''))

    return {
        'Title': title,
        'Year': year,
        'Number of Citations': num_citations,
        'Authors': authors,
        'Source': source,
        'Abstract': abstract,
        'Link': link,
        'Language': language,
        'DOI': doi,
        'References': references,
        'Number of Pages': num_pages,
        'Keywords': keywords,
    }


def process_bibtex_files(directory):
    all_entries = []
    for filename in os.listdir(directory):
        if filename.endswith('.bib'):
            filepath = os.path.join(directory, filename)
            entries = parse_bibtex_file(filepath)
            for entry in entries:
                entry_info = extract_entry_info(entry)
                entry_info['Source File'] = filename  # Add the source file column
                all_entries.append(entry_info)
    return all_entries


def save_to_csv(entries, output_filepath):
    df = pd.DataFrame(entries)
    df.to_csv(output_filepath, index=False)


# Directory containing the .bib files
bibtex_directory = 'bibtex2'  # Update this to your directory
output_csv = 'resultbitex.csv'

# Process .bib files and save to CSV
all_entries = process_bibtex_files(bibtex_directory)
save_to_csv(all_entries, output_csv)

print(f'Merged BibTeX entries saved to {output_csv}')
