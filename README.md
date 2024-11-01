# sistematicreviem

This project aims to assist in systematic reviews by extracting BibTeX files and exporting them into a CSV format, all while utilizing AI to enhance the process.

## Installation

To set up the project locally, follow these steps:

1. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate the Virtual Environment**:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

3. **Install the Required Packages**:
   ```bash
   pip install -r requirements.txt 
   ```

## Usage Instructions

If you are not familiar with how to run Python scripts, you can simply execute the `main.py` file. This file will guide you through the necessary steps.

### Step 1: Extract Scholar Data

1. Access the **extract scholar** module and input your desired query.
   - **Note**: It is recommended to use a query that extracts fewer than 1000 results from Google Scholar.

### Step 2: Collect BibTeX Entries

1. Go to all relevant portals where you want to search for articles.
2. Extract the BibTeX entries of your search results and place them in the **bibtex** folder.

### Step 3: Remove Duplicates

1. Create a **results** folder.
2. Execute the `remove_duplicates.py` script.
   - Adjust the `remove_by_language_and_abstract` function according to your needs before running the script.
   - If you want to filter out certain domains from the results, modify the `nobooks` variable accordingly.
   - Customize the `rank_with_llm` function to use the term you wish to rank in the search.

### Step 4: Classification and Scoring

1. Modify the classification functions to score your results as desired.
2. Adjust the cut note to refine the results further.

## Contributing

Contributions are welcome! If you have suggestions for improvements or bug fixes, feel free to open an issue or submit a pull request.

## License

This project is licensed under the Apache License 2.0.

---

Made with help from Geto (GPT)