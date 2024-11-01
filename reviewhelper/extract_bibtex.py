import os
import pandas as pd
import bibtexparser


def extract_bibtex(folder_path):
    # List to store extracted data
    data = []

    # Loop through each file in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.bib'):  # Assuming BibTeX files have .bib extension
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'r', encoding='utf-8') as f:
                bibtex_str = f.read()

            # Parse the BibTeX file
            bib_data = bibtexparser.loads(bibtex_str)

            for entry in bib_data.entries:
                # Extract relevant information
                title = entry.get('title', '')
                abstract = entry.get('abstract', '')
                keywords = entry.get('keywords', entry.get('author_keywords',''))
                authors = entry.get('author', '')
                source_title = entry.get('journal', entry.get('booktitle', ''))
                date = entry.get('year', '')
                language = entry.get('language', '')
                doi = entry.get('doi', '')
                citations = entry.get('citation', '')
                num_pages = entry.get('pages', '')
                references = entry.get('references', '')
                entry_type = entry.get('ENTRYTYPE', '')

                # Append extracted data to the list
                data.append({
                    'Titulo': title,
                    'Abstract': abstract,
                    'Keywords': keywords,
                    'Autors': authors,
                    'source_title': source_title,
                    'Data': date,
                    'Idioma': language,
                    'file_name': filename,
                    'doi': doi,
                    'citations': citations,
                    'Number of Pages': num_pages,
                    'references': references,
                    'type': entry_type
                })

    # Convert the list to a DataFrame
    df = pd.DataFrame(data)

    return df

