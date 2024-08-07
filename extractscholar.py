import scholarly
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_additional_info(link):
    """
    Scrape additional information from the paper's page.
    This function returns abstract, language, DOI, references, and number of pages if available.
    """
    abstract = None
    language = None
    doi = None
    references = None
    num_pages = None

    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Example: Scrape abstract (depends on the structure of the page)
        abstract_tag = soup.find('meta', {'name': 'description'})
        if abstract_tag:
            abstract = abstract_tag['content']

        # Example: Scrape DOI
        doi_tag = soup.find('a', {'href': lambda x: x and 'doi.org' in x})
        if doi_tag:
            doi = doi_tag.text.strip()

        # Example: Scrape number of pages (if available)
        pages_tag = soup.find(text='Pages')
        if pages_tag and pages_tag.next:
            num_pages = pages_tag.next.strip()

        # Example: Scrape references (this could vary greatly by source)
        references_tag = soup.find(text='References')
        if references_tag and references_tag.next:
            references = references_tag.next.strip()

        # Additional scraping logic for language, etc., can be added here

    except Exception as e:
        print(f"Error scraping {link}: {e}")

    return abstract, language, doi, references, num_pages


def search_scholar(query, num_results=20, start_year=2005, end_year=2025):
    search_query = scholarly.search_pubs(query)
    papers = []

    for i, paper in enumerate(search_query):
        if i >= num_results:
            break

        # Filter by year
        if paper['pub_year'] and (start_year <= paper['pub_year'] <= end_year):
            title = paper.get('bib', {}).get('title', '')
            year = paper.get('pub_year', '')
            num_citations = paper.get('num_citations', 0)
            authors = ', '.join(paper.get('bib', {}).get('author', []))
            source = paper.get('bib', {}).get('venue', '')
            link = paper.get('pub_url', '')

            # Get additional information
            abstract, language, doi, references, num_pages = get_additional_info(link)

            papers.append({
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
                'Number of Pages': num_pages
            })

    return pd.DataFrame(papers)


# Usage example
query = ('("code smell" OR "code smells" OR "bad smells" OR "antipattern" OR "antipatterns") AND game and  ('
         '"programming" OR "development" ) AND ("software testing" OR "tests" OR "unit testing" OR "automated '
         'testing" OR "design patterns") -gamification')
df = search_scholar(query, num_results=20)
print(df)

# Save to CSV
df.to_csv('scholar_results.csv', index=False)