from scholarly import scholarly
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

def search_scholar(query):
    search_query = scholarly.search_pubs(query)
    papers = []

    for i, paper in enumerate(search_query):
        # Filter by year
        title = paper.get('bib', {}).get('title', '')
        year = paper.get('pub_year', '')
        num_citations = paper.get('num_citations', 0)
        authors = ', '.join(paper.get('bib', {}).get('author', []))
        source = paper.get('bib', {}).get('venue', '')
        link = paper.get('pub_url', '')
        abstract = paper.get('bib', {}).get('abstract', '')
        language = paper.get('bib', {}).get('language', detect_language(abstract))
        doi = paper.get('bib', {}).get('doi', None)
        references = paper.get('bib', {}).get('references', None)
        num_pages = paper.get('bib', {}).get('pages', None)
        keywords = ', '.join(paper.get('bib', {}).get('keywords', paper.get('bib', {}).get('author_keywords', [])))


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
            'Number of Pages': num_pages,
            'Keywords': keywords,
        })

    return pd.DataFrame(papers)


# Usage example
query = ('("game development" OR "game programming" OR "video game" OR "game software") AND ( "code smell" OR "bad '
         'smell" OR "technical debt" OR "antipattern" ) AND ( "test" OR "design pattern" ) -gamification')
df = search_scholar(query)

# Save to CSV
df.to_csv('scholar_results.csv', index=False)

print('Merged BibTeX entries saved to scholar_results.csv')