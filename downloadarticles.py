import csv
import os
import requests
from scholarly import scholarly
from pathlib import Path
import re
import time

# Define the output folder
output_folder = "downloaded_articles"
os.makedirs(output_folder, exist_ok=True)


# CSV file path
csv_file = "articles.csv"  # Replace with your actual CSV file

# List to track titles of articles that could not be downloaded
failed_articles = []

def download_via_doi(doi, output_path):
    """Attempt to download the article using the DOI."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    # Use a session to persist cookies and headers
    session = requests.Session()
    session.headers.update(headers)
    doi_url = f"https://doi.org/{doi}"
    if doi.startswith("http"):
        doi_url = doi
    try:
        # Initial request to DOI
        response = session.get(doi_url, allow_redirects=True, stream=True)

        # Check if the response is a PDF
        if response.status_code == 200 and "application/pdf" in response.headers.get("Content-Type", ""):
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"Successfully downloaded PDF via DOI: {doi}")
            return True

        # If not a PDF, follow the redirect
        redirected_url = response.url
        print(f"Redirected to: {redirected_url}")

        # Check if the redirected site is IEEE
        if "ieeexplore.ieee.org" in redirected_url:
            print(f"Detected IEEE site. Attempting to scrape PDF download link {redirected_url}.")
            match = re.search(r"/document/(\d+)", redirected_url)
            if match:
                document_id = match.group(1)
                print(f"Extracted Document ID: {document_id}")

                # Construct the direct PDF download URL
                direct_pdf_url = f"https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber={document_id}"
                print(f"Direct PDF URL: {direct_pdf_url}")
                time.sleep(6)
                # Attempt to download the PDF
                pdf_response = session.get(direct_pdf_url, stream=True, allow_redirects=True)
                if pdf_response.status_code == 200 and "application/pdf" in pdf_response.headers.get("Content-Type",""):
                    with open(output_path, "wb") as f:
                        f.write(pdf_response.content)
                    return True
                else:
                    print(pdf_response.headers)
                    print(pdf_response.url)
                    print(pdf_response.status_code)
                    print(pdf_response.content)
                    print(f"Could not download: {direct_pdf_url}")
            else:
                print(f"Could match document ID {redirected_url}")
        else:
            pdf_response = session.get(redirected_url, stream=True, allow_redirects=True)
            if "application/pdf" in pdf_response.headers.get("Content-Type", ""):
                with open(output_path, "wb") as f:
                    f.write(pdf_response.content)
                return True
            else:
                print(f"Redirected to a non-IEEE site: {redirected_url}")

    except Exception as e:
        print(f"Error occurred while downloading via DOI: {doi}, Error: {e}")
    print(f"Could not download from DOI: {doi_url}")
    return False

def download_via_title(title, output_path):
    time.sleep(6)
    """Search for an article using the title and attempt to download."""

    search_query = scholarly.search_pubs(title)
    article = next(search_query)  # Get the first result


    try:
        if article:
            # Print the structure of the article object for debugging
            print("\nArticle structure:")
            scholarly.pprint(article)

            # Check if 'eprint_url' exists at the top level
            if "eprint_url" in article:
                pdf_url = article["eprint_url"]
                print(f"Found eprint_url: {pdf_url}")
                response = requests.get(pdf_url, stream=True)
                if response.status_code == 200 and "application/pdf" in response.headers.get("Content-Type", ""):
                    with open(output_path, "wb") as f:
                        f.write(response.content)
                    return 1
                else:
                    print("Failed to download PDF from eprint_url.")
            else:
                print("No 'eprint_url' found in the article.")
        else:
            print(f"No articles found for title: {title}")
        print(f"Google blocked")
        return -1
    except Exception as e:
        print(e)
        print(f"Failed to download via title: {title}, Error: {e}")
        return 0

def process_csv(file_path):
    """Process the CSV and download articles."""
    index=52
    google = True
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            index += 1
            title = row.get("title", "").strip()
            doi = row.get("doi", "").strip()
            if not title and not doi:
                continue  # Skip if both title and DOI are missing
            titleArray = title.split()
            titleName = titleArray[0].lower().replace('/', '_')
            if(titleName == "a"):
                titleName = titleArray[1].lower().replace('/', '_')
            output_path = Path(output_folder) / f"{index}_{titleName}.pdf"

            if output_path.exists():
                print(f"Article already downloaded: {title}")
                continue

            downloaded = False
            if doi:
                downloaded = download_via_doi(doi, output_path)

            if not downloaded and title and google:
                print(title)
                downloaded = download_via_title(title, output_path)
                if(downloaded>0):
                    downloaded = True
                elif(downloaded==0):
                    downloaded = False
                else:
                    downloaded = False
                    google = False
                    print(f"Failed to google {index}")
            if not downloaded:
                failed_articles.append(title)

if __name__ == "__main__":
    process_csv(csv_file)

    # Print titles of failed downloads
    if failed_articles:
        print("\nFailed to download the following articles:")
        for title in failed_articles:
            print(f"- {title}")
    else:
        print("\nAll articles were successfully downloaded!")
