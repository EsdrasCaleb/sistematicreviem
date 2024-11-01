import os
import pandas as pd
from reviewhelper.extract_bibtex import extract_bibtex  # Adjust the import based on your module structure


def main():
    # Define the default folder path
    default_folder = 'bibtex'  # Change this to your actual default path

    # Prompt the user for the folder path
    folder_path = input(
        f"Please enter the path of the folder containing the BibTeX files (default: {default_folder}): ")
    if(not folder_path):
        folder_path = default_folder

    # Check if the entered path is valid
    if not os.path.isdir(folder_path):
        print("The provided path is not a valid directory. Please try again.")
        return

    # Call the extract_bibtex function and get the DataFrame
    df = extract_bibtex(folder_path)

    save_response = input("Do you want to save the extracted BibTeX entries? (yes/no): ").strip().lower()

    if save_response == 'yes':
        default_filename_path = folder_path + "/extracted_bibtex.csv"
        # Prompt for the save location
        save_path = input(
            "Please enter the full path where you want to save the CSV file (default: {default_filename_path}): ")

        # Ensure the directory exists or create it
        save_directory = os.path.dirname(save_path)
        if save_directory and not os.path.isdir(save_directory):
            os.makedirs(save_directory)
        elif not save_path:
            save_path = default_filename_path
        # Save the DataFrame to the specified CSV file
        df.to_csv(save_path, index=False, encoding='utf-8')

        print(f"BibTeX entries have been saved to {save_path}.")
    else:
        print("The extracted BibTeX entries were not saved.")


if __name__ == "__main__":
    main()
