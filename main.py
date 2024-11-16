import os
import pandas as pd
from reviewhelper.extract import extract_bibtex, extract_csv
from reviewhelper.remove_duplicates import remove_duplicates
from reviewhelper.classifier import extract_keywords, detect_language, classify_with_zero_shot, extract_keywords_file


def main():
    # Define the default folder path
    default_folder = 'data'  # Change this to your actual default path
    bib_df, csv_df = pd.DataFrame(), pd.DataFrame()
    question = input(
        "Do you want to extract bibitex?(yes/no) ")
    if question == 'yes':
        # Prompt the user for the folder path
        folder_path = input(
            f"Please enter the path of the folder containing the BibTeX files (default: {default_folder}): ")
        if not folder_path:
            folder_path = default_folder

        # Check if the entered path is valid
        if not os.path.isdir(folder_path):
            print("The provided path is not a valid directory. Please try again.")
        else:
            # Call the extract_bibtex function and get the DataFrame
            bib_df = extract_bibtex(folder_path)
    question = input(
        "Do you want to extract csv?(yes/no) ")
    if question == 'yes':
        # Prompt the user for the folder path
        folder_path = input(
            f"Please enter the path of the folder containing the CSV files (default: {default_folder}): ")
        if not folder_path:
            folder_path = default_folder

        # Check if the entered path is valid
        if not os.path.isdir(folder_path):
            print("The provided path is not a valid directory.")
        else:
            # Call the extract_bibtex function and get the DataFrame
            csv_df = extract_csv(folder_path)

    if(not csv_df.empty and not bib_df.empty):
        # Combine the DataFrames
        df = pd.concat([bib_df, csv_df], ignore_index=True)
    elif(not csv_df.empty and bib_df.empty):
        df = csv_df
    elif(not bib_df.empty and csv_df.empty):
        df = bib_df
    else:
        print("No data provided. Please try again.")
    # Ask the user if they want to remove duplicates
    remove_duplicates_response = input("Do you want to remove duplicates? (yes/no): ").strip().lower()
    while remove_duplicates_response == "yes":
        # Display DataFrame columns
        print("Available columns in the DataFrame:")
        print(df.columns.tolist())

        column_to_check = input("Please enter the column name to check for duplicates: ")

        # Normalize the column names for case-insensitive matching
        normalized_columns = [col.lower() for col in df.columns]
        if column_to_check.lower() not in normalized_columns:
            print(f"Error: Column '{column_to_check}' does not exist.")
        else:
            # Get the actual column name from the DataFrame
            actual_column_name = df.columns[normalized_columns.index(column_to_check.lower())]

            # Show number of rows before removal
            print(f"Number of rows before removal: {len(df)}")

            # Ensure the specified column exists in the DataFrame
            if actual_column_name in df.columns:
                df = remove_duplicates(df, actual_column_name)
                print("\nDuplicates have been removed.")
                print(f"Number of rows after removal: {len(df)}")
        remove_duplicates_response = input("Do you want to remove duplicates? (yes/no): ").strip().lower()

    # Classification: Extract Language
    if 'abstract' in df.columns:
        language_response = input("Do you want to detect the language of the abstracts? (yes/no): ").strip().lower()
        if language_response == 'yes':
            df['detected_language'] = detect_language(data_frame=df)
            print("Detected languages have been added to the DataFrame.")

    # Classification: Extract Keywords
    keywords_response = input("Do you want to extract keywords from the titles and abstracts? (yes/no): ").strip().lower()
    if keywords_response == 'yes':
        df['extracted_keywords'] = extract_keywords(data_frame=df)
        print("Extracted keywords have been added to the DataFrame.")

    keywords_file_response = input(
        "Do you want to find keywords from a file in the titles and abstracts? (yes/no): ").strip().lower()
    if keywords_file_response == 'yes':
        default_file = "key_requirements_engineering.txt"
        keywords_file = input(f"Give file path (default: {default_file}): )")
        if not keywords_file:
            keywords_file = default_file
        df['extracted_keywords'] = extract_keywords_file(data_frame=df,file_path=keywords_file)
        print(f"Extracted keywords of {keywords_file} have been added to the DataFrame.")

    # Classification Loop
    classification_response = input("Do you want to classify your results based on specific label? (yes/no): ").strip().lower()
    while classification_response == "yes":
        label = input("Please enter the classification label: ")
        # Assuming you have a function to classify based on criteria
        df[f"{label} score"] = classify_with_zero_shot(data_frame=df,candidate_label=label)
        print(f"Scores based on '{label}' have been added to the DataFrame.")
        classification_response = input("Do you want to classify again? (yes/no): ").strip().lower()

    save_response = input("Do you want to save the resulting file? (yes/no): ").strip().lower()

    if save_response == 'yes':
        default_filename_path =  "resulting_file.csv"
        # Prompt for the save location
        save_path = input(
            f"Please enter the full path where you want to save the CSV file (default: {default_filename_path}): ")

        # Ensure the directory exists or create it
        save_directory = os.path.dirname(save_path)
        if save_directory and not os.path.isdir(save_directory):
            os.makedirs(save_directory)
        elif not save_path:
            save_path = default_filename_path

        # Save the DataFrame to the specified CSV file
        df.to_csv(save_path, index=False, encoding='utf-8')
        print(f"File entries have been saved to {save_path}.")
    else:
        # Set display options to show the entire DataFrame
        pd.set_option('display.max_rows', None)  # Set max rows to None to show all rows
        pd.set_option('display.max_columns', None)  # Set max columns to None to show all columns
        pd.set_option('display.expand_frame_repr', False)  # Prevent wrapping to multiple lines
        print(df)
        pd.reset_option('display.max_rows')
        pd.reset_option('display.max_columns')
        pd.reset_option('display.expand_frame_repr')


if __name__ == "__main__":
    main()
