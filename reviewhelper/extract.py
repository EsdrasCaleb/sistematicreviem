import os
import pandas as pd
import bibtexparser


def extract_bibtex(folder_path):
    # List to store extracted data
    data = []

    # Loop through each file in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.bib'):  # Assuming BibTeX files have .bib extension
            print("Reading "+filename)
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'r', encoding='utf-8') as f:
                bibtex_str = f.read()

            # Parse the BibTeX file
            bib_data = bibtexparser.loads(bibtex_str)
            print("File with " + str(len(bib_data.entries))+" entries")
            for entry in bib_data.entries:
                # Extract relevant information


                keywords = []
                if 'keywords' in entry and entry['keywords']:
                    keywords.append(entry['keywords'])
                if 'keywords-plus' in entry and entry['keywords-plus']:
                    keywords.append(entry['keywords-plus'])
                if 'author_keywords' in entry and entry['author_keywords']:
                    keywords.append(entry['author_keywords'])

                title = entry.get('title', '')
                abstract = entry.get('abstract', '')
                keywords = ','.join(keywords)
                authors = entry.get('author', '')
                source_title = entry.get('journal', entry.get('booktitle', ''))
                date = entry.get('year', '')
                language = entry.get('language', '')
                doi = entry.get('doi', '').replace('\\_', '_')
                issn = entry.get('issn', '')
                citations = entry.get('citation', entry.get('times-cited', ''))
                num_pages = entry.get('pages', '')
                references = entry.get('references', entry.get('cited-references', ''))
                entry_type = entry.get('type', entry.get('entrytype',''))

                # Append extracted data to the list
                data.append({
                    'title': title,
                    'abstract': abstract,
                    'keywords': keywords,
                    'autors': authors,
                    'source_title': source_title,
                    'date': date,
                    'language': language,
                    'file_name': filename,
                    'doi': doi,
                    'citations': citations,
                    'number of pages': num_pages,
                    'references': references,
                    'type': entry_type,
                    'issn':issn,
                })
    print("Added "+str(len(data))+" entries")
    # Convert the list to a DataFrame
    df = pd.DataFrame(data)

    return df


def extract_csv(folder_path):
    """
    Extract data from CSV files in a specified folder and return a DataFrame
    with specific columns matching user input, ignoring case.

    Parameters:
    - folder_path: str: path to the folder containing CSV files.

    Returns:
    - pd.DataFrame: Combined DataFrame from all processed CSV files.
    """
    # Define the expected columns
    expected_columns = {
        'title': 'Document Title',
        'abstract': 'Abstract',
        'keywords': 'Author Keywords+IEEE Terms+Mesh_Terms',
        'authors': 'Authors',
        'source_title': 'Publication Title',
        'date': 'Publication Year',
        'language': '',
        'doi': 'DOI',
        'citations': 'Article Citation Count+Patent Citation Count',
        'number of pages': 'Start Page+End Page',
        'references': 'Reference Count',
        'type': 'Document Identifier',
        'issn': 'ISSN',
    }

    # Normalize expected columns for case-insensitive matching
    normalized_columns = {col: item.lower() for col,item in expected_columns.items()}

    # Initialize an empty list to hold DataFrames
    df_list = []

    # Process each CSV file in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_csv(file_path)

            # Display available columns to the user
            print(f"Available columns in '{filename}': {df.columns.tolist()}")

            # Create a new DataFrame with the specified columns
            new_data = {}
            for col_name, default_column in normalized_columns.items():
                # Ask the user for the column name, ignoring case

                user_input = input(f"Please specify the column for '{col_name}' (you can use + to combine columns)(default:{default_column}): ")
                if not user_input:
                    user_input = default_column
                # Split the user input by '+' and strip whitespace
                columns_to_combine = [c.strip().lower() for c in user_input.split('+')]

                # Check if each specified column exists in the DataFrame
                existing_columns = []
                for col in columns_to_combine:
                    if col in df.columns.str.lower().tolist():
                        existing_columns.append(df.columns[df.columns.str.lower() == col].tolist()[0])
                    else:
                        print(f"Warning: Column '{col}' does not exist in '{filename}'.")

                # Combine the specified columns if any exist
                if existing_columns:
                    new_data[col_name] = df[existing_columns].apply(lambda row: ','.join(row.values.astype(str)),
                                                                    axis=1)
                else:
                    collum_string = ','.join(existing_columns)
                    new_data[col_name] = pd.Series([collum_string] * len(df))  # Default to None if no columns are found
                    print(f"Error: Column '{col_name}' does not exist in {filename}. Collum will be filled with ({collum_string})")
                new_data["file_name"] = pd.Series([filename] * len(df))  # Put filename in all
            # Create a new DataFrame with the combined data
            new_df = pd.DataFrame(new_data)
            df_list.append(new_df)
    print("Added " + str(len(df_list)) + " entries")
    # Combine all DataFrames into one
    combined_df = pd.concat(df_list, ignore_index=True)

    return combined_df